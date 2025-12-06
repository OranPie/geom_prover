"""
Tests for geometric objects (Point, Line, Circle, Angle, Segment).

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 1, Task 1.2 - Test Requirements:
- Unit tests for each class (minimum 80% coverage)
- Test equality and hashing
- Test edge cases (degenerate cases)
"""

import pytest
import math
from geometry_prover.utils import Point, Line, Circle, Angle, Segment, LineType


class TestPoint:
    """Tests for Point class."""

    def test_point_creation(self):
        """Test basic point creation."""
        p = Point("A")
        assert p.name == "A"
        assert p.coords is None
        assert p.metadata == {}

    def test_point_with_coords(self):
        """Test point creation with coordinates."""
        p = Point("B", coords=(1.0, 2.0))
        assert p.name == "B"
        assert p.coords == (1.0, 2.0)

    def test_point_equality(self):
        """Test point equality (based on name)."""
        p1 = Point("A")
        p2 = Point("A")
        p3 = Point("B")

        assert p1 == p2
        assert p1 != p3
        assert p1 != "A"  # Not equal to string

    def test_point_hash(self):
        """Test that points can be used in sets and dicts."""
        p1 = Point("A")
        p2 = Point("A")
        p3 = Point("B")

        point_set = {p1, p2, p3}
        assert len(point_set) == 2  # p1 and p2 are same

        point_dict = {p1: 1, p3: 2}
        assert point_dict[p2] == 1  # p2 same as p1

    def test_point_str_repr(self):
        """Test string representations."""
        p1 = Point("A")
        assert str(p1) == "A"
        assert repr(p1) == "Point('A')"

        p2 = Point("B", coords=(1.0, 2.0))
        assert str(p2) == "B"
        assert repr(p2) == "Point('B', coords=(1.0, 2.0))"


class TestLine:
    """Tests for Line class."""

    def test_line_creation(self):
        """Test basic line creation."""
        p1 = Point("A")
        p2 = Point("B")
        line = Line(p1, p2)

        assert line.point1 == p1
        assert line.point2 == p2
        assert line.line_type == LineType.LINE
        assert line.id == "AB"

    def test_segment_creation(self):
        """Test segment creation."""
        p1 = Point("A")
        p2 = Point("B")
        seg = Segment(p1, p2)

        assert seg.line_type == LineType.SEGMENT
        assert str(seg) == "AB"

    def test_line_equality(self):
        """Test line equality (order-independent)."""
        p1, p2, p3 = Point("A"), Point("B"), Point("C")

        line1 = Line(p1, p2)
        line2 = Line(p2, p1)  # Same line, reversed
        line3 = Line(p1, p3)  # Different line

        assert line1 == line2
        assert line1 != line3

    def test_line_hash(self):
        """Test that lines can be used in sets."""
        p1, p2, p3 = Point("A"), Point("B"), Point("C")

        line1 = Line(p1, p2)
        line2 = Line(p2, p1)
        line3 = Line(p1, p3)

        line_set = {line1, line2, line3}
        assert len(line_set) == 2  # line1 and line2 are same

    def test_line_contains_point(self):
        """Test point containment (requires coordinates)."""
        p1 = Point("A", coords=(0.0, 0.0))
        p2 = Point("B", coords=(1.0, 1.0))
        p3 = Point("C", coords=(0.5, 0.5))  # On line AB
        p4 = Point("D", coords=(0.5, 0.6))  # Not on line AB

        line = Line(p1, p2, equation=(-1.0, 1.0, 0.0))  # y = x => -x + y = 0

        assert line.contains_point(p3)
        assert not line.contains_point(p4)

    def test_parallel_lines(self):
        """Test parallel line detection."""
        # Two horizontal lines: y = 0 and y = 1
        line1 = Line(Point("A"), Point("B"), equation=(0.0, 1.0, 0.0))
        line2 = Line(Point("C"), Point("D"), equation=(0.0, 1.0, -1.0))

        assert line1.is_parallel_to(line2)

    def test_perpendicular_lines(self):
        """Test perpendicular line detection."""
        # Horizontal line y = 0 and vertical line x = 0
        line1 = Line(Point("A"), Point("B"), equation=(0.0, 1.0, 0.0))  # y = 0
        line2 = Line(Point("C"), Point("D"), equation=(1.0, 0.0, 0.0))  # x = 0

        assert line1.is_perpendicular_to(line2)


class TestCircle:
    """Tests for Circle class."""

    def test_circle_creation(self):
        """Test basic circle creation."""
        center = Point("O", coords=(0.0, 0.0))
        circle = Circle(center, radius=5.0)

        assert circle.center == center
        assert circle.radius == 5.0
        assert circle.id == "circle_O"

    def test_circle_contains_point(self):
        """Test point containment on circle."""
        center = Point("O", coords=(0.0, 0.0))
        circle = Circle(center, radius=1.0)

        p1 = Point("A", coords=(1.0, 0.0))  # On circle
        p2 = Point("B", coords=(0.0, 1.0))  # On circle
        p3 = Point("C", coords=(0.5, 0.5))  # Not on circle

        assert circle.contains_point(p1)
        assert circle.contains_point(p2)
        assert not circle.contains_point(p3)

    def test_circle_equality(self):
        """Test circle equality."""
        c1 = Point("O", coords=(0.0, 0.0))
        c2 = Point("O", coords=(0.0, 0.0))
        c3 = Point("P", coords=(1.0, 1.0))

        circle1 = Circle(c1, radius=5.0)
        circle2 = Circle(c2, radius=5.0)
        circle3 = Circle(c3, radius=5.0)
        circle4 = Circle(c1, radius=3.0)

        assert circle1 == circle2
        assert circle1 != circle3
        assert circle1 != circle4


class TestAngle:
    """Tests for Angle class."""

    def test_angle_creation(self):
        """Test basic angle creation."""
        p1 = Point("A")
        vertex = Point("B")
        p2 = Point("C")

        angle = Angle(p1, vertex, p2)

        assert angle.point1 == p1
        assert angle.vertex == vertex
        assert angle.point2 == p2

    def test_angle_calculation(self):
        """Test angle value calculation (requires coordinates)."""
        # Right angle: A at (0,1), B at origin, C at (1,0)
        p1 = Point("A", coords=(0.0, 1.0))
        vertex = Point("B", coords=(0.0, 0.0))
        p2 = Point("C", coords=(1.0, 0.0))

        angle = Angle(p1, vertex, p2)

        radians = angle.to_radians()
        degrees = angle.to_degrees()

        assert radians is not None
        assert abs(radians - math.pi / 2) < 1e-6  # 90 degrees
        assert abs(degrees - 90.0) < 1e-6

    def test_angle_without_coords(self):
        """Test angle calculation without coordinates."""
        p1 = Point("A")
        vertex = Point("B")
        p2 = Point("C")

        angle = Angle(p1, vertex, p2)

        assert angle.to_radians() is None
        assert angle.to_degrees() is None

    def test_angle_equality_symbolic(self):
        """Test symbolic angle equality (by points)."""
        p1, p2, p3 = Point("A"), Point("B"), Point("C")

        angle1 = Angle(p1, p2, p3)
        angle2 = Angle(p1, p2, p3)
        angle3 = Angle(p3, p2, p1)

        assert angle1 == angle2
        assert angle1 != angle3  # Different order

    def test_angle_equality_numeric(self):
        """Test numeric angle equality."""
        # Two 90-degree angles
        angle1 = Angle(
            Point("A", coords=(0.0, 1.0)),
            Point("B", coords=(0.0, 0.0)),
            Point("C", coords=(1.0, 0.0)),
        )

        angle2 = Angle(
            Point("D", coords=(0.0, 2.0)),
            Point("E", coords=(0.0, 0.0)),
            Point("F", coords=(2.0, 0.0)),
        )

        assert angle1.equals(angle2, tolerance=1e-6)

    def test_angle_str_repr(self):
        """Test string representations."""
        angle = Angle(Point("A"), Point("B"), Point("C"))

        assert str(angle) == "∠ABC"
        assert repr(angle) == "Angle(A, B, C)"


class TestEdgeCases:
    """Test edge cases and degenerate geometries."""

    def test_degenerate_line(self):
        """Test line with same start and end point."""
        p = Point("A", coords=(0.0, 0.0))
        line = Line(p, p)

        # Should be created but may behave unusually
        assert line.point1 == line.point2

    def test_zero_radius_circle(self):
        """Test circle with zero radius (degenerate to point)."""
        center = Point("O", coords=(0.0, 0.0))
        circle = Circle(center, radius=0.0)

        assert circle.radius == 0.0
        # Point at center should be "on" circle
        assert circle.contains_point(center)

    def test_zero_angle(self):
        """Test angle with collinear points."""
        # Three collinear points
        p1 = Point("A", coords=(0.0, 0.0))
        vertex = Point("B", coords=(1.0, 0.0))
        p2 = Point("C", coords=(2.0, 0.0))

        angle = Angle(p1, vertex, p2)
        radians = angle.to_radians()

        assert radians is not None
        assert abs(radians) < 1e-6 or abs(radians - math.pi) < 1e-6  # 0 or 180 degrees
