"""
End-to-End Semantic Analysis Integration Tests.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 3, Task 3.5 - Semantic Integration Testing
- Test complete DSL → AST → GeometryModel pipeline
- Test real geometry problems end-to-end
- Test performance and correctness
- Validate the complete semantic analysis system
"""

import pytest
from geometry_prover.dsl.parser import parse_program
from geometry_prover.semantic.fact_extractor import extract_facts
from geometry_prover.facts.fact_types import (
    EqualSegment, EqualAngle, Parallel, Perpendicular,
    RightAngle, On, OnCircle
)


class TestEndToEndPipeline:
    """Test complete DSL → Semantic Model pipeline."""

    def test_simple_triangle_problem(self):
        """Test simple triangle problem end-to-end."""
        dsl_code = """
        point A, B, C
        triangle ABC
        """

        # Parse DSL
        program = parse_program(dsl_code)
        assert program is not None

        # Extract semantic model
        model = extract_facts(program)

        # Verify model
        assert len(model.points) == 3
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert len(model.triangles) == 1
        assert len(model.segments) == 3  # AB, BC, CA

    def test_isosceles_triangle_theorem(self):
        """Test isosceles triangle base angles theorem."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify structure
        assert len(model.points) == 3
        assert len(model.triangles) == 1
        assert len(model.constraints) == 1
        assert len(model.prove_goals) == 1

        # Verify constraint: AB = AC
        assert isinstance(model.constraints[0], EqualSegment)
        seg1 = model.constraints[0].parameters["segment1"]
        seg2 = model.constraints[0].parameters["segment2"]
        assert seg1.point1.name == "A" and seg1.point2.name == "B"
        assert seg2.point1.name == "A" and seg2.point2.name == "C"

        # Verify goal: angle(ABC) = angle(ACB)
        assert isinstance(model.prove_goals[0], EqualAngle)
        angle1 = model.prove_goals[0].parameters["angle1"]
        angle2 = model.prove_goals[0].parameters["angle2"]
        assert angle1.vertex.name == "B"
        assert angle2.vertex.name == "C"

    def test_parallel_lines_transversal(self):
        """Test parallel lines with transversal problem."""
        dsl_code = """
        line AB
        line CD
        AB || CD
        line EF
        point G on AB
        point H on CD
        G on EF
        H on EF
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify lines
        assert len(model.lines) == 3
        assert model.has_line("AB")
        assert model.has_line("CD")
        assert model.has_line("EF")

        # Verify points
        assert model.has_point("G")
        assert model.has_point("H")

        # Verify parallel constraint
        assert len(model.constraints) >= 1
        parallel_constraints = [c for c in model.constraints if isinstance(c, Parallel)]
        assert len(parallel_constraints) >= 1

        # Verify on constraints (G on AB, H on CD, G on EF, H on EF = 4 total)
        on_constraints = [c for c in model.constraints if isinstance(c, On)]
        assert len(on_constraints) == 4

    def test_right_triangle_pythagorean_setup(self):
        """Test right triangle setup for Pythagorean theorem."""
        dsl_code = """
        point A, B, C
        triangle ABC
        angle(ABC) = 90
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify triangle
        assert len(model.triangles) == 1

        # Verify right angle constraint
        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], RightAngle)
        right_angle = model.constraints[0].parameters["angle"]
        assert right_angle.vertex.name == "B"

    def test_perpendicular_lines(self):
        """Test perpendicular lines problem."""
        dsl_code = """
        line AB
        line CD
        AB ⊥ CD
        prove angle(AOC) = 90
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify perpendicular constraint
        assert len(model.constraints) == 1
        assert isinstance(model.constraints[0], Perpendicular)

        # Verify prove goal
        assert len(model.prove_goals) == 1
        assert isinstance(model.prove_goals[0], RightAngle)

    def test_circle_problem(self):
        """Test circle-related problem with OnCircle constraint."""
        dsl_code = """
        point O
        circle O with radius 5
        point A, B, C
        A on circle O
        B on circle O
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify circle
        assert len(model.circles) == 1
        assert model.has_point("O")
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")

        # Verify OnCircle constraints
        on_circle_constraints = [c for c in model.constraints if isinstance(c, OnCircle)]
        assert len(on_circle_constraints) == 2  # A on circle O, B on circle O


class TestComplexProblems:
    """Test complex geometry problems."""

    def test_equilateral_triangle(self):
        """Test equilateral triangle setup."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = BC
        BC = CA
        prove AB = CA
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify constraints
        assert len(model.constraints) == 2
        assert all(isinstance(c, EqualSegment) for c in model.constraints)

        # Verify goal
        assert len(model.prove_goals) == 1
        assert isinstance(model.prove_goals[0], EqualSegment)

    def test_angle_bisector(self):
        """Test angle bisector problem."""
        dsl_code = """
        point A, B, C, D
        triangle ABC
        D on BC
        angle(ABD) = angle(DBC)
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify structure
        assert len(model.points) == 4
        assert len(model.triangles) == 1

        # Verify angle equality
        assert len(model.constraints) == 2  # angle equality + D on BC
        angle_constraints = [c for c in model.constraints if isinstance(c, EqualAngle)]
        assert len(angle_constraints) == 1

    def test_parallelogram_properties(self):
        """Test parallelogram properties."""
        dsl_code = """
        point A, B, C, D
        AB || CD
        AD || BC
        prove AC = AC
        """

        # Parse and extract
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Verify parallel constraints
        parallel_constraints = [c for c in model.constraints if isinstance(c, Parallel)]
        assert len(parallel_constraints) == 2

        # Verify goal (diagonal equality)
        assert len(model.prove_goals) == 1


class TestPerformance:
    """Test performance of semantic analysis."""

    def test_large_problem_performance(self):
        """Test semantic analysis on larger problem."""
        # Create a problem with many points and constraints
        dsl_code = """
        point A, B, C, D, E, F, G, H, I, J
        triangle ABC
        triangle DEF
        triangle GHI
        AB = DE
        BC = EF
        CA = FD
        AB || GH
        BC || HI
        CA || IG
        prove angle(ABC) = angle(DEF)
        """

        import time

        # Parse
        start = time.time()
        program = parse_program(dsl_code)
        parse_time = time.time() - start

        # Extract
        start = time.time()
        model = extract_facts(program)
        extract_time = time.time() - start

        # Verify model created successfully
        assert len(model.points) == 10
        assert len(model.triangles) == 3
        assert len(model.constraints) == 6  # 3 equal + 3 parallel
        assert len(model.prove_goals) == 1

        # Performance should be fast (sub-millisecond for this size)
        assert parse_time < 0.1  # 100ms
        assert extract_time < 0.1  # 100ms

    def test_repeated_extraction(self):
        """Test that multiple extractions work correctly."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        """

        program = parse_program(dsl_code)

        # Extract multiple times
        model1 = extract_facts(program)
        model2 = extract_facts(program)

        # Each extraction should create independent model
        assert len(model1.points) == 3
        assert len(model2.points) == 3
        assert model1 is not model2


class TestErrorHandling:
    """Test error handling in semantic analysis."""

    def test_well_formed_program(self):
        """Test that well-formed programs don't raise errors."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        # Should not raise any errors
        program = parse_program(dsl_code)
        model = extract_facts(program)

        assert model is not None
        assert len(model.points) == 3

    def test_implicit_object_creation(self):
        """Test that implicit object creation works correctly."""
        dsl_code = """
        AB = CD
        """

        # No explicit point declarations, but should create implicit points
        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Should create implicit points A, B, C, D
        assert len(model.points) == 4
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert model.has_point("D")

        # But none should be declared
        assert len(model.declared_points) == 0


class TestModelInspection:
    """Test GeometryModel inspection methods."""

    def test_model_summary(self):
        """Test model summary generation."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Get summary
        summary = model.summary()

        # Verify summary contains expected information
        assert "Points: 3" in summary
        assert "Triangles: 1" in summary
        assert "Constraints: 1" in summary
        assert "Prove Goals: 1" in summary

    def test_model_query_methods(self):
        """Test model query methods."""
        dsl_code = """
        point A, B, C
        line AB
        circle O with radius 5
        triangle ABC
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Test query methods
        all_points = model.get_all_points()
        assert len(all_points) >= 3

        all_lines = model.get_all_lines()
        assert len(all_lines) >= 1

        all_circles = model.get_all_circles()
        assert len(all_circles) == 1

        declared_points = model.get_declared_points()
        assert "A" in declared_points


class TestSemanticCornerCases:
    """Test corner cases in semantic analysis."""

    def test_empty_program(self):
        """Test empty program."""
        dsl_code = ""

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Should create empty model
        assert len(model.points) == 0
        assert len(model.constraints) == 0

    def test_only_declarations(self):
        """Test program with only declarations."""
        dsl_code = """
        point A, B, C
        line AB
        circle O with radius 5
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Should have objects but no constraints
        assert len(model.points) >= 3
        assert len(model.lines) >= 1
        assert len(model.circles) == 1
        assert len(model.constraints) == 0

    def test_only_constraints(self):
        """Test program with only constraints (implicit creation)."""
        dsl_code = """
        AB = CD
        EF || GH
        IJ ⊥ KL
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Should create all implicit objects
        assert len(model.points) == 12  # A,B,C,D,E,F,G,H,I,J,K,L
        assert len(model.constraints) == 3


class TestSemanticValidation:
    """Test validation of semantic correctness."""

    def test_consistent_object_reuse(self):
        """Test that objects are consistently reused."""
        dsl_code = """
        point A, B, C
        triangle ABC
        AB = AC
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # Point A should be the same object everywhere
        point_a = model.get_point("A")
        triangle_points = model.triangles["ABC"]
        assert point_a is triangle_points[0]

        # Segments AB and AC should reuse point A
        seg_ab = model.get_segment("AB")
        seg_ac = model.get_segment("AC")
        assert seg_ab.point1 is point_a
        assert seg_ac.point1 is point_a

    def test_declared_vs_implicit_tracking(self):
        """Test that declared vs implicit is tracked correctly."""
        dsl_code = """
        point A, B
        AB = CD
        """

        program = parse_program(dsl_code)
        model = extract_facts(program)

        # A and B are declared
        assert "A" in model.declared_points
        assert "B" in model.declared_points

        # C and D are implicit
        assert "C" not in model.declared_points
        assert "D" not in model.declared_points

        # But all exist in model
        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")
        assert model.has_point("D")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
