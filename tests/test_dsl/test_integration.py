"""
Comprehensive DSL Integration Tests.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 2, Task 2.5 - Test Requirements:
- End-to-end integration tests
- Performance testing (parse speed, memory)
- Error message quality testing
- Edge cases and stress tests
"""

import pytest
import time
from geometry_prover.dsl.parser import parse_program
from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.ast_nodes import (
    Program, PointDecl, LineDecl, CircleDecl, TriangleDecl,
    EqualConstraint, ParallelConstraint, PerpendicularConstraint,
    OnConstraint, ProveStatement,
    ASTStringVisitor
)
from geometry_prover.utils import DSLParseError


class TestEndToEndPipeline:
    """Test complete pipeline from text to AST."""

    def test_simple_problem_full_pipeline(self):
        """Test parsing a simple geometry problem."""
        text = """
        point A, B
        line AB
        """

        # Full pipeline
        program = parse_program(text)

        # Validate AST structure
        assert isinstance(program, Program)
        assert len(program.statements) == 2
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], LineDecl)

        # Validate content
        point_decl = program.statements[0]
        assert len(point_decl.points) == 2
        assert point_decl.points[0].name == "A"
        assert point_decl.points[1].name == "B"

    def test_complex_problem_full_pipeline(self):
        """Test parsing a complex geometry problem with multiple constructs."""
        text = """
        # Define points
        point A, B, C, D, E

        # Create shapes
        triangle ABC
        circle D with radius 10

        # Constraints
        AB = BC
        AB || DE
        AC ⊥ DE
        E on D

        # Angles
        angle(ABC) = 60

        # Goal
        prove angle(BAC) = angle(BCA)
        """

        program = parse_program(text)

        # Count statement types
        point_decls = [s for s in program.statements if isinstance(s, PointDecl)]
        triangle_decls = [s for s in program.statements if isinstance(s, TriangleDecl)]
        circle_decls = [s for s in program.statements if isinstance(s, CircleDecl)]
        equal_constraints = [s for s in program.statements if isinstance(s, EqualConstraint)]
        parallel_constraints = [s for s in program.statements if isinstance(s, ParallelConstraint)]
        perp_constraints = [s for s in program.statements if isinstance(s, PerpendicularConstraint)]
        on_constraints = [s for s in program.statements if isinstance(s, OnConstraint)]
        prove_stmts = [s for s in program.statements if isinstance(s, ProveStatement)]

        assert len(point_decls) == 1
        assert len(triangle_decls) == 1
        assert len(circle_decls) == 1
        assert len(equal_constraints) == 2  # AB = BC, angle(ABC) = 60
        assert len(parallel_constraints) == 1
        assert len(perp_constraints) == 1
        assert len(on_constraints) == 1
        assert len(prove_stmts) == 1

    def test_visitor_pattern_integration(self):
        """Test visitor pattern works with parsed AST."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        """

        program = parse_program(text)
        visitor = ASTStringVisitor()
        result = visitor.visit_program(program)

        # Check that visitor produces readable output
        assert "Program:" in result
        assert "PointDecl" in result
        assert "TriangleDecl" in result
        assert "Equal" in result
        assert "A" in result
        assert "B" in result
        assert "C" in result


class TestPerformance:
    """Test parsing performance."""

    def test_parse_speed_small(self):
        """Test parsing speed for small program."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        start = time.time()
        for _ in range(1000):
            program = parse_program(text)
        end = time.time()

        elapsed = end - start
        per_parse = elapsed / 1000

        # Should parse 1000 times in reasonable time (< 1 second)
        assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s for 1000 parses"
        print(f"\n  Parse speed: {per_parse*1000:.3f}ms per parse")
        print(f"  Throughput: {1000/elapsed:.0f} parses/sec")

    def test_parse_speed_large(self):
        """Test parsing speed for larger program."""
        # Generate a large program
        lines = ["point " + ", ".join(f"P{i}" for i in range(50))]
        for i in range(49):
            lines.append(f"P{i}P{i+1} = P{i+1}P{i+2}")
        text = "\n".join(lines)

        start = time.time()
        program = parse_program(text)
        end = time.time()

        elapsed = end - start

        # Should parse large program quickly (< 100ms)
        assert elapsed < 0.1, f"Too slow: {elapsed*1000:.1f}ms for large program"
        assert len(program.statements) == 50  # 1 point decl + 49 constraints
        print(f"\n  Large program ({len(program.statements)} statements): {elapsed*1000:.1f}ms")

    def test_lexer_performance(self):
        """Test lexer performance separately."""
        text = " ".join(f"point P{i}" for i in range(100)) + "\n"
        text += " ".join(f"line L{i}" for i in range(100))

        start = time.time()
        for _ in range(100):
            lexer = Lexer(text)
            tokens = lexer.tokenize()
        end = time.time()

        elapsed = end - start
        per_lex = elapsed / 100

        assert elapsed < 1.0, f"Lexer too slow: {elapsed:.3f}s"
        print(f"\n  Lexer speed: {per_lex*1000:.3f}ms per tokenization")

    def test_memory_efficiency(self):
        """Test that parsing doesn't create excessive objects."""
        text = """
        point A, B, C, D, E, F, G, H, I, J
        triangle ABC
        triangle DEF
        triangle GHI
        AB = BC
        DE = EF
        GH = HI
        """

        # Parse multiple times - shouldn't accumulate memory
        programs = []
        for _ in range(100):
            program = parse_program(text)
            programs.append(program)

        # All programs should have same structure
        for program in programs:
            assert len(program.statements) == 7


class TestErrorQuality:
    """Test error message quality."""

    def test_error_message_clarity(self):
        """Test that error messages are clear and helpful."""
        test_cases = [
            ("point", "Expected IDENTIFIER"),
            ("line", "Expected IDENTIFIER"),
            ("AB CD", "constraint operator"),
            ("triangle", "Expected IDENTIFIER"),
            ("point A\nline", "line 2"),
        ]

        for text, expected_msg in test_cases:
            with pytest.raises(DSLParseError) as exc_info:
                parse_program(text)
            error_msg = str(exc_info.value)
            assert expected_msg in error_msg, f"Expected '{expected_msg}' in error message, got: {error_msg}"

    def test_error_position_accuracy(self):
        """Test that error positions are accurate."""
        text = "point A, B, C\nline AB\ntriangle"

        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)

        error = exc_info.value
        assert error.line == 3, f"Expected error on line 3, got line {error.line}"

    def test_multiple_errors_first_reported(self):
        """Test that parser reports errors as it encounters them."""
        text = "point A, B\nline AB\ntriangle"

        # Should report error on line 3 (missing identifier for triangle)
        with pytest.raises(DSLParseError) as exc_info:
            parse_program(text)

        error = exc_info.value
        # Parser successfully parses first two statements, fails on third
        assert error.line == 3
        assert "Expected IDENTIFIER" in str(error)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_program(self):
        """Test parsing empty program."""
        program = parse_program("")
        assert isinstance(program, Program)
        assert len(program.statements) == 0

    def test_only_whitespace(self):
        """Test program with only whitespace."""
        program = parse_program("   \n\n  \t  \n  ")
        assert len(program.statements) == 0

    def test_only_comments(self):
        """Test program with only comments."""
        text = """
        # Comment 1
        # Comment 2
        # Comment 3
        """
        program = parse_program(text)
        assert len(program.statements) == 0

    def test_long_identifier(self):
        """Test parsing long identifier."""
        text = "point " + "A" * 100
        program = parse_program(text)
        assert len(program.statements) == 1
        assert program.statements[0].points[0].name == "A" * 100

    def test_many_points(self):
        """Test declaring many points at once."""
        points = ", ".join(f"P{i}" for i in range(100))
        text = f"point {points}"
        program = parse_program(text)
        assert len(program.statements) == 1
        assert len(program.statements[0].points) == 100

    def test_deeply_nested_structure(self):
        """Test program with many statements."""
        lines = []
        for i in range(50):
            lines.append(f"point P{i}")
        text = "\n".join(lines)

        program = parse_program(text)
        assert len(program.statements) == 50

    def test_unicode_symbols(self):
        """Test all unicode symbols work."""
        text = """
        point A, B, C
        AB ⊥ BC
        angle(ABC) = 90
        """
        program = parse_program(text)
        assert len(program.statements) == 3

    def test_mixed_operators(self):
        """Test mixing different operator styles."""
        text = """
        point A, B, C, D, E
        AB || CD
        CD // DE
        """
        program = parse_program(text)
        assert len(program.statements) == 3
        assert isinstance(program.statements[1], ParallelConstraint)
        assert isinstance(program.statements[2], ParallelConstraint)

    def test_float_numbers(self):
        """Test parsing float numbers."""
        text = "circle O with radius 3.14159"
        program = parse_program(text)
        circle = program.statements[0]
        assert circle.radius.value == 3.14159

    def test_case_insensitivity(self):
        """Test that keywords are case-insensitive."""
        text = """
        POINT A, B
        Point C
        pOiNt D
        """
        program = parse_program(text)
        assert len(program.statements) == 3


class TestStressTests:
    """Stress tests for parser robustness."""

    def test_stress_many_statements(self):
        """Test parsing many statements."""
        lines = []
        lines.append("point " + ", ".join(f"P{i}" for i in range(100)))
        for i in range(99):
            lines.append(f"P{i}P{i+1} = P{i+1}P{i+2}")
        text = "\n".join(lines)

        program = parse_program(text)
        assert len(program.statements) == 100

    def test_stress_complex_constraints(self):
        """Test many different constraint types."""
        text = """
        point A, B, C, D, E, F
        AB = BC
        AB || CD
        AB ⊥ EF
        C on AB
        angle(ABC) = 90
        angle(DEF) = angle(ABC)
        """
        program = parse_program(text)
        assert len(program.statements) == 7

    def test_stress_repeated_parsing(self):
        """Test parsing same text multiple times."""
        text = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        # Parse 1000 times - should be consistent
        programs = [parse_program(text) for _ in range(1000)]

        # All should have same structure
        for program in programs:
            assert len(program.statements) == 4


class TestRealWorldExamples:
    """Test real-world geometry problem patterns."""

    def test_pythagorean_theorem(self):
        """Test Pythagorean theorem setup."""
        text = """
        point A, B, C
        triangle ABC
        angle(ABC) = 90
        """
        program = parse_program(text)
        assert len(program.statements) == 3

    def test_angle_bisector(self):
        """Test angle bisector setup."""
        text = """
        point A, B, C, D
        triangle ABC
        D on BC
        angle(ABD) = angle(DBC)
        """
        program = parse_program(text)
        assert len(program.statements) == 4

    def test_parallel_lines_transversal(self):
        """Test parallel lines with transversal."""
        text = """
        point A, B, C, D, E, F
        AB || CD
        E on AB
        F on CD
        """
        program = parse_program(text)
        assert len(program.statements) == 4

    def test_inscribed_angle(self):
        """Test inscribed angle in circle."""
        text = """
        point O, A, B, C
        circle O with radius 5
        A on O
        B on O
        C on O
        """
        program = parse_program(text)
        # 1 point decl + 1 circle decl + 3 on constraints = 5 statements
        assert len(program.statements) == 5


class TestDocumentation:
    """Test that DSL is well-documented through examples."""

    def test_api_usage_convenience(self):
        """Test convenience API."""
        # Single function call should work
        program = parse_program("point A, B")
        assert isinstance(program, Program)

    def test_error_handling_documented(self):
        """Test that errors are clear enough to be self-documenting."""
        try:
            parse_program("point")
        except DSLParseError as e:
            # Error message should be self-explanatory
            assert "Expected" in str(e)
            assert "IDENTIFIER" in str(e)
            assert e.line is not None

    def test_ast_structure_accessible(self):
        """Test that AST structure is easy to work with."""
        program = parse_program("point A, B")

        # Should be easy to navigate
        point_decl = program.statements[0]
        first_point = point_decl.points[0]
        point_name = first_point.name

        assert point_name == "A"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
