"""
Tests for Pattern and Variable classes.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 17 - Test pattern matching data structures
"""

import pytest
from geometry_prover.theorems.pattern import Variable, Pattern, PatternTemplate


class TestVariable:
    """Test Variable class."""

    def test_create_point_variable(self):
        """Test creating a point variable."""
        var = Variable(name="?A", type="point", description="A point")
        assert var.name == "?A"
        assert var.type == "point"
        assert var.description == "A point"

    def test_create_segment_variable(self):
        """Test creating a segment variable."""
        var = Variable(name="?AB", type="segment")
        assert var.name == "?AB"
        assert var.type == "segment"

    def test_variable_must_start_with_question_mark(self):
        """Test that variable names must start with ?."""
        with pytest.raises(ValueError, match="must start with"):
            Variable(name="A", type="point")

    def test_invalid_variable_type(self):
        """Test that invalid variable types are rejected."""
        with pytest.raises(ValueError, match="Invalid variable type"):
            Variable(name="?X", type="invalid_type")

    def test_valid_variable_types(self):
        """Test all valid variable types."""
        valid_types = ["point", "segment", "angle", "line", "circle", "triangle", "any"]
        for vtype in valid_types:
            var = Variable(name="?X", type=vtype)
            assert var.type == vtype

    def test_variable_equality(self):
        """Test variable equality."""
        var1 = Variable(name="?A", type="point")
        var2 = Variable(name="?A", type="point")
        var3 = Variable(name="?B", type="point")

        assert var1 == var2
        assert var1 != var3

    def test_variable_hashable(self):
        """Test that variables are hashable."""
        var1 = Variable(name="?A", type="point")
        var2 = Variable(name="?B", type="point")

        # Should be able to use in set
        var_set = {var1, var2, var1}
        assert len(var_set) == 2


class TestPattern:
    """Test Pattern class."""

    def test_create_simple_pattern(self):
        """Test creating a simple pattern."""
        pattern = Pattern("EqualSegment", {
            "segment1": "?AB",
            "segment2": "?CD"
        })

        assert pattern.fact_type == "EqualSegment"
        assert pattern.parameters["segment1"] == "?AB"
        assert pattern.parameters["segment2"] == "?CD"

    def test_pattern_with_variable_objects(self):
        """Test pattern with Variable instances."""
        var_a = Variable("?A", "point")
        var_b = Variable("?B", "point")

        pattern = Pattern("On", {
            "point": var_a,
            "line": var_b
        })

        assert pattern.parameters["point"] == var_a
        assert pattern.parameters["line"] == var_b

    def test_get_variables(self):
        """Test extracting variables from pattern."""
        var_ab = Variable("?AB", "segment")
        var_cd = Variable("?CD", "segment")

        pattern = Pattern("EqualSegment", {
            "segment1": var_ab,
            "segment2": var_cd
        })

        variables = pattern.get_variables()
        assert len(variables) == 2
        assert var_ab in variables
        assert var_cd in variables

    def test_has_variables(self):
        """Test checking if pattern has variables."""
        var = Variable("?A", "point")

        pattern1 = Pattern("On", {"point": var, "line": "AB"})
        assert pattern1.has_variables() is True

        pattern2 = Pattern("On", {"point": "A", "line": "AB"})
        assert pattern2.has_variables() is False

    def test_pattern_equality(self):
        """Test pattern equality."""
        pattern1 = Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?CD"})
        pattern2 = Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?CD"})
        pattern3 = Pattern("EqualSegment", {"segment1": "?EF", "segment2": "?GH"})

        assert pattern1 == pattern2
        assert pattern1 != pattern3

    def test_pattern_hashable(self):
        """Test that patterns are hashable."""
        pattern1 = Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?CD"})
        pattern2 = Pattern("EqualAngle", {"angle1": "?ABC", "angle2": "?DEF"})

        pattern_set = {pattern1, pattern2, pattern1}
        assert len(pattern_set) == 2

    def test_pattern_repr(self):
        """Test pattern string representation."""
        pattern = Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?CD"})
        repr_str = repr(pattern)

        assert "Pattern" in repr_str
        assert "EqualSegment" in repr_str


class TestPatternTemplate:
    """Test PatternTemplate convenience constructors."""

    def test_equal_segment_template(self):
        """Test EqualSegment pattern template."""
        pattern = PatternTemplate.equal_segment("?AB", "?CD")

        assert pattern.fact_type == "EqualSegment"
        assert pattern.parameters["segment1"] == "?AB"
        assert pattern.parameters["segment2"] == "?CD"

    def test_equal_angle_template(self):
        """Test EqualAngle pattern template."""
        pattern = PatternTemplate.equal_angle("?ABC", "?DEF")

        assert pattern.fact_type == "EqualAngle"
        assert pattern.parameters["angle1"] == "?ABC"
        assert pattern.parameters["angle2"] == "?DEF"

    def test_right_angle_template(self):
        """Test RightAngle pattern template."""
        pattern = PatternTemplate.right_angle("?ABC")

        assert pattern.fact_type == "RightAngle"
        assert pattern.parameters["angle"] == "?ABC"

    def test_parallel_template(self):
        """Test Parallel pattern template."""
        pattern = PatternTemplate.parallel("?AB", "?CD")

        assert pattern.fact_type == "Parallel"
        assert pattern.parameters["line1"] == "?AB"
        assert pattern.parameters["line2"] == "?CD"

    def test_perpendicular_template(self):
        """Test Perpendicular pattern template."""
        pattern = PatternTemplate.perpendicular("?AB", "?CD")

        assert pattern.fact_type == "Perpendicular"
        assert pattern.parameters["line1"] == "?AB"
        assert pattern.parameters["line2"] == "?CD"

    def test_on_point_template(self):
        """Test On (point on line) pattern template."""
        pattern = PatternTemplate.on_point("?P", "?AB")

        assert pattern.fact_type == "On"
        assert pattern.parameters["point"] == "?P"
        assert pattern.parameters["line"] == "?AB"

    def test_on_circle_template(self):
        """Test OnCircle pattern template."""
        pattern = PatternTemplate.on_circle("?P", "?O")

        assert pattern.fact_type == "OnCircle"
        assert pattern.parameters["point"] == "?P"
        assert pattern.parameters["circle"] == "?O"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
