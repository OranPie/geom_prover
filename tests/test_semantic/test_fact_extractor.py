"""
Tests for FactExtractor.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 3, Task 3.4 - Test Requirements:
- Test processing all declaration types
- Test constraint and goal extraction
- Test integration with DSL parser
- Test complete program processing
"""

import pytest
from geometry_prover.semantic.fact_extractor import FactExtractor, extract_facts
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.dsl.ast_nodes import (
    Program, PointDecl, LineDecl, CircleDecl, TriangleDecl,
    EqualConstraint, ParallelConstraint, PerpendicularConstraint,
    OnConstraint, ProveStatement,
    Identifier, Number, SegmentExpr, AngleExpr
)
from geometry_prover.facts.fact_types import (
    EqualSegment, EqualAngle, Parallel, Perpendicular, On, RightAngle
)


class TestFactExtractorDeclarations:
    """Test FactExtractor handling of declaration statements."""

    def test_extract_point_declarations(self):
        """Test extracting point declarations."""
        program = Program([
            PointDecl([Identifier("A"), Identifier("B"), Identifier("C")])
        ])

        model = extract_facts(program)

        assert len(model.points) == 3
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert "A" in model.declared_points
        assert "B" in model.declared_points
        assert "C" in model.declared_points

    def test_extract_line_declaration(self):
        """Test extracting line declaration."""
        program = Program([
            LineDecl(Identifier("AB"))
        ])

        model = extract_facts(program)

        # Line AB should create points A and B implicitly
        assert len(model.points) == 2
        assert model.has_point("A")
        assert model.has_point("B")
        assert len(model.lines) == 1
        assert model.has_line("AB")

        # Points created implicitly, line declared
        assert "A" not in model.declared_points
        assert "B" not in model.declared_points

    def test_extract_circle_declaration_with_radius(self):
        """Test extracting circle with explicit radius."""
        program = Program([
            CircleDecl(center=Identifier("O"), radius=Number(5.0))
        ])

        model = extract_facts(program)

        assert len(model.circles) == 1
        assert model.has_point("O")  # Center created implicitly

    def test_extract_circle_declaration_through_point(self):
        """Test extracting circle through point."""
        program = Program([
            CircleDecl(center=Identifier("O"), through_point=Identifier("A"))
        ])

        model = extract_facts(program)

        assert len(model.circles) == 1
        assert model.has_point("O")

    def test_extract_triangle_declaration(self):
        """Test extracting triangle declaration."""
        program = Program([
            TriangleDecl(Identifier("ABC"))
        ])

        model = extract_facts(program)

        # Triangle ABC creates points A, B, C and segments
        assert len(model.points) == 3
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert len(model.triangles) == 1


class TestFactExtractorConstraints:
    """Test FactExtractor handling of constraint statements."""

    def test_extract_equal_segments_constraint(self):
        """Test extracting equal segments constraint."""
        program = Program([
            EqualConstraint(
                left=SegmentExpr(Identifier("AB")),
                right=SegmentExpr(Identifier("CD"))
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], EqualSegment)

    def test_extract_equal_angles_constraint(self):
        """Test extracting equal angles constraint."""
        program = Program([
            EqualConstraint(
                left=AngleExpr(Identifier("ABC")),
                right=AngleExpr(Identifier("DEF"))
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], EqualAngle)

    def test_extract_right_angle_constraint(self):
        """Test extracting right angle constraint."""
        program = Program([
            EqualConstraint(
                left=AngleExpr(Identifier("ABC")),
                right=Number(90.0)
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], RightAngle)

    def test_extract_parallel_constraint(self):
        """Test extracting parallel constraint."""
        program = Program([
            ParallelConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], Parallel)

    def test_extract_perpendicular_constraint(self):
        """Test extracting perpendicular constraint."""
        program = Program([
            PerpendicularConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], Perpendicular)

    def test_extract_on_constraint(self):
        """Test extracting point-on-line constraint."""
        program = Program([
            OnConstraint(
                point=Identifier("P"),
                object=Identifier("AB")
            )
        ])

        model = extract_facts(program)

        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], On)


class TestFactExtractorProveStatements:
    """Test FactExtractor handling of prove statements."""

    def test_extract_prove_equal_segments(self):
        """Test extracting prove goal for equal segments."""
        program = Program([
            ProveStatement(
                goal=EqualConstraint(
                    left=SegmentExpr(Identifier("AB")),
                    right=SegmentExpr(Identifier("CD"))
                )
            )
        ])

        model = extract_facts(program)

        assert len(model.prove_goals) == 1
        assert isinstance(model.prove_goals[0], EqualSegment)

    def test_extract_prove_equal_angles(self):
        """Test extracting prove goal for equal angles."""
        program = Program([
            ProveStatement(
                goal=EqualConstraint(
                    left=AngleExpr(Identifier("ABC")),
                    right=AngleExpr(Identifier("DEF"))
                )
            )
        ])

        model = extract_facts(program)

        assert len(model.prove_goals) == 1
        assert isinstance(model.prove_goals[0], EqualAngle)

    def test_extract_prove_parallel(self):
        """Test extracting prove goal for parallel lines."""
        program = Program([
            ProveStatement(
                goal=ParallelConstraint(
                    segment1=SegmentExpr(Identifier("AB")),
                    segment2=SegmentExpr(Identifier("CD"))
                )
            )
        ])

        model = extract_facts(program)

        assert len(model.prove_goals) == 1
        assert isinstance(model.prove_goals[0], Parallel)


class TestFactExtractorIntegration:
    """Test FactExtractor with complete programs."""

    def test_extract_isosceles_triangle_problem(self):
        """Test extracting complete isosceles triangle problem."""
        program = Program([
            # point A, B, C
            PointDecl([Identifier("A"), Identifier("B"), Identifier("C")]),

            # triangle ABC
            TriangleDecl(Identifier("ABC")),

            # AB = AC
            EqualConstraint(
                left=SegmentExpr(Identifier("AB")),
                right=SegmentExpr(Identifier("AC"))
            ),

            # prove angle(ABC) = angle(ACB)
            ProveStatement(
                goal=EqualConstraint(
                    left=AngleExpr(Identifier("ABC")),
                    right=AngleExpr(Identifier("ACB"))
                )
            )
        ])

        model = extract_facts(program)

        # Verify structure
        assert len(model.points) == 3
        assert len(model.triangles) == 1
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1

        # Verify constraint and goal types
        assert isinstance(model.constraints[0], EqualSegment)
        assert isinstance(model.prove_goals[0], EqualAngle)

    def test_extract_parallel_lines_problem(self):
        """Test extracting parallel lines problem."""
        program = Program([
            # line AB
            LineDecl(Identifier("AB")),

            # line CD
            LineDecl(Identifier("CD")),

            # AB || CD
            ParallelConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            ),

            # line EF
            LineDecl(Identifier("EF")),

            # prove EF || AB
            ProveStatement(
                goal=ParallelConstraint(
                    segment1=SegmentExpr(Identifier("EF")),
                    segment2=SegmentExpr(Identifier("AB"))
                )
            )
        ])

        model = extract_facts(program)

        assert len(model.lines) == 3
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1
        assert isinstance(model.constraints[0], Parallel)
        assert isinstance(model.prove_goals[0], Parallel)

    def test_extract_right_triangle_problem(self):
        """Test extracting right triangle problem."""
        program = Program([
            # point A, B, C
            PointDecl([Identifier("A"), Identifier("B"), Identifier("C")]),

            # triangle ABC
            TriangleDecl(Identifier("ABC")),

            # angle(ABC) = 90
            EqualConstraint(
                left=AngleExpr(Identifier("ABC")),
                right=Number(90.0)
            ),

            # AB = BC
            EqualConstraint(
                left=SegmentExpr(Identifier("AB")),
                right=SegmentExpr(Identifier("BC"))
            )
        ])

        model = extract_facts(program)

        assert len(model.points) == 3
        assert len(model.triangles) == 1
        assert len(model.constraints) == 2
        assert isinstance(model.constraints[0], RightAngle)
        assert isinstance(model.constraints[1], EqualSegment)

    def test_extract_mixed_statements(self):
        """Test extracting program with mixed statement types."""
        program = Program([
            PointDecl([Identifier("A"), Identifier("B")]),
            LineDecl(Identifier("AB")),
            CircleDecl(center=Identifier("O"), radius=Number(3.0)),
            TriangleDecl(Identifier("ABC")),
            ParallelConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            ),
            ProveStatement(
                goal=EqualConstraint(
                    left=SegmentExpr(Identifier("AB")),
                    right=SegmentExpr(Identifier("CD"))
                )
            )
        ])

        model = extract_facts(program)

        # Verify all components present
        assert len(model.points) >= 2
        assert len(model.lines) >= 1
        assert len(model.circles) == 1
        assert len(model.triangles) == 1
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1

    def test_reuse_existing_model(self):
        """Test that FactExtractor can use existing model."""
        # Create model with some initial points
        existing_model = GeometryModel()
        existing_model.add_point("A")
        existing_model.add_point("B")

        # Extract facts into existing model
        program = Program([
            PointDecl([Identifier("C"), Identifier("D")])
        ])

        extractor = FactExtractor(model=existing_model)
        model = extractor.extract_from_program(program)

        # Should have all 4 points
        assert len(model.points) == 4
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert model.has_point("D")


class TestFactExtractorWithParser:
    """Test FactExtractor integration with DSL parser."""

    def test_extract_from_parsed_program(self):
        """Test extracting facts from parsed DSL program."""
        from geometry_prover.dsl.parser import parse_program

        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        # Parse DSL
        program = parse_program(dsl_code)

        # Extract facts
        model = extract_facts(program)

        # Verify complete pipeline
        assert len(model.points) == 3
        assert len(model.triangles) == 1
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1
        assert isinstance(model.constraints[0], EqualSegment)
        assert isinstance(model.prove_goals[0], EqualAngle)

    def test_extract_complex_parsed_program(self):
        """Test extracting from complex parsed program."""
        from geometry_prover.dsl.parser import parse_program

        dsl_code = """
        point A, B, C, D
        line AB
        line CD
        AB || CD
        point E, F
        line EF
        EF ⊥ AB
        prove EF ⊥ CD
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify
        assert len(model.points) == 6
        assert len(model.lines) == 3
        assert len(model.constraints) == 2  # AB || CD, EF ⊥ AB
        assert len(model.prove_goals) == 1  # prove EF ⊥ CD

        # Check constraint types
        constraint_types = [type(c).__name__ for c in model.constraints]
        assert "Parallel" in constraint_types
        assert "Perpendicular" in constraint_types


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
