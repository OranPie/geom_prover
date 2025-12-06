"""
Tests for GeometryModel.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 3, Task 3.1 - Test Requirements:
- Test object registration (points, lines, circles)
- Test implicit object creation
- Test constraint tracking
- Test query methods
"""

import pytest
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.utils.geometry_objects import Point, Line, Circle, Segment, Angle, LineType
from geometry_prover.facts.fact_types import On


class TestPointManagement:
    """Test point management in GeometryModel."""

    def test_add_point(self):
        """Test adding a point."""
        model = GeometryModel()
        point = model.add_point("A")

        assert point.name == "A"
        assert model.has_point("A")
        assert model.get_point("A") == point

    def test_add_point_with_coords(self):
        """Test adding point with coordinates."""
        model = GeometryModel()
        point = model.add_point("A", (1.0, 2.0))

        assert point.coords == (1.0, 2.0)

    def test_add_duplicate_point(self):
        """Test adding duplicate point returns existing."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("A")

        assert p1 is p2
        assert len(model.points) == 1

    def test_add_point_with_conflicting_coords(self):
        """Test adding point with conflicting coordinates raises error."""
        model = GeometryModel()
        model.add_point("A", (1.0, 2.0))

        with pytest.raises(ValueError) as exc_info:
            model.add_point("A", (3.0, 4.0))
        assert "different coordinates" in str(exc_info.value)

    def test_get_or_create_point_existing(self):
        """Test get_or_create with existing point."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.get_or_create_point("A")

        assert p1 is p2

    def test_get_or_create_point_new(self):
        """Test get_or_create creates new point."""
        model = GeometryModel()
        point = model.get_or_create_point("A")

        assert point.name == "A"
        assert model.has_point("A")
        # Should be implicit (not declared)
        assert "A" not in model.declared_points

    def test_declared_vs_implicit_points(self):
        """Test tracking of declared vs implicit points."""
        model = GeometryModel()

        # Explicitly declared
        model.add_point("A", declared=True)
        # Implicitly created
        model.add_point("B", declared=False)

        assert "A" in model.declared_points
        assert "B" not in model.declared_points


class TestLineManagement:
    """Test line management in GeometryModel."""

    def test_add_line(self):
        """Test adding a line."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")

        line = model.add_line(p1, p2)

        assert line.point1 == p1
        assert line.point2 == p2
        assert model.has_line("AB")

    def test_add_line_with_name(self):
        """Test adding line with explicit name."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")

        line = model.add_line(p1, p2, name="line1")

        assert model.has_line("line1")
        assert model.get_line("line1") == line

    def test_add_duplicate_line(self):
        """Test adding duplicate line returns existing."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")

        l1 = model.add_line(p1, p2)
        l2 = model.add_line(p1, p2)

        assert l1 is l2
        assert len(model.lines) == 1

    def test_get_or_create_line(self):
        """Test get_or_create_line from point names."""
        model = GeometryModel()
        model.add_point("A")
        model.add_point("B")

        line = model.get_or_create_line("AB")

        assert line.point1.name == "A"
        assert line.point2.name == "B"

    def test_get_or_create_line_creates_points(self):
        """Test get_or_create_line creates implicit points."""
        model = GeometryModel()

        line = model.get_or_create_line("AB")

        # Points should be created implicitly
        assert model.has_point("A")
        assert model.has_point("B")
        assert "A" not in model.declared_points
        assert "B" not in model.declared_points


class TestSegmentManagement:
    """Test segment management in GeometryModel."""

    def test_add_segment(self):
        """Test adding a segment."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")

        segment = model.add_segment(p1, p2)

        assert segment.point1 == p1
        assert segment.point2 == p2
        assert model.get_segment("AB") == segment

    def test_get_or_create_segment(self):
        """Test get_or_create_segment."""
        model = GeometryModel()

        segment = model.get_or_create_segment("AB")

        assert segment.point1.name == "A"
        assert segment.point2.name == "B"


class TestCircleManagement:
    """Test circle management in GeometryModel."""

    def test_add_circle_with_radius(self):
        """Test adding circle with radius."""
        model = GeometryModel()
        center = model.add_point("O")

        circle = model.add_circle(center, radius=5.0)

        assert circle.center == center
        assert circle.radius == 5.0
        assert model.has_circle("O")

    def test_add_circle_through_point(self):
        """Test adding circle through point."""
        model = GeometryModel()
        center = model.add_point("O")
        point_on = model.add_point("A", (3.0, 4.0))

        # When center has no coords, can't calculate radius
        circle = model.add_circle(center, through_point=point_on)

        assert circle.center == center

    def test_get_circle(self):
        """Test getting circle by name."""
        model = GeometryModel()
        center = model.add_point("O")
        circle = model.add_circle(center, radius=10.0)

        retrieved = model.get_circle("O")
        assert retrieved == circle


class TestTriangleManagement:
    """Test triangle management in GeometryModel."""

    def test_add_triangle(self):
        """Test adding a triangle."""
        model = GeometryModel()
        a = model.add_point("A")
        b = model.add_point("B")
        c = model.add_point("C")

        triangle = model.add_triangle(a, b, c)

        assert triangle == (a, b, c)
        assert model.get_triangle("ABC") == triangle

    def test_triangle_creates_segments(self):
        """Test that triangle creates three side segments."""
        model = GeometryModel()
        a = model.add_point("A")
        b = model.add_point("B")
        c = model.add_point("C")

        model.add_triangle(a, b, c)

        # Three segments should be created
        assert model.get_segment("AB") is not None
        assert model.get_segment("BC") is not None
        assert model.get_segment("CA") is not None


class TestAngleManagement:
    """Test angle management in GeometryModel."""

    def test_add_angle(self):
        """Test adding an angle."""
        model = GeometryModel()
        a = model.add_point("A")
        b = model.add_point("B")
        c = model.add_point("C")

        angle = model.add_angle(a, b, c)

        assert angle.point1 == a
        assert angle.vertex == b
        assert angle.point2 == c
        assert model.get_angle("ABC") == angle

    def test_get_or_create_angle(self):
        """Test get_or_create_angle."""
        model = GeometryModel()

        angle = model.get_or_create_angle("ABC")

        assert angle.point1.name == "A"
        assert angle.vertex.name == "B"
        assert angle.point2.name == "C"


class TestConstraintTracking:
    """Test constraint and goal tracking."""

    def test_add_constraint(self):
        """Test adding constraints."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")
        line = model.add_line(p1, p2)

        # Create a constraint fact
        fact = On(p1, line)
        model.add_constraint(fact)

        assert len(model.constraints) == 1
        assert model.constraints[0] == fact

    def test_add_prove_goal(self):
        """Test adding prove goals."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")
        line = model.add_line(p1, p2)

        # Create a goal fact
        fact = On(p1, line)
        model.add_prove_goal(fact)

        assert len(model.prove_goals) == 1
        assert model.prove_goals[0] == fact


class TestQueryMethods:
    """Test query methods."""

    def test_get_all_points(self):
        """Test getting all points."""
        model = GeometryModel()
        model.add_point("A")
        model.add_point("B")
        model.add_point("C")

        points = model.get_all_points()
        assert len(points) == 3
        assert all(isinstance(p, Point) for p in points)

    def test_get_all_lines(self):
        """Test getting all lines."""
        model = GeometryModel()
        p1 = model.add_point("A")
        p2 = model.add_point("B")
        model.add_line(p1, p2)

        lines = model.get_all_lines()
        assert len(lines) == 1

    def test_get_all_circles(self):
        """Test getting all circles."""
        model = GeometryModel()
        center = model.add_point("O")
        model.add_circle(center, radius=5.0)

        circles = model.get_all_circles()
        assert len(circles) == 1

    def test_get_declared_points(self):
        """Test getting declared points."""
        model = GeometryModel()
        model.add_point("A", declared=True)
        model.add_point("B", declared=False)

        declared = model.get_declared_points()
        assert "A" in declared
        assert "B" not in declared


class TestModelSummary:
    """Test model summary and representation."""

    def test_summary(self):
        """Test summary generation."""
        model = GeometryModel()
        model.add_point("A")
        model.add_point("B")
        p1 = model.get_point("A")
        p2 = model.get_point("B")
        model.add_line(p1, p2)

        summary = model.summary()

        assert "Points: 2" in summary
        assert "Lines: 1" in summary

    def test_repr(self):
        """Test __repr__ method."""
        model = GeometryModel()
        model.add_point("A")

        repr_str = repr(model)
        assert "GeometryModel" in repr_str
        assert "Points: 1" in repr_str


class TestComplexScenarios:
    """Test complex geometry scenarios."""

    def test_isosceles_triangle_setup(self):
        """Test setting up an isosceles triangle."""
        model = GeometryModel()

        # Points
        a = model.add_point("A")
        b = model.add_point("B")
        c = model.add_point("C")

        # Triangle
        model.add_triangle(a, b, c)

        # Should have 3 points, 3 segments
        assert len(model.points) == 3
        assert len(model.segments) == 3
        assert len(model.triangles) == 1

    def test_circle_with_points(self):
        """Test circle with multiple points on it."""
        model = GeometryModel()

        center = model.add_point("O")
        circle = model.add_circle(center, radius=5.0)

        a = model.add_point("A")
        b = model.add_point("B")
        c = model.add_point("C")

        # Note: For point-on-circle, we would need a different fact type
        # For now, just test that we can track the points and circle
        assert len(model.points) == 4  # O, A, B, C
        assert len(model.circles) == 1

    def test_parallel_lines_setup(self):
        """Test setting up parallel lines."""
        model = GeometryModel()

        # Line 1
        a = model.add_point("A")
        b = model.add_point("B")
        line1 = model.add_line(a, b, name="AB")

        # Line 2
        c = model.add_point("C")
        d = model.add_point("D")
        line2 = model.add_line(c, d, name="CD")

        assert len(model.lines) == 2
        assert len(model.points) == 4


class TestImplicitCreation:
    """Test implicit object creation."""

    def test_implicit_points_from_line(self):
        """Test that line creation can create implicit points."""
        model = GeometryModel()

        # Create line without declaring points first
        line = model.get_or_create_line("AB")

        # Points should exist but not be declared
        assert model.has_point("A")
        assert model.has_point("B")
        assert "A" not in model.declared_points
        assert "B" not in model.declared_points

    def test_implicit_points_from_segment(self):
        """Test segment creation creates implicit points."""
        model = GeometryModel()

        segment = model.get_or_create_segment("CD")

        assert model.has_point("C")
        assert model.has_point("D")

    def test_implicit_points_from_angle(self):
        """Test angle creation creates implicit points."""
        model = GeometryModel()

        angle = model.get_or_create_angle("ABC")

        assert model.has_point("A")
        assert model.has_point("B")
        assert model.has_point("C")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
