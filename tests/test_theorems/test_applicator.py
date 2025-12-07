"""
Tests for theorem application.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 18 - Test theorem application
"""

import pytest
from geometry_prover.theorems.applicator import TheoremApplicator, TheoremApplication
from geometry_prover.theorems.auxiliary_constructor import AuxiliaryConstructor
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate, Pattern
from geometry_prover.facts.fact_types import (
    EqualSegment,
    EqualAngle,
    RightAngle,
    Collinear,
    Parallel,
)
from geometry_prover.utils.geometry_objects import Point, Segment, Angle


class TestTheoremApplicator:
    """Test TheoremApplicator class."""

    def test_apply_simple_theorem(self):
        """Test applying a simple theorem with transitivity."""
        # Build transitivity theorem:
        # If AB = CD, then CD = AB (symmetric property)
        theorem = (TheoremBuilder("transitivity")
                   .category("equality_properties")
                   .description("Equality is symmetric")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        # Create facts: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Apply theorem
        applicator = TheoremApplicator()
        result = applicator.apply(theorem, facts)

        # Should succeed
        assert result is not None
        assert isinstance(result, TheoremApplication)
        assert result.theorem == theorem

        # Check binding
        assert result.binding.get("?AB") == seg_ab
        assert result.binding.get("?CD") == seg_cd

        # Check derived facts
        assert len(result.derived_facts) == 1
        derived = result.derived_facts[0]
        assert isinstance(derived, EqualSegment)
        # CD = AB (reversed)
        assert derived.parameters["segment1"] == seg_cd
        assert derived.parameters["segment2"] == seg_ab

    def test_apply_fails_conditions_not_met(self):
        """Test that theorem fails to apply when conditions aren't met."""
        # Build theorem requiring equal segments
        theorem = (TheoremBuilder("test_theorem")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_variable(Variable("?ABC", "angle"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.right_angle("?ABC"))
                   .build())

        # Create facts without the required equal segments
        angle = Angle(Point("A"), Point("B"), Point("C"))
        facts = [RightAngle(angle)]

        # Apply theorem
        applicator = TheoremApplicator()
        result = applicator.apply(theorem, facts)

        # Should fail
        assert result is None

    def test_apply_theorem_multiple_conditions(self):
        """Test applying theorem with multiple conditions."""
        # Build theorem: If AB = CD and CD = EF, then AB = EF (transitivity)
        theorem = (TheoremBuilder("transitivity")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_variable(Variable("?EF", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_condition(PatternTemplate.equal_segment("?CD", "?EF"))
                   .add_conclusion(PatternTemplate.equal_segment("?AB", "?EF"))
                   .build())

        # Create facts satisfying both conditions
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Apply theorem
        applicator = TheoremApplicator()
        result = applicator.apply(theorem, facts)

        # Should succeed
        assert result is not None
        assert len(result.derived_facts) == 1
        derived = result.derived_facts[0]
        assert isinstance(derived, EqualSegment)
        assert derived.parameters["segment1"] == seg_ab
        assert derived.parameters["segment2"] == seg_ef

    def test_apply_theorem_multiple_conclusions(self):
        """Test applying theorem with multiple conclusions."""
        # Build theorem with two conclusions (symmetry and reflexivity)
        # If AB = CD, then CD = AB AND AB = AB
        theorem = (TheoremBuilder("test_theorem")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .add_conclusion(PatternTemplate.equal_segment("?AB", "?AB"))
                   .build())

        # Create facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Apply theorem
        applicator = TheoremApplicator()
        result = applicator.apply(theorem, facts)

        # Should succeed with two derived facts
        assert result is not None
        assert len(result.derived_facts) == 2
        assert all(isinstance(f, EqualSegment) for f in result.derived_facts)

    def test_apply_all_theorems(self):
        """Test applying multiple theorems to facts."""
        # Build two theorems with symmetry property
        theorem1 = (TheoremBuilder("theorem1")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        theorem2 = (TheoremBuilder("theorem2")
                    .add_variable(Variable("?EF", "segment"))
                    .add_variable(Variable("?GH", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?EF", "?GH"))
                    .add_conclusion(PatternTemplate.equal_segment("?GH", "?EF"))
                    .build())

        # Create facts that satisfy both theorems
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))
        seg_gh = Segment(Point("G"), Point("H"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_ef, seg_gh)
        ]

        # Apply all theorems
        applicator = TheoremApplicator()
        applications = applicator.apply_all([theorem1, theorem2], facts)

        # Both theorems should apply
        assert len(applications) == 2
        assert all(isinstance(app, TheoremApplication) for app in applications)
        assert applications[0].theorem.metadata.name == "theorem1"
        assert applications[1].theorem.metadata.name == "theorem2"

    def test_apply_all_some_fail(self):
        """Test apply_all when some theorems don't apply."""
        # Build three theorems with different conditions
        # Theorem 1: AB = CD => CD = AB
        theorem1 = (TheoremBuilder("theorem1")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        # Theorem 2: Requires angle equality (won't match our facts)
        theorem2 = (TheoremBuilder("theorem2")
                    .add_variable(Variable("?ABC", "angle"))
                    .add_variable(Variable("?DEF", "angle"))
                    .add_condition(PatternTemplate.equal_angle("?ABC", "?DEF"))
                    .add_conclusion(PatternTemplate.equal_angle("?DEF", "?ABC"))
                    .build())

        # Theorem 3: Requires right angle (won't match our facts)
        theorem3 = (TheoremBuilder("theorem3")
                    .add_variable(Variable("?X", "angle"))
                    .add_condition(PatternTemplate.right_angle("?X"))
                    .add_conclusion(PatternTemplate.right_angle("?X"))  # Identity
                    .build())

        # Create facts that only satisfy theorem1
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Apply all theorems
        applicator = TheoremApplicator()
        applications = applicator.apply_all([theorem1, theorem2, theorem3], facts)

        # Only theorem1 should apply
        assert len(applications) == 1
        assert applications[0].theorem.metadata.name == "theorem1"

    def test_auxiliary_constructor_rejects_degenerate_line(self):
        """Do not construct lines when both endpoints are the same point."""

        theorem = (
            TheoremBuilder("degenerate_line_guard")
            .category("auxiliary")
            .add_variable(Variable("?A", "point"))
            .add_variable(Variable("?B", "point"))
            .add_variable(Variable("?C", "point"))
            .add_variable(Variable("?AB", "line", derived_from=["?A", "?B"]))
            .add_condition(
                Pattern("Collinear", {"point1": "?A", "point2": "?B", "point3": "?C"})
            )
            .add_conclusion(PatternTemplate.parallel("?AB", "?AB"))
            .build()
        )

        facts = [Collinear(Point("C"), Point("C"), Point("D"))]

        applicator = TheoremApplicator()
        applicator.matcher.auxiliary_constructor = AuxiliaryConstructor()

        match_result = applicator.matcher.match_all_with_facts(theorem.conditions, facts, theorem)
        assert match_result is not None

        binding, _ = match_result
        assert binding.get("?AB") is None

        result = applicator.apply(theorem, facts)
        assert result is None

    def test_auxiliary_constructor_allows_valid_line(self):
        """Composite construction should work when endpoints differ."""

        theorem = (
            TheoremBuilder("non_degenerate_line_application")
            .category("auxiliary")
            .add_variable(Variable("?A", "point"))
            .add_variable(Variable("?B", "point"))
            .add_variable(Variable("?C", "point"))
            .add_variable(Variable("?AB", "line", derived_from=["?A", "?B"]))
            .add_condition(
                Pattern("Collinear", {"point1": "?A", "point2": "?B", "point3": "?C"})
            )
            .add_conclusion(PatternTemplate.parallel("?AB", "?AB"))
            .build()
        )

        facts = [Collinear(Point("A"), Point("B"), Point("C"))]

        applicator = TheoremApplicator()
        applicator.matcher.auxiliary_constructor = AuxiliaryConstructor()

        match_result = applicator.matcher.match_all_with_facts(theorem.conditions, facts, theorem)
        assert match_result is not None

        binding, _ = match_result
        assert binding.get("?AB") is not None

        result = applicator.apply(theorem, facts)
        assert result is not None
        assert any(isinstance(fact, Parallel) for fact in result.derived_facts)

    def test_theorem_application_repr(self):
        """Test TheoremApplication repr."""
        theorem = (TheoremBuilder("test")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        applicator = TheoremApplicator()
        result = applicator.apply(theorem, facts)

        repr_str = repr(result)
        assert "TheoremApplication" in repr_str
        assert "test" in repr_str
        assert "facts=" in repr_str


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
