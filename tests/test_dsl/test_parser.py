"""
Tests for DSL Parser.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 2, Task 2.4 - Test Requirements:
- Test parsing of all valid constructs
- Test error handling for invalid syntax
- Test complete program parsing
- Test full pipeline (text → tokens → AST)
"""

import pytest
from geometry_prover.dsl.lexer import Lexer, TokenType
from geometry_prover.dsl.parser import Parser, parse_program
from geometry_prover.dsl.ast_nodes import (
    Program, PointDecl, LineDecl, CircleDecl, TriangleDecl,
    EqualConstraint, ParallelConstraint, PerpendicularConstraint, OnConstraint,
    ProveStatement,
    Identifier, Number, SegmentExpr, AngleExpr
)
from geometry_prover.utils import DSLParseError


class TestBasicParsing:
    """Test parsing basic constructs."""

    def test_empty_program(self):
        """Test parsing empty program."""
        text = ""
        program = parse_program(text)
        assert isinstance(program, Program)
        assert len(program.statements) == 0

    def test_single_identifier(self):
        """Test parsing single identifier."""
        lexer = Lexer("A")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ident = parser.parse_identifier()
        assert isinstance(ident, Identifier)
        assert ident.name == "A"

    def test_single_number(self):
        """Test parsing single number."""
        lexer = Lexer("42")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        num = parser.parse_number()
        assert isinstance(num, Number)
        assert num.value == 42.0

    def test_identifier_list(self):
        """Test parsing identifier list."""
        lexer = Lexer("A, B, C")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        idents = parser.parse_identifier_list()
        assert len(idents) == 3
        assert [i.name for i in idents] == ["A", "B", "C"]


class TestDeclarationParsing:
    """Test parsing declaration statements."""

    def test_point_decl_single(self):
        """Test parsing single point declaration."""
        text = "point A"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, PointDecl)
        assert len(stmt.points) == 1
        assert stmt.points[0].name == "A"

    def test_point_decl_multiple(self):
        """Test parsing multiple point declaration."""
        text = "point A, B, C"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, PointDecl)
        assert len(stmt.points) == 3
        assert [p.name for p in stmt.points] == ["A", "B", "C"]

    def test_line_decl(self):
        """Test parsing line declaration."""
        text = "line AB"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, LineDecl)
        assert stmt.name.name == "AB"

    def test_triangle_decl(self):
        """Test parsing triangle declaration."""
        text = "triangle ABC"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, TriangleDecl)
        assert stmt.name.name == "ABC"

    def test_circle_with_radius(self):
        """Test parsing circle with radius."""
        text = "circle O with radius 5"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, CircleDecl)
        assert stmt.center.name == "O"
        assert stmt.radius.value == 5.0
        assert stmt.through_point is None

    def test_circle_through_point(self):
        """Test parsing circle through point."""
        text = "circle O through A"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, CircleDecl)
        assert stmt.center.name == "O"
        assert stmt.through_point.name == "A"
        assert stmt.radius is None


class TestConstraintParsing:
    """Test parsing constraint statements."""

    def test_equal_segments(self):
        """Test parsing segment equality."""
        text = "AB = CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, EqualConstraint)
        assert isinstance(stmt.left, SegmentExpr)
        assert isinstance(stmt.right, SegmentExpr)
        assert stmt.left.identifier.name == "AB"
        assert stmt.right.identifier.name == "CD"

    def test_parallel_segments(self):
        """Test parsing parallel constraint."""
        text = "AB || CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, ParallelConstraint)
        assert stmt.segment1.identifier.name == "AB"
        assert stmt.segment2.identifier.name == "CD"

    def test_parallel_double_slash(self):
        """Test parsing parallel with // operator."""
        text = "AB // CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, ParallelConstraint)

    def test_perpendicular_unicode(self):
        """Test parsing perpendicular with ⊥."""
        text = "AB ⊥ CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, PerpendicularConstraint)
        assert stmt.segment1.identifier.name == "AB"
        assert stmt.segment2.identifier.name == "CD"

    def test_on_constraint(self):
        """Test parsing 'on' constraint."""
        text = "P on AB"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, OnConstraint)
        assert stmt.point.name == "P"
        assert stmt.object.name == "AB"

    def test_angle_equality(self):
        """Test parsing angle equality."""
        text = "angle(ABC) = angle(DEF)"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, EqualConstraint)
        assert isinstance(stmt.left, AngleExpr)
        assert isinstance(stmt.right, AngleExpr)
        assert stmt.left.identifier.name == "ABC"
        assert stmt.right.identifier.name == "DEF"

    def test_angle_equals_number(self):
        """Test parsing angle equals number."""
        text = "angle(ABC) = 90"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, EqualConstraint)
        assert isinstance(stmt.left, AngleExpr)
        assert isinstance(stmt.right, Number)
        assert stmt.left.identifier.name == "ABC"
        assert stmt.right.value == 90.0


class TestProveStatements:
    """Test parsing prove statements."""

    def test_prove_equal_segments(self):
        """Test prove with segment equality."""
        text = "prove AB = CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, ProveStatement)
        assert isinstance(stmt.goal, EqualConstraint)

    def test_prove_parallel(self):
        """Test prove with parallel."""
        text = "prove AB || CD"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, ProveStatement)
        assert isinstance(stmt.goal, ParallelConstraint)

    def test_prove_angle_equality(self):
        """Test prove with angle equality."""
        text = "prove angle(ABC) = angle(DEF)"
        program = parse_program(text)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, ProveStatement)
        goal = stmt.goal
        assert isinstance(goal, EqualConstraint)
        assert isinstance(goal.left, AngleExpr)
        assert isinstance(goal.right, AngleExpr)


class TestCompletePrograms:
    """Test parsing complete DSL programs."""

    def test_isosceles_triangle(self):
        """Test parsing isosceles triangle program."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """
        program = parse_program(text)
        assert len(program.statements) == 4
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], TriangleDecl)
        assert isinstance(program.statements[2], EqualConstraint)
        assert isinstance(program.statements[3], ProveStatement)

    def test_parallel_lines(self):
        """Test parsing parallel lines program."""
        text = """
        point A, B, C, D
        line AB
        line CD
        AB || CD
        """
        program = parse_program(text)
        assert len(program.statements) == 4
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], LineDecl)
        assert isinstance(program.statements[2], LineDecl)
        assert isinstance(program.statements[3], ParallelConstraint)

    def test_circle_construction(self):
        """Test parsing circle construction."""
        text = """
        point O, A
        circle O with radius 5
        A on O
        """
        program = parse_program(text)
        assert len(program.statements) == 3
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], CircleDecl)
        assert isinstance(program.statements[2], OnConstraint)

    def test_right_triangle(self):
        """Test parsing right triangle."""
        text = """
        point A, B, C
        triangle ABC
        angle(ABC) = 90
        """
        program = parse_program(text)
        assert len(program.statements) == 3
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], TriangleDecl)
        assert isinstance(program.statements[2], EqualConstraint)
        # Check angle = 90
        constraint = program.statements[2]
        assert isinstance(constraint.left, AngleExpr)
        assert isinstance(constraint.right, Number)
        assert constraint.right.value == 90.0

    def test_program_with_comments(self):
        """Test parsing program with comments."""
        text = """
        # Isosceles triangle
        point A, B, C
        # Equal sides
        AB = AC
        """
        program = parse_program(text)
        # Comments should be ignored by lexer
        assert len(program.statements) == 2
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], EqualConstraint)


class TestExampleFiles:
    """Test parsing example DSL files."""

    def test_example_01_isosceles(self):
        """Test parsing example 01 (isosceles triangle)."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """
        program = parse_program(text)
        assert len(program.statements) == 4
        # Verify structure
        assert isinstance(program.statements[0], PointDecl)
        assert len(program.statements[0].points) == 3
        assert isinstance(program.statements[1], TriangleDecl)
        assert isinstance(program.statements[2], EqualConstraint)
        assert isinstance(program.statements[3], ProveStatement)

    def test_example_02_parallel(self):
        """Test parsing example with parallel lines."""
        text = """
        point A, B, C, D
        AB || CD
        """
        program = parse_program(text)
        assert len(program.statements) == 2
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], ParallelConstraint)

    def test_example_perpendicular(self):
        """Test parsing perpendicular example."""
        text = """
        point A, B, C
        AB ⊥ BC
        """
        program = parse_program(text)
        assert len(program.statements) == 2
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], PerpendicularConstraint)


class TestErrorHandling:
    """Test parser error handling."""

    def test_unexpected_token(self):
        """Test error on unexpected token."""
        text = "point"  # Missing identifier
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)
        assert "Expected IDENTIFIER" in str(exc_info.value)

    def test_invalid_statement(self):
        """Test error on invalid statement."""
        text = "123"  # Number at statement level
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)
        assert "Unexpected token" in str(exc_info.value)

    def test_missing_operator(self):
        """Test error on missing operator."""
        text = "AB CD"  # Missing operator between segments
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)
        assert "constraint operator" in str(exc_info.value)

    def test_unclosed_parenthesis(self):
        """Test error on unclosed parenthesis."""
        text = "prove angle(ABC"
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)
        assert "Expected RPAREN" in str(exc_info.value)

    def test_error_includes_position(self):
        """Test that errors include line/column."""
        text = "point A\nline"  # Missing identifier on line 2
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)
        error = exc_info.value
        assert error.line == 2


class TestFullPipeline:
    """Test complete parsing pipeline (text → tokens → AST)."""

    def test_pipeline_point_decl(self):
        """Test full pipeline for point declaration."""
        text = "point A, B, C"

        # Step 1: Lexing
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        assert len(tokens) == 7  # POINT, ID, COMMA, ID, COMMA, ID, EOF

        # Step 2: Parsing
        parser = Parser(tokens)
        program = parser.parse()

        # Step 3: AST verification
        assert isinstance(program, Program)
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, PointDecl)
        assert len(stmt.points) == 3

    def test_pipeline_complete_problem(self):
        """Test full pipeline for complete geometry problem."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        # Full pipeline
        program = parse_program(text)

        # Verify AST structure
        assert len(program.statements) == 4

        # Check each statement
        point_decl = program.statements[0]
        assert isinstance(point_decl, PointDecl)
        assert len(point_decl.points) == 3

        triangle_decl = program.statements[1]
        assert isinstance(triangle_decl, TriangleDecl)

        constraint = program.statements[2]
        assert isinstance(constraint, EqualConstraint)

        prove = program.statements[3]
        assert isinstance(prove, ProveStatement)
        assert isinstance(prove.goal, EqualConstraint)

    def test_pipeline_with_all_constructs(self):
        """Test pipeline with all major constructs."""
        text = """
        point A, B, C, O
        line AB
        circle O with radius 5
        triangle ABC
        AB = AC
        AB || CD
        AB ⊥ BC
        P on AB
        angle(ABC) = 90
        prove angle(ABC) = angle(ACB)
        """

        program = parse_program(text)

        # Count statement types
        point_decls = [s for s in program.statements if isinstance(s, PointDecl)]
        line_decls = [s for s in program.statements if isinstance(s, LineDecl)]
        circle_decls = [s for s in program.statements if isinstance(s, CircleDecl)]
        triangle_decls = [s for s in program.statements if isinstance(s, TriangleDecl)]
        equal_constraints = [s for s in program.statements if isinstance(s, EqualConstraint)]
        parallel_constraints = [s for s in program.statements if isinstance(s, ParallelConstraint)]
        perp_constraints = [s for s in program.statements if isinstance(s, PerpendicularConstraint)]
        on_constraints = [s for s in program.statements if isinstance(s, OnConstraint)]
        prove_stmts = [s for s in program.statements if isinstance(s, ProveStatement)]

        assert len(point_decls) == 1
        assert len(line_decls) == 1
        assert len(circle_decls) == 1
        assert len(triangle_decls) == 1
        assert len(equal_constraints) == 2  # AB = AC and angle(ABC) = 90
        assert len(parallel_constraints) == 1
        assert len(perp_constraints) == 1
        assert len(on_constraints) == 1
        assert len(prove_stmts) == 1


class TestParserUtilities:
    """Test parser utility methods."""

    def test_peek(self):
        """Test peek method."""
        lexer = Lexer("point A, B")
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        # Peek at current
        assert parser.peek(0).type == TokenType.POINT
        # Peek ahead
        assert parser.peek(1).type == TokenType.IDENTIFIER
        assert parser.peek(2).type == TokenType.COMMA

    def test_match(self):
        """Test match method."""
        lexer = Lexer("point A")
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        assert parser.match(TokenType.POINT)
        assert not parser.match(TokenType.LINE)
        assert parser.match(TokenType.POINT, TokenType.LINE)  # Multiple types

    def test_advance(self):
        """Test advance method."""
        lexer = Lexer("point A")
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        first = parser.current_token
        assert first.type == TokenType.POINT

        parser.advance()
        assert parser.current_token.type == TokenType.IDENTIFIER


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
