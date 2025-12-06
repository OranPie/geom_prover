"""
Tests for DSL AST Node Definitions.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 2, Task 2.3 - Test Requirements:
- Test all node types can be created
- Test visitor pattern functionality
- Test __repr__ for debugging
"""

import pytest
from geometry_prover.dsl.ast_nodes import (
    # Base classes
    ASTNode, Statement, Constraint, Expression,
    # Statement nodes
    Program, PointDecl, LineDecl, CircleDecl, TriangleDecl,
    EqualConstraint, ParallelConstraint, PerpendicularConstraint, OnConstraint,
    ProveStatement,
    # Expression nodes
    Identifier, Number, SegmentExpr, AngleExpr,
    # Visitor
    ASTVisitor, ASTStringVisitor
)


class TestBasicNodes:
    """Test basic node creation and properties."""

    def test_identifier_creation(self):
        """Test creating identifier node."""
        ident = Identifier("A")
        assert ident.name == "A"

    def test_identifier_repr(self):
        """Test identifier __repr__."""
        ident = Identifier("Point1")
        assert repr(ident) == "Identifier('Point1')"

    def test_identifier_equality(self):
        """Test identifier equality."""
        id1 = Identifier("A")
        id2 = Identifier("A")
        id3 = Identifier("B")
        assert id1 == id2
        assert id1 != id3

    def test_identifier_hash(self):
        """Test identifier can be hashed."""
        id1 = Identifier("A")
        id2 = Identifier("A")
        assert hash(id1) == hash(id2)
        # Can be used in sets
        s = {id1, id2}
        assert len(s) == 1

    def test_number_creation(self):
        """Test creating number node."""
        num = Number(3.14)
        assert num.value == 3.14

    def test_number_repr(self):
        """Test number __repr__."""
        num = Number(90.0)
        assert repr(num) == "Number(90.0)"


class TestExpressionNodes:
    """Test expression node types."""

    def test_segment_expr(self):
        """Test segment expression."""
        seg = SegmentExpr(Identifier("AB"))
        assert seg.identifier.name == "AB"
        assert "SegmentExpr" in repr(seg)

    def test_angle_expr(self):
        """Test angle expression."""
        angle = AngleExpr(Identifier("ABC"))
        assert angle.identifier.name == "ABC"
        assert "AngleExpr" in repr(angle)


class TestDeclarationNodes:
    """Test declaration statement nodes."""

    def test_point_decl_single(self):
        """Test point declaration with single point."""
        decl = PointDecl([Identifier("A")])
        assert len(decl.points) == 1
        assert decl.points[0].name == "A"

    def test_point_decl_multiple(self):
        """Test point declaration with multiple points."""
        decl = PointDecl([
            Identifier("A"),
            Identifier("B"),
            Identifier("C")
        ])
        assert len(decl.points) == 3
        assert [p.name for p in decl.points] == ["A", "B", "C"]

    def test_point_decl_repr(self):
        """Test point declaration __repr__."""
        decl = PointDecl([Identifier("A"), Identifier("B")])
        repr_str = repr(decl)
        assert "PointDecl" in repr_str
        assert "A" in repr_str
        assert "B" in repr_str

    def test_line_decl(self):
        """Test line declaration."""
        decl = LineDecl(Identifier("AB"))
        assert decl.name.name == "AB"
        assert "LineDecl" in repr(decl)

    def test_triangle_decl(self):
        """Test triangle declaration."""
        decl = TriangleDecl(Identifier("ABC"))
        assert decl.name.name == "ABC"
        assert "TriangleDecl" in repr(decl)

    def test_circle_decl_with_radius(self):
        """Test circle declaration with radius."""
        decl = CircleDecl(
            center=Identifier("O"),
            radius=Number(5.0)
        )
        assert decl.center.name == "O"
        assert decl.radius.value == 5.0
        assert decl.through_point is None
        assert "radius" in repr(decl)

    def test_circle_decl_through_point(self):
        """Test circle declaration through point."""
        decl = CircleDecl(
            center=Identifier("O"),
            through_point=Identifier("A")
        )
        assert decl.center.name == "O"
        assert decl.through_point.name == "A"
        assert decl.radius is None
        assert "through" in repr(decl)


class TestConstraintNodes:
    """Test constraint statement nodes."""

    def test_equal_constraint_segments(self):
        """Test equality constraint between segments."""
        seg1 = SegmentExpr(Identifier("AB"))
        seg2 = SegmentExpr(Identifier("CD"))
        constraint = EqualConstraint(seg1, seg2)
        assert constraint.left == seg1
        assert constraint.right == seg2
        assert "=" in repr(constraint)

    def test_equal_constraint_angles(self):
        """Test equality constraint between angles."""
        angle1 = AngleExpr(Identifier("ABC"))
        angle2 = AngleExpr(Identifier("DEF"))
        constraint = EqualConstraint(angle1, angle2)
        assert constraint.left == angle1
        assert constraint.right == angle2

    def test_equal_constraint_angle_number(self):
        """Test equality constraint angle = number."""
        angle = AngleExpr(Identifier("ABC"))
        num = Number(90.0)
        constraint = EqualConstraint(angle, num)
        assert constraint.left == angle
        assert constraint.right == num

    def test_parallel_constraint(self):
        """Test parallel constraint."""
        seg1 = SegmentExpr(Identifier("AB"))
        seg2 = SegmentExpr(Identifier("CD"))
        constraint = ParallelConstraint(seg1, seg2)
        assert constraint.segment1 == seg1
        assert constraint.segment2 == seg2
        assert "||" in repr(constraint)

    def test_perpendicular_constraint(self):
        """Test perpendicular constraint."""
        seg1 = SegmentExpr(Identifier("AB"))
        seg2 = SegmentExpr(Identifier("CD"))
        constraint = PerpendicularConstraint(seg1, seg2)
        assert constraint.segment1 == seg1
        assert constraint.segment2 == seg2
        assert "⊥" in repr(constraint)

    def test_on_constraint(self):
        """Test on constraint."""
        point = Identifier("P")
        line = Identifier("AB")
        constraint = OnConstraint(point, line)
        assert constraint.point == point
        assert constraint.object == line
        assert "on" in repr(constraint)


class TestProveStatement:
    """Test prove statement node."""

    def test_prove_statement(self):
        """Test prove statement creation."""
        goal = EqualConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        prove = ProveStatement(goal)
        assert prove.goal == goal
        assert "ProveStatement" in repr(prove)


class TestProgramNode:
    """Test program root node."""

    def test_empty_program(self):
        """Test empty program."""
        program = Program([])
        assert len(program.statements) == 0
        assert "Program" in repr(program)

    def test_program_single_statement(self):
        """Test program with single statement."""
        stmt = PointDecl([Identifier("A")])
        program = Program([stmt])
        assert len(program.statements) == 1
        assert program.statements[0] == stmt

    def test_program_multiple_statements(self):
        """Test program with multiple statements."""
        stmt1 = PointDecl([Identifier("A"), Identifier("B")])
        stmt2 = LineDecl(Identifier("AB"))
        stmt3 = EqualConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        program = Program([stmt1, stmt2, stmt3])
        assert len(program.statements) == 3


class TestVisitorPattern:
    """Test visitor pattern functionality."""

    def test_identifier_accepts_visitor(self):
        """Test identifier accepts visitor."""
        ident = Identifier("A")

        class CountingVisitor(ASTVisitor):
            def __init__(self):
                self.count = 0

            def visit_identifier(self, node):
                self.count += 1
                return node.name

            # Implement other required methods (stub)
            def visit_program(self, node): pass
            def visit_point_decl(self, node): pass
            def visit_line_decl(self, node): pass
            def visit_circle_decl(self, node): pass
            def visit_triangle_decl(self, node): pass
            def visit_equal_constraint(self, node): pass
            def visit_parallel_constraint(self, node): pass
            def visit_perpendicular_constraint(self, node): pass
            def visit_on_constraint(self, node): pass
            def visit_prove_statement(self, node): pass
            def visit_number(self, node): pass
            def visit_segment_expr(self, node): pass
            def visit_angle_expr(self, node): pass

        visitor = CountingVisitor()
        result = ident.accept(visitor)

        assert result == "A"
        assert visitor.count == 1

    def test_program_accepts_visitor(self):
        """Test program accepts visitor."""
        program = Program([
            PointDecl([Identifier("A")]),
            LineDecl(Identifier("AB"))
        ])

        class CountingVisitor(ASTVisitor):
            def __init__(self):
                self.statement_count = 0

            def visit_program(self, node):
                for stmt in node.statements:
                    stmt.accept(self)
                return self.statement_count

            def visit_point_decl(self, node):
                self.statement_count += 1

            def visit_line_decl(self, node):
                self.statement_count += 1

            # Stubs
            def visit_circle_decl(self, node): pass
            def visit_triangle_decl(self, node): pass
            def visit_equal_constraint(self, node): pass
            def visit_parallel_constraint(self, node): pass
            def visit_perpendicular_constraint(self, node): pass
            def visit_on_constraint(self, node): pass
            def visit_prove_statement(self, node): pass
            def visit_identifier(self, node): pass
            def visit_number(self, node): pass
            def visit_segment_expr(self, node): pass
            def visit_angle_expr(self, node): pass

        visitor = CountingVisitor()
        result = program.accept(visitor)

        assert result == 2


class TestStringVisitor:
    """Test the ASTStringVisitor utility."""

    def test_string_visitor_identifier(self):
        """Test string visitor on identifier."""
        ident = Identifier("A")
        visitor = ASTStringVisitor()
        result = ident.accept(visitor)
        assert result == "A"

    def test_string_visitor_number(self):
        """Test string visitor on number."""
        num = Number(3.14)
        visitor = ASTStringVisitor()
        result = num.accept(visitor)
        assert result == "3.14"

    def test_string_visitor_point_decl(self):
        """Test string visitor on point declaration."""
        decl = PointDecl([Identifier("A"), Identifier("B"), Identifier("C")])
        visitor = ASTStringVisitor()
        result = decl.accept(visitor)
        assert "PointDecl" in result
        assert "A, B, C" in result

    def test_string_visitor_line_decl(self):
        """Test string visitor on line declaration."""
        decl = LineDecl(Identifier("AB"))
        visitor = ASTStringVisitor()
        result = decl.accept(visitor)
        assert "LineDecl" in result
        assert "AB" in result

    def test_string_visitor_triangle_decl(self):
        """Test string visitor on triangle declaration."""
        decl = TriangleDecl(Identifier("ABC"))
        visitor = ASTStringVisitor()
        result = decl.accept(visitor)
        assert "TriangleDecl" in result
        assert "ABC" in result

    def test_string_visitor_circle_radius(self):
        """Test string visitor on circle with radius."""
        decl = CircleDecl(Identifier("O"), radius=Number(5.0))
        visitor = ASTStringVisitor()
        result = decl.accept(visitor)
        assert "CircleDecl" in result
        assert "O" in result
        assert "5.0" in result

    def test_string_visitor_equal_constraint(self):
        """Test string visitor on equal constraint."""
        constraint = EqualConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        visitor = ASTStringVisitor()
        result = constraint.accept(visitor)
        assert "Equal" in result
        assert "AB" in result
        assert "CD" in result

    def test_string_visitor_parallel_constraint(self):
        """Test string visitor on parallel constraint."""
        constraint = ParallelConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        visitor = ASTStringVisitor()
        result = constraint.accept(visitor)
        assert "Parallel" in result
        assert "||" in result

    def test_string_visitor_perpendicular_constraint(self):
        """Test string visitor on perpendicular constraint."""
        constraint = PerpendicularConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        visitor = ASTStringVisitor()
        result = constraint.accept(visitor)
        assert "Perpendicular" in result
        assert "⊥" in result

    def test_string_visitor_on_constraint(self):
        """Test string visitor on 'on' constraint."""
        constraint = OnConstraint(Identifier("P"), Identifier("AB"))
        visitor = ASTStringVisitor()
        result = constraint.accept(visitor)
        assert "On" in result
        assert "P" in result
        assert "AB" in result

    def test_string_visitor_prove_statement(self):
        """Test string visitor on prove statement."""
        goal = EqualConstraint(
            SegmentExpr(Identifier("AB")),
            SegmentExpr(Identifier("CD"))
        )
        prove = ProveStatement(goal)
        visitor = ASTStringVisitor()
        result = prove.accept(visitor)
        assert "Prove" in result

    def test_string_visitor_program(self):
        """Test string visitor on complete program."""
        program = Program([
            PointDecl([Identifier("A"), Identifier("B"), Identifier("C")]),
            TriangleDecl(Identifier("ABC")),
            EqualConstraint(
                SegmentExpr(Identifier("AB")),
                SegmentExpr(Identifier("AC"))
            ),
            ProveStatement(
                EqualConstraint(
                    AngleExpr(Identifier("ABC")),
                    AngleExpr(Identifier("ACB"))
                )
            )
        ])
        visitor = ASTStringVisitor()
        result = program.accept(visitor)

        # Check that all components are present
        assert "Program" in result
        assert "PointDecl" in result
        assert "TriangleDecl" in result
        assert "Equal" in result
        assert "Prove" in result


class TestComplexAST:
    """Test building complex AST structures."""

    def test_isosceles_triangle_ast(self):
        """Test AST for isosceles triangle problem."""
        # point A, B, C
        # triangle ABC
        # AB = AC
        # prove angle(ABC) = angle(ACB)

        program = Program([
            PointDecl([Identifier("A"), Identifier("B"), Identifier("C")]),
            TriangleDecl(Identifier("ABC")),
            EqualConstraint(
                SegmentExpr(Identifier("AB")),
                SegmentExpr(Identifier("AC"))
            ),
            ProveStatement(
                EqualConstraint(
                    AngleExpr(Identifier("ABC")),
                    AngleExpr(Identifier("ACB"))
                )
            )
        ])

        assert len(program.statements) == 4
        assert isinstance(program.statements[0], PointDecl)
        assert isinstance(program.statements[1], TriangleDecl)
        assert isinstance(program.statements[2], EqualConstraint)
        assert isinstance(program.statements[3], ProveStatement)

    def test_parallel_lines_ast(self):
        """Test AST for parallel lines problem."""
        # point A, B, C, D
        # AB || CD

        program = Program([
            PointDecl([
                Identifier("A"),
                Identifier("B"),
                Identifier("C"),
                Identifier("D")
            ]),
            ParallelConstraint(
                SegmentExpr(Identifier("AB")),
                SegmentExpr(Identifier("CD"))
            )
        ])

        assert len(program.statements) == 2
        parallel = program.statements[1]
        assert isinstance(parallel, ParallelConstraint)
        assert parallel.segment1.identifier.name == "AB"
        assert parallel.segment2.identifier.name == "CD"

    def test_right_angle_ast(self):
        """Test AST for right angle problem."""
        # triangle ABC
        # angle(ABC) = 90

        program = Program([
            TriangleDecl(Identifier("ABC")),
            EqualConstraint(
                AngleExpr(Identifier("ABC")),
                Number(90.0)
            )
        ])

        assert len(program.statements) == 2
        equal = program.statements[1]
        assert isinstance(equal, EqualConstraint)
        assert isinstance(equal.left, AngleExpr)
        assert isinstance(equal.right, Number)
        assert equal.right.value == 90.0

    def test_circle_construction_ast(self):
        """Test AST for circle construction."""
        # point O, A
        # circle O with radius 5
        # A on circle O

        program = Program([
            PointDecl([Identifier("O"), Identifier("A")]),
            CircleDecl(Identifier("O"), radius=Number(5.0)),
            OnConstraint(Identifier("A"), Identifier("O"))
        ])

        assert len(program.statements) == 3
        circle = program.statements[1]
        assert isinstance(circle, CircleDecl)
        assert circle.center.name == "O"
        assert circle.radius.value == 5.0


class TestNodeTraversal:
    """Test traversing AST with visitor."""

    def test_collect_all_identifiers(self):
        """Test collecting all identifiers from AST."""
        program = Program([
            PointDecl([Identifier("A"), Identifier("B")]),
            LineDecl(Identifier("AB")),
            EqualConstraint(
                SegmentExpr(Identifier("AB")),
                SegmentExpr(Identifier("CD"))
            )
        ])

        class IdentifierCollector(ASTVisitor):
            def __init__(self):
                self.identifiers = []

            def visit_program(self, node):
                for stmt in node.statements:
                    stmt.accept(self)

            def visit_point_decl(self, node):
                for point in node.points:
                    point.accept(self)

            def visit_line_decl(self, node):
                node.name.accept(self)

            def visit_equal_constraint(self, node):
                node.left.accept(self)
                node.right.accept(self)

            def visit_segment_expr(self, node):
                node.identifier.accept(self)

            def visit_identifier(self, node):
                self.identifiers.append(node.name)

            # Stubs
            def visit_circle_decl(self, node): pass
            def visit_triangle_decl(self, node): pass
            def visit_parallel_constraint(self, node): pass
            def visit_perpendicular_constraint(self, node): pass
            def visit_on_constraint(self, node): pass
            def visit_prove_statement(self, node): pass
            def visit_number(self, node): pass
            def visit_angle_expr(self, node): pass

        collector = IdentifierCollector()
        program.accept(collector)

        # Should have collected: A, B (from point decl), AB (from line decl),
        # AB, CD (from equal constraint)
        assert "A" in collector.identifiers
        assert "B" in collector.identifiers
        assert "AB" in collector.identifiers
        assert "CD" in collector.identifiers


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
