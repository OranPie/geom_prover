"""
Geometric objects for the geometry prover system.

This module defines the basic geometric primitives:
- Point
- Line
- Circle
- Angle
- Segment
"""

from typing import Optional, Tuple
from enum import Enum


class LineType(Enum):
    """Types of lines."""

    LINE = "line"  # Infinite line
    SEGMENT = "segment"  # Line segment
    RAY = "ray"  # Ray (half-line)


class Point:
    """
    Represents a geometric point.

    Attributes:
        name: Identifier for the point (e.g., 'A', 'B', 'C')
        coords: Optional numeric coordinates (x, y)
        metadata: Additional information about the point
    """

    def __init__(
        self, name: str, coords: Optional[Tuple[float, float]] = None, metadata: Optional[dict] = None
    ):
        self.name = name
        self.coords = coords
        self.metadata = metadata or {}

    def __eq__(self, other) -> bool:
        """Points are equal if they have the same name."""
        if not isinstance(other, Point):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on name for use in sets and dicts."""
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if self.coords:
            return f"Point('{self.name}', coords={self.coords})"
        return f"Point('{self.name}')"


class Line:
    """
    Represents a line, segment, or ray.

    Attributes:
        id: Unique identifier for the line
        point1: First defining point
        point2: Second defining point
        equation: Optional line equation (a, b, c) for ax + by + c = 0
        line_type: Type of line (LINE, SEGMENT, RAY)
        metadata: Additional information
    """

    def __init__(
        self,
        point1: Point,
        point2: Point,
        line_type: LineType = LineType.LINE,
        equation: Optional[Tuple[float, float, float]] = None,
        line_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        self.point1 = point1
        self.point2 = point2
        self.line_type = line_type
        self.equation = equation
        self.id = line_id or f"{point1.name}{point2.name}"
        self.metadata = metadata or {}

    def contains_point(self, point: Point) -> bool:
        """Check if a point is on this line (requires coordinates)."""
        if self.equation and point.coords:
            a, b, c = self.equation
            x, y = point.coords
            return abs(a * x + b * y + c) < 1e-9
        # Without numeric info, cannot determine
        return False

    def is_parallel_to(self, other: "Line", tolerance: float = 1e-9) -> bool:
        """Check if this line is parallel to another (requires equations)."""
        if not self.equation or not other.equation:
            return False
        a1, b1, _ = self.equation
        a2, b2, _ = other.equation
        # Parallel if slopes are equal: a1/b1 == a2/b2 => a1*b2 == a2*b1
        return abs(a1 * b2 - a2 * b1) < tolerance

    def is_perpendicular_to(self, other: "Line", tolerance: float = 1e-9) -> bool:
        """Check if this line is perpendicular to another (requires equations)."""
        if not self.equation or not other.equation:
            return False
        a1, b1, _ = self.equation
        a2, b2, _ = other.equation
        # Perpendicular if a1*a2 + b1*b2 == 0
        return abs(a1 * a2 + b1 * b2) < tolerance

    def __eq__(self, other) -> bool:
        """Lines are equal if they have the same endpoints (order-independent)."""
        if not isinstance(other, Line):
            return False
        return (
            (self.point1 == other.point1 and self.point2 == other.point2)
            or (self.point1 == other.point2 and self.point2 == other.point1)
        ) and self.line_type == other.line_type

    def __hash__(self) -> int:
        """Hash based on sorted point names and line type."""
        points = tuple(sorted([self.point1.name, self.point2.name]))
        return hash((points, self.line_type))

    def __str__(self) -> str:
        if self.line_type == LineType.SEGMENT:
            return f"{self.point1.name}{self.point2.name}"
        elif self.line_type == LineType.LINE:
            return f"line({self.point1.name}{self.point2.name})"
        else:  # RAY
            return f"ray({self.point1.name}{self.point2.name})"

    def __repr__(self) -> str:
        return f"Line({self.point1.name}, {self.point2.name}, {self.line_type.value})"


class Segment(Line):
    """
    A line segment - convenience class wrapping Line with SEGMENT type.
    """

    def __init__(
        self,
        point1: Point,
        point2: Point,
        segment_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        super().__init__(
            point1, point2, LineType.SEGMENT, line_id=segment_id, metadata=metadata
        )


class Circle:
    """
    Represents a circle.

    Attributes:
        center: Center point of the circle
        radius: Radius (can be symbolic or numeric)
        id: Unique identifier
        metadata: Additional information
    """

    def __init__(
        self,
        center: Point,
        radius: float,
        circle_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):
        self.center = center
        self.radius = radius
        self.id = circle_id or f"circle_{center.name}"
        self.metadata = metadata or {}

    def contains_point(self, point: Point, tolerance: float = 1e-9) -> bool:
        """Check if a point is on this circle (requires coordinates)."""
        if not self.center.coords or not point.coords:
            return False
        cx, cy = self.center.coords
        px, py = point.coords
        distance_sq = (px - cx) ** 2 + (py - cy) ** 2
        return abs(distance_sq - self.radius**2) < tolerance

    def __eq__(self, other) -> bool:
        """Circles are equal if they have the same center and radius."""
        if not isinstance(other, Circle):
            return False
        return self.center == other.center and abs(self.radius - other.radius) < 1e-9

    def __hash__(self) -> int:
        return hash((self.center, round(self.radius, 6)))

    def __str__(self) -> str:
        return f"Circle({self.center.name}, r={self.radius})"

    def __repr__(self) -> str:
        return f"Circle(center={self.center.name}, radius={self.radius})"


class Angle:
    """
    Represents an angle defined by three points.

    The angle is at the vertex (middle point), formed by the rays
    from vertex to point1 and from vertex to point2.

    Attributes:
        vertex: The vertex point of the angle
        point1: First point defining a ray
        point2: Second point defining a ray
        metadata: Additional information
    """

    def __init__(
        self, point1: Point, vertex: Point, point2: Point, metadata: Optional[dict] = None
    ):
        self.point1 = point1
        self.vertex = vertex
        self.point2 = point2
        self.metadata = metadata or {}

    def to_radians(self) -> Optional[float]:
        """Calculate angle in radians (requires coordinates)."""
        if not all([self.point1.coords, self.vertex.coords, self.point2.coords]):
            return None

        import math

        vx, vy = self.vertex.coords
        p1x, p1y = self.point1.coords
        p2x, p2y = self.point2.coords

        # Vectors from vertex to point1 and point2
        v1 = (p1x - vx, p1y - vy)
        v2 = (p2x - vx, p2y - vy)

        # Angle using atan2
        angle1 = math.atan2(v1[1], v1[0])
        angle2 = math.atan2(v2[1], v2[0])

        angle = abs(angle2 - angle1)
        # Normalize to [0, 2π]
        if angle > math.pi:
            angle = 2 * math.pi - angle

        return angle

    def to_degrees(self) -> Optional[float]:
        """Calculate angle in degrees (requires coordinates)."""
        radians = self.to_radians()
        if radians is None:
            return None
        import math

        return math.degrees(radians)

    def equals(self, other: "Angle", tolerance: float = 1e-6) -> bool:
        """Check if two angles are equal (requires coordinates)."""
        angle1 = self.to_radians()
        angle2 = other.to_radians()
        if angle1 is None or angle2 is None:
            return False
        return abs(angle1 - angle2) < tolerance

    def __eq__(self, other) -> bool:
        """Angles are equal if they have the same three points."""
        if not isinstance(other, Angle):
            return False
        return (
            self.vertex == other.vertex
            and self.point1 == other.point1
            and self.point2 == other.point2
        )

    def __hash__(self) -> int:
        return hash((self.point1, self.vertex, self.point2))

    def __str__(self) -> str:
        return f"∠{self.point1.name}{self.vertex.name}{self.point2.name}"

    def __repr__(self) -> str:
        return f"Angle({self.point1.name}, {self.vertex.name}, {self.point2.name})"
