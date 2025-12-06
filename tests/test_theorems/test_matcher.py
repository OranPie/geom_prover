"""
Tests for pattern matching and unification.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 18 - Test pattern matching and unification
"""

import pytest
from geometry_prover.theorems.matcher import Binding, PatternMatcher, Unifier
from geometry_prover.theorems.pattern import Pattern, Variable, PatternTemplate
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle, RightAngle, On
from geometry_prover.utils.geometry_objects import Point, Segment, Angle, Line


class TestBinding:
    """Test Binding class."""

    def test_create_empty_binding(self):
        """Test creating empty binding."""
        binding = Binding()
        assert len(binding.bindings) == 0

    def test_create_binding_with_initial_values(self):
        """Test creating binding with initial values."""
        point_a = Point("A")
        binding = Binding({"?A": point_a})

        assert binding.get("?A") == point_a
        assert binding.is_bound("?A")

    def test_bind_variable(self):
        """Test binding a variable."""
        binding = Binding()
        point_a = Point("A")

        result = binding.bind("?A", point_a)

        assert result is True
        assert binding.get("?A") == point_a
        assert binding.is_bound("?A")

    def test_bind_same_variable_consistent(self):
        """Test binding same variable to same value is consistent."""
        binding = Binding()
        point_a = Point("A")

        binding.bind("?A", point_a)
        result = binding.bind("?A", point_a)

        assert result is True

    def test_bind_same_variable_inconsistent(self):
        """Test binding same variable to different value fails."""
        binding = Binding()
        point_a = Point("A")
        point_b = Point("B")

        binding.bind("?A", point_a)
        result = binding.bind("?A", point_b)

        assert result is False

    def test_get_unbound_variable(self):
        """Test getting unbound variable returns None."""
        binding = Binding()
        assert binding.get("?X") is None
        assert not binding.is_bound("?X")

    def test_binding_copy(self):
        """Test copying binding."""
        point_a = Point("A")
        binding1 = Binding({"?A": point_a})
        binding2 = binding1.copy()

        # Modify binding2
        point_b = Point("B")
        binding2.bind("?B", point_b)

        # binding1 should be unchanged
        assert binding1.is_bound("?A")
        assert not binding1.is_bound("?B")
        assert binding2.is_bound("?A")
        assert binding2.is_bound("?B")

    def test_binding_repr(self):
        """Test binding string representation."""
        point_a = Point("A")
        binding = Binding({"?A": point_a})
        repr_str = repr(binding)

        assert "Binding" in repr_str
        assert "?A" in repr_str


class TestPatternMatcher:
    """Test PatternMatcher class."""

    def test_match_equal_segment_pattern(self):
        """Test matching EqualSegment pattern."""
        # Create fact
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        # Create pattern
        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        # Match
        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        assert binding is not None
        assert binding.get("?AB") == seg_ab
        assert binding.get("?CD") == seg_cd

    def test_match_equal_angle_pattern(self):
        """Test matching EqualAngle pattern."""
        # Create fact
        angle1 = Angle(Point("A"), Point("B"), Point("C"))
        angle2 = Angle(Point("D"), Point("E"), Point("F"))
        fact = EqualAngle(angle1, angle2)

        # Create pattern with Variable instances
        var1 = Variable("?ABC", "angle")
        var2 = Variable("?DEF", "angle")
        pattern = Pattern("EqualAngle", {
            "angle1": var1,
            "angle2": var2
        })

        # Match
        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        assert binding is not None
        assert binding.get("?ABC") == angle1
        assert binding.get("?DEF") == angle2

    def test_match_right_angle_pattern(self):
        """Test matching RightAngle pattern."""
        angle = Angle(Point("A"), Point("B"), Point("C"))
        fact = RightAngle(angle)

        pattern = PatternTemplate.right_angle("?ABC")

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        assert binding is not None
        assert binding.get("?ABC") == angle

    def test_match_on_pattern(self):
        """Test matching On (point on line) pattern."""
        point = Point("P")
        line = Line(Point("A"), Point("B"))
        fact = On(point, line)

        pattern = PatternTemplate.on_point("?P", "?AB")

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        assert binding is not None
        assert binding.get("?P") == point
        assert binding.get("?AB") == line

    def test_match_fails_wrong_fact_type(self):
        """Test that matching fails for wrong fact type."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        # Try to match with EqualAngle pattern
        pattern = PatternTemplate.equal_angle("?ABC", "?DEF")

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        assert binding is None

    def test_match_with_existing_binding(self):
        """Test matching with existing binding."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        # Create existing binding
        existing_binding = Binding({"?AB": seg_ab})

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact, existing_binding)

        assert binding is not None
        assert binding.get("?AB") == seg_ab
        assert binding.get("?CD") == seg_cd

    def test_match_fails_inconsistent_binding(self):
        """Test that matching fails with inconsistent existing binding."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))
        fact = EqualSegment(seg_ab, seg_cd)

        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        # Create existing binding with conflicting value for ?AB
        existing_binding = Binding({"?AB": seg_ef})

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact, existing_binding)

        assert binding is None

    def test_match_all_patterns(self):
        """Test matching multiple patterns with consistent bindings."""
        # Create facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        angle1 = Angle(Point("A"), Point("B"), Point("C"))
        angle2 = Angle(Point("D"), Point("E"), Point("F"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualAngle(angle1, angle2)
        ]

        # Create patterns
        patterns = [
            PatternTemplate.equal_segment("?AB", "?CD"),
            PatternTemplate.equal_angle("?ABC", "?DEF")
        ]

        matcher = PatternMatcher()
        binding = matcher.match_all(patterns, facts)

        assert binding is not None
        assert binding.get("?AB") == seg_ab
        assert binding.get("?CD") == seg_cd
        assert binding.get("?ABC") == angle1
        assert binding.get("?DEF") == angle2

    def test_match_all_fails_missing_fact(self):
        """Test that match_all fails if any pattern doesn't match."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        facts = [
            EqualSegment(seg_ab, seg_cd)
        ]

        # Two patterns but only one fact
        patterns = [
            PatternTemplate.equal_segment("?AB", "?CD"),
            PatternTemplate.equal_angle("?ABC", "?DEF")  # Won't match
        ]

        matcher = PatternMatcher()
        binding = matcher.match_all(patterns, facts)

        assert binding is None


class TestUnifier:
    """Test Unifier class."""

    def test_substitute_variables(self):
        """Test substituting variables in pattern."""
        # Create pattern with variables
        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        # Create binding
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        binding = Binding({
            "?AB": seg_ab,
            "?CD": seg_cd
        })

        # Substitute
        unifier = Unifier()
        new_pattern = unifier.substitute(pattern, binding)

        assert new_pattern.parameters["segment1"] == seg_ab
        assert new_pattern.parameters["segment2"] == seg_cd

    def test_substitute_with_variable_objects(self):
        """Test substituting Variable instances."""
        var1 = Variable("?AB", "segment")
        var2 = Variable("?CD", "segment")

        pattern = Pattern("EqualSegment", {
            "segment1": var1,
            "segment2": var2
        })

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        binding = Binding({
            "?AB": seg_ab,
            "?CD": seg_cd
        })

        unifier = Unifier()
        new_pattern = unifier.substitute(pattern, binding)

        assert new_pattern.parameters["segment1"] == seg_ab
        assert new_pattern.parameters["segment2"] == seg_cd

    def test_substitute_partial_binding(self):
        """Test substitution with partial binding."""
        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        # Only bind one variable
        seg_ab = Segment(Point("A"), Point("B"))
        binding = Binding({"?AB": seg_ab})

        unifier = Unifier()
        new_pattern = unifier.substitute(pattern, binding)

        assert new_pattern.parameters["segment1"] == seg_ab
        assert new_pattern.parameters["segment2"] == "?CD"  # Unbound

    def test_is_ground_true(self):
        """Test is_ground with ground pattern (no variables)."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        pattern = Pattern("EqualSegment", {
            "segment1": seg_ab,
            "segment2": seg_cd
        })

        unifier = Unifier()
        assert unifier.is_ground(pattern) is True

    def test_is_ground_false_with_variables(self):
        """Test is_ground with pattern containing variables."""
        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        unifier = Unifier()
        assert unifier.is_ground(pattern) is False

    def test_is_ground_false_with_variable_objects(self):
        """Test is_ground with Variable instances."""
        var1 = Variable("?AB", "segment")

        pattern = Pattern("EqualSegment", {
            "segment1": var1,
            "segment2": "CD"
        })

        unifier = Unifier()
        assert unifier.is_ground(pattern) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
