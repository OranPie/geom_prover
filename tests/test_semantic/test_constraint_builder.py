"""
Tests for ConstraintBuilder and ProveGoalExtractor.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 3, Tasks 3.2 & 3.3 - Test Requirements:
- Test constraint conversion (all constraint types)
- Test goal extraction from ProveStatements
- Test integration with GeometryModel
"""

import pytest
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.semantic.constraint_builder import ConstraintBuilder
from geometry_prover.semantic.prove_goal_extractor import ProveGoalExtractor
from geometry_prover.dsl.ast_nodes import (
    EqualConstraint, ParallelConstraint, PerpendicularConstraint,
    OnConstraint, ProveStatement,
    SegmentExpr, AngleExpr, Number, Identifier
)
from geometry_prover.facts.fact_types import (
    EqualSegment, EqualAngle, Parallel, Perpendicular, On, RightAngle
)


class TestConstraintBuilder:
    """Test ConstraintBuilder functionality."""

    def test_build_equal_segments(self):
        """Test building EqualSegment fact."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: AB = CD
        constraint = EqualConstraint(
            left=SegmentExpr(Identifier("AB")),
            right=SegmentExpr(Identifier("CD"))
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, EqualSegment)
        assert fact.parameters["segment1"].point1.name == "A"
        assert fact.parameters["segment1"].point2.name == "B"
        assert fact.parameters["segment2"].point1.name == "C"
        assert fact.parameters["segment2"].point2.name == "D"

    def test_build_equal_angles(self):
        """Test building EqualAngle fact."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: angle(ABC) = angle(DEF)
        constraint = EqualConstraint(
            left=AngleExpr(Identifier("ABC")),
            right=AngleExpr(Identifier("DEF"))
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, EqualAngle)
        angle1 = fact.parameters["angle1"]
        angle2 = fact.parameters["angle2"]
        assert angle1.point1.name == "A"
        assert angle1.vertex.name == "B"
        assert angle1.point2.name == "C"
        assert angle2.point1.name == "D"
        assert angle2.vertex.name == "E"
        assert angle2.point2.name == "F"

    def test_build_right_angle(self):
        """Test building RightAngle fact from angle = 90."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: angle(ABC) = 90
        constraint = EqualConstraint(
            left=AngleExpr(Identifier("ABC")),
            right=Number(90.0)
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, RightAngle)
        # RightAngle uses an angle
        angle = fact.parameters["angle"]
        assert angle.point1.name == "A"
        assert angle.vertex.name == "B"
        assert angle.point2.name == "C"

    def test_build_parallel_constraint(self):
        """Test building Parallel fact."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: AB || CD
        constraint = ParallelConstraint(
            segment1=SegmentExpr(Identifier("AB")),
            segment2=SegmentExpr(Identifier("CD"))
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, Parallel)
        assert fact.parameters["line1"].point1.name == "A"
        assert fact.parameters["line2"].point1.name == "C"

    def test_build_perpendicular_constraint(self):
        """Test building Perpendicular fact."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: AB ⊥ CD
        constraint = PerpendicularConstraint(
            segment1=SegmentExpr(Identifier("AB")),
            segment2=SegmentExpr(Identifier("CD"))
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, Perpendicular)
        assert fact.parameters["line1"].point1.name == "A"
        assert fact.parameters["line2"].point1.name == "C"

    def test_build_on_constraint(self):
        """Test building On fact."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # AST: P on AB
        constraint = OnConstraint(
            point=Identifier("P"),
            object=Identifier("AB")
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, On)
        assert fact.parameters["point"].name == "P"
        assert fact.parameters["line"].point1.name == "A"
        assert fact.parameters["line"].point2.name == "B"

    def test_constraint_creates_implicit_objects(self):
        """Test that constraint building creates implicit objects."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # Build constraint without declaring points first
        constraint = EqualConstraint(
            left=SegmentExpr(Identifier("AB")),
            right=SegmentExpr(Identifier("CD"))
        )

        builder.build_constraint(constraint)

        # Points should be created implicitly
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert model.has_point("D")

        # But not declared
        assert "A" not in model.declared_points
        assert "B" not in model.declared_points

    def test_unsupported_constraint_raises_error(self):
        """Test that unsupported constraint raises error."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # Create a mock unsupported constraint
        class UnsupportedConstraint:
            pass

        with pytest.raises(ValueError) as exc_info:
            builder.build_constraint(UnsupportedConstraint())
        assert "Unsupported constraint type" in str(exc_info.value)


class TestProveGoalExtractor:
    """Test ProveGoalExtractor functionality."""

    def test_extract_equal_segments_goal(self):
        """Test extracting equal segments goal."""
        model = GeometryModel()
        extractor = ProveGoalExtractor(model)

        # AST: prove AB = CD
        prove_stmt = ProveStatement(
            goal=EqualConstraint(
                left=SegmentExpr(Identifier("AB")),
                right=SegmentExpr(Identifier("CD"))
            )
        )

        goal_fact = extractor.extract_goal(prove_stmt)

        assert isinstance(goal_fact, EqualSegment)
        assert goal_fact.parameters["segment1"].point1.name == "A"
        assert goal_fact.parameters["segment2"].point1.name == "C"

    def test_extract_equal_angles_goal(self):
        """Test extracting equal angles goal."""
        model = GeometryModel()
        extractor = ProveGoalExtractor(model)

        # AST: prove angle(ABC) = angle(DEF)
        prove_stmt = ProveStatement(
            goal=EqualConstraint(
                left=AngleExpr(Identifier("ABC")),
                right=AngleExpr(Identifier("DEF"))
            )
        )

        goal_fact = extractor.extract_goal(prove_stmt)

        assert isinstance(goal_fact, EqualAngle)

    def test_extract_parallel_goal(self):
        """Test extracting parallel goal."""
        model = GeometryModel()
        extractor = ProveGoalExtractor(model)

        # AST: prove AB || CD
        prove_stmt = ProveStatement(
            goal=ParallelConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            )
        )

        goal_fact = extractor.extract_goal(prove_stmt)

        assert isinstance(goal_fact, Parallel)

    def test_extract_perpendicular_goal(self):
        """Test extracting perpendicular goal."""
        model = GeometryModel()
        extractor = ProveGoalExtractor(model)

        # AST: prove AB ⊥ CD
        prove_stmt = ProveStatement(
            goal=PerpendicularConstraint(
                segment1=SegmentExpr(Identifier("AB")),
                segment2=SegmentExpr(Identifier("CD"))
            )
        )

        goal_fact = extractor.extract_goal(prove_stmt)

        assert isinstance(goal_fact, Perpendicular)

    def test_extract_multiple_goals(self):
        """Test extracting multiple goals."""
        model = GeometryModel()
        extractor = ProveGoalExtractor(model)

        prove_stmts = [
            ProveStatement(
                goal=EqualConstraint(
                    left=SegmentExpr(Identifier("AB")),
                    right=SegmentExpr(Identifier("CD"))
                )
            ),
            ProveStatement(
                goal=ParallelConstraint(
                    segment1=SegmentExpr(Identifier("EF")),
                    segment2=SegmentExpr(Identifier("GH"))
                )
            )
        ]

        goals = extractor.extract_goals(prove_stmts)

        assert len(goals) == 2
        assert isinstance(goals[0], EqualSegment)
        assert isinstance(goals[1], Parallel)


class TestIntegration:
    """Test integration of ConstraintBuilder with GeometryModel."""

    def test_isosceles_triangle_constraints(self):
        """Test building constraints for isosceles triangle."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # Declare points
        model.add_point("A")
        model.add_point("B")
        model.add_point("C")

        # Constraint: AB = AC
        constraint = EqualConstraint(
            left=SegmentExpr(Identifier("AB")),
            right=SegmentExpr(Identifier("AC"))
        )

        fact = builder.build_constraint(constraint)
        model.add_constraint(fact)

        # Verify
        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], EqualSegment)

    def test_parallel_lines_constraints(self):
        """Test building constraints for parallel lines."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # Constraint: AB || CD
        constraint = ParallelConstraint(
            segment1=SegmentExpr(Identifier("AB")),
            segment2=SegmentExpr(Identifier("CD"))
        )

        fact = builder.build_constraint(constraint)
        model.add_constraint(fact)

        # Verify
        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], Parallel)

        # Implicit points should be created
        assert len(model.points) == 4

    def test_right_triangle_constraint(self):
        """Test building right angle constraint."""
        model = GeometryModel()
        builder = ConstraintBuilder(model)

        # Constraint: angle(ABC) = 90
        constraint = EqualConstraint(
            left=AngleExpr(Identifier("ABC")),
            right=Number(90.0)
        )

        fact = builder.build_constraint(constraint)

        assert isinstance(fact, RightAngle)

    def test_full_problem_setup(self):
        """Test setting up a complete problem with constraints and goals."""
        model = GeometryModel()
        constraint_builder = ConstraintBuilder(model)
        goal_extractor = ProveGoalExtractor(model)

        # Points
        model.add_point("A")
        model.add_point("B")
        model.add_point("C")

        # Triangle
        model.add_triangle(
            model.get_point("A"),
            model.get_point("B"),
            model.get_point("C")
        )

        # Constraint: AB = AC
        constraint = EqualConstraint(
            left=SegmentExpr(Identifier("AB")),
            right=SegmentExpr(Identifier("AC"))
        )
        fact = constraint_builder.build_constraint(constraint)
        model.add_constraint(fact)

        # Goal: prove angle(ABC) = angle(ACB)
        prove_stmt = ProveStatement(
            goal=EqualConstraint(
                left=AngleExpr(Identifier("ABC")),
                right=AngleExpr(Identifier("ACB"))
            )
        )
        goal = goal_extractor.extract_goal(prove_stmt)
        model.add_prove_goal(goal)

        # Verify complete setup
        assert len(model.points) == 3
        assert len(model.triangles) == 1
        # Triangle creates AB, BC, CA; constraint creates AC separately = 4 segments
        assert len(model.segments) == 4
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1
        assert isinstance(model.constraints[0], EqualSegment)
        assert isinstance(model.prove_goals[0], EqualAngle)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
