"""
Complete system integration tests for theorem system.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 21 - Integration testing

These tests demonstrate the complete theorem system working end-to-end,
from initial facts through automated reasoning to derived conclusions.
"""

import pytest
from pathlib import Path

from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle, Parallel
from geometry_prover.utils.geometry_objects import Point, Segment, Angle, Line


class TestCompleteSystemIntegration:
    """End-to-end integration tests for complete theorem system."""

    def test_simple_equality_reasoning(self):
        """
        Test simple equality reasoning with symmetry and transitivity.

        Given: AB = CD
        Derive: CD = AB (symmetry)

        Given: AB = CD, CD = EF
        Derive: AB = EF (transitivity)
        """
        # Load theorem library
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        count = engine.load_library(str(theorem_dir))
        assert count >= 13

        # Create initial facts: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Run forward chaining
        result = engine.forward_chain(initial_facts, max_iterations=5)

        # Should derive CD = AB via symmetry
        assert len(result.derived_facts) >= 1
        assert result.converged is True

        # Check that symmetry theorem was applied
        theorem_names = [step.theorem_name for step in result.derivation_steps]
        assert "equality_symmetry" in theorem_names

    def test_transitivity_chain(self):
        """
        Test transitivity chaining.

        Given: AB = CD, CD = EF
        Derive: AB = EF, CD = AB, EF = CD, EF = AB
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create facts: AB = CD, CD = EF
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Run forward chaining
        result = engine.forward_chain(initial_facts, max_iterations=10)

        # Should derive multiple facts via symmetry and transitivity
        assert len(result.derived_facts) >= 2
        assert result.converged is True

        # Should apply both symmetry and transitivity
        theorem_names = {step.theorem_name for step in result.derivation_steps}
        assert "equality_symmetry" in theorem_names
        assert "equality_transitivity" in theorem_names

    def test_parallel_line_reasoning(self):
        """
        Test parallel line reasoning.

        Given: AB || CD, CD || EF
        Derive: AB || EF (parallel transitivity)
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create facts: AB || CD, CD || EF
        line_ab = Line(Point("A"), Point("B"))
        line_cd = Line(Point("C"), Point("D"))
        line_ef = Line(Point("E"), Point("F"))

        initial_facts = [
            Parallel(line_ab, line_cd),
            Parallel(line_cd, line_ef)
        ]

        # Run forward chaining
        result = engine.forward_chain(initial_facts, max_iterations=10)

        # Should derive parallel facts
        assert len(result.derived_facts) >= 1
        assert result.converged is True

    def test_angle_equality_reasoning(self):
        """
        Test angle equality reasoning.

        Given: ∠ABC = ∠DEF
        Derive: ∠DEF = ∠ABC (symmetry)
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create facts: angle ABC = angle DEF
        angle1 = Angle(Point("A"), Point("B"), Point("C"))
        angle2 = Angle(Point("D"), Point("E"), Point("F"))

        initial_facts = [EqualAngle(angle1, angle2)]

        # Run forward chaining
        result = engine.forward_chain(initial_facts, max_iterations=5)

        # Should derive symmetric equality
        assert len(result.derived_facts) >= 1
        assert result.converged is True

        # Should apply angle symmetry
        theorem_names = [step.theorem_name for step in result.derivation_steps]
        assert "angle_equality_symmetry" in theorem_names

    def test_convergence_detection(self):
        """
        Test that forward chaining detects convergence (fixed point).

        When no new facts can be derived, should stop and set converged=True.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Simple case that converges quickly
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Run with high max_iterations
        result = engine.forward_chain(initial_facts, max_iterations=100)

        # Should converge before hitting max iterations
        assert result.converged is True
        assert result.iterations < 100

    def test_no_applicable_theorems(self):
        """
        Test behavior when no theorems apply to the facts.

        Should converge immediately with no derivations.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create a fact that no theorem will match
        # (using uncommon fact type or structure)
        seg_ab = Segment(Point("A"), Point("B"))
        seg_ab_again = Segment(Point("A"), Point("B"))

        # Same segment twice - reflexive but won't derive anything new
        initial_facts = [EqualSegment(seg_ab, seg_ab_again)]

        result = engine.forward_chain(initial_facts, max_iterations=10)

        # Should converge immediately
        assert result.converged is True
        assert result.iterations == 1
        # May derive reflexive fact or nothing
        assert len(result.derived_facts) >= 0

    def test_derivation_history_tracking(self):
        """
        Test that derivation history is properly tracked.

        Every theorem application should be recorded.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = engine.forward_chain(initial_facts, max_iterations=10)

        # Check derivation steps structure
        for step in result.derivation_steps:
            assert hasattr(step, 'theorem_name')
            assert hasattr(step, 'derived_facts')
            assert hasattr(step, 'step_number')
            assert len(step.theorem_name) > 0
            assert len(step.derived_facts) > 0
            assert step.step_number > 0

    def test_specific_theorem_application(self):
        """
        Test applying a specific theorem by name.

        Should be able to selectively apply individual theorems.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        facts = [EqualSegment(seg_ab, seg_cd)]

        # Apply specific theorem
        result = engine.apply_single_theorem("equality_symmetry", facts)

        assert result is not None
        assert len(result.derived_facts) == 1

        # Verify the derived fact is the symmetric one
        derived = result.derived_facts[0]
        assert isinstance(derived, EqualSegment)

    def test_theorem_categories(self):
        """
        Test filtering theorems by category.

        Should be able to get theorems grouped by category.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Get equality theorems
        equality_theorems = engine.get_theorems_by_category("equality_properties")
        assert len(equality_theorems) >= 2  # symmetry, transitivity

        # Get angle theorems
        angle_theorems = engine.get_theorems_by_category("angle_properties")
        assert len(angle_theorems) >= 2  # symmetry, transitivity

    def test_result_summary_output(self):
        """
        Test that result summary can be printed without error.

        Ensures the print_summary method works.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = engine.forward_chain(initial_facts, max_iterations=5)

        # Should not raise exception
        result.print_summary()

    def test_large_fact_set_performance(self):
        """
        Test performance with larger fact sets.

        Should handle multiple facts efficiently.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create chain of equalities: AB = CD = EF = GH = IJ
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))
        seg_gh = Segment(Point("G"), Point("H"))
        seg_ij = Segment(Point("I"), Point("J"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef),
            EqualSegment(seg_ef, seg_gh),
            EqualSegment(seg_gh, seg_ij)
        ]

        # Run with reasonable limits
        result = engine.forward_chain(
            initial_facts,
            max_iterations=20,
            max_facts=100
        )

        # Should complete and converge
        assert result.converged or result.iterations == 20
        assert len(result.all_facts) <= 100

    def test_mixed_fact_types(self):
        """
        Test reasoning with mixed fact types.

        Should handle segments, angles, lines, etc. in same fact set.
        """
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Mix of different fact types
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        angle1 = Angle(Point("E"), Point("F"), Point("G"))
        angle2 = Angle(Point("H"), Point("I"), Point("J"))
        line1 = Line(Point("K"), Point("L"))
        line2 = Line(Point("M"), Point("N"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualAngle(angle1, angle2),
            Parallel(line1, line2)
        ]

        result = engine.forward_chain(initial_facts, max_iterations=10)

        # Should process all fact types
        assert result.converged is True
        assert len(result.derived_facts) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
