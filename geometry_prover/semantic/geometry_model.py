"""
GeometryModel - In-memory representation of geometric configuration.

The GeometryModel maintains the geometric objects (points, lines, circles, etc.)
created during semantic analysis of a DSL program. It provides methods to
register objects, look them up, and track relationships.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 3, Task 3.1 - GeometryModel Implementation
- Maintain geometric objects (points, lines, circles)
- Object lookup and registration
- Constraint tracking
- Support for implicit object creation
"""

from typing import Dict, List, Optional, Set, Tuple
from geometry_prover.utils.geometry_objects import (
    Point, Line, Circle, Angle, Segment, LineType
)
from geometry_prover.facts.fact_types import Fact


class GeometryModel:
    """
    In-memory representation of geometric configuration.

    Stores all geometric objects created from a DSL program and tracks
    relationships between them.
    """

    def __init__(self):
        """Initialize empty geometry model."""
        # Storage for geometric objects
        self.points: Dict[str, Point] = {}
        self.lines: Dict[str, Line] = {}
        self.circles: Dict[str, Circle] = {}
        self.triangles: Dict[str, Tuple[Point, Point, Point]] = {}
        self.segments: Dict[str, Segment] = {}
        self.angles: Dict[str, Angle] = {}

        # Track explicitly declared vs. implicitly created objects
        self.declared_points: Set[str] = set()
        self.declared_lines: Set[str] = set()
        self.declared_circles: Set[str] = set()

        # Track constraints and facts
        self.constraints: List[Fact] = []
        self.prove_goals: List[Fact] = []

    # Point management

    def add_point(self, name: str, coords: Optional[Tuple[float, float]] = None,
                  declared: bool = True) -> Point:
        """
        Add a point to the model.

        Args:
            name: Point name (e.g., "A", "B", "P1")
            coords: Optional coordinates (x, y)
            declared: Whether point was explicitly declared in DSL

        Returns:
            Point object

        Raises:
            ValueError: If point already exists with different definition
        """
        if name in self.points:
            existing = self.points[name]
            if coords is not None and existing.coords is not None:
                if existing.coords != coords:
                    raise ValueError(
                        f"Point {name} already exists with different coordinates"
                    )
            return existing

        point = Point(name, coords)
        self.points[name] = point

        if declared:
            self.declared_points.add(name)

        return point

    def get_point(self, name: str) -> Optional[Point]:
        """
        Get point by name.

        Args:
            name: Point name

        Returns:
            Point object, or None if not found
        """
        return self.points.get(name)

    def has_point(self, name: str) -> bool:
        """Check if point exists."""
        return name in self.points

    def get_or_create_point(self, name: str) -> Point:
        """
        Get existing point or create implicit point.

        Args:
            name: Point name

        Returns:
            Point object
        """
        if name in self.points:
            return self.points[name]
        return self.add_point(name, declared=False)

    # Line management

    def add_line(self, point1: Point, point2: Point,
                 line_type: LineType = LineType.LINE,
                 name: Optional[str] = None,
                 declared: bool = True) -> Line:
        """
        Add a line to the model.

        Args:
            point1: First point
            point2: Second point
            line_type: Type of line (LINE, SEGMENT, RAY)
            name: Optional line name
            declared: Whether line was explicitly declared

        Returns:
            Line object
        """
        # Generate name if not provided
        if name is None:
            name = f"{point1.name}{point2.name}"

        # Check if line already exists
        if name in self.lines:
            return self.lines[name]

        line = Line(point1, point2, line_type)
        self.lines[name] = line

        if declared:
            self.declared_lines.add(name)

        return line

    def get_line(self, name: str) -> Optional[Line]:
        """Get line by name."""
        return self.lines.get(name)

    def has_line(self, name: str) -> bool:
        """Check if line exists."""
        return name in self.lines

    def get_or_create_line(self, name: str, line_type: LineType = LineType.LINE) -> Line:
        """
        Get existing line or create implicit line from point names.

        Args:
            name: Line name (e.g., "AB" means line through points A and B)
            line_type: Type of line

        Returns:
            Line object
        """
        if name in self.lines:
            return self.lines[name]

        # Extract point names from line name
        # Typical format: "AB" = line through A and B
        if len(name) >= 2:
            p1_name = name[0]
            p2_name = name[1]

            p1 = self.get_or_create_point(p1_name)
            p2 = self.get_or_create_point(p2_name)

            return self.add_line(p1, p2, line_type, name, declared=False)

        raise ValueError(f"Cannot create line from name: {name}")

    # Segment management

    def add_segment(self, point1: Point, point2: Point,
                    name: Optional[str] = None) -> Segment:
        """
        Add a segment to the model.

        Args:
            point1: First endpoint
            point2: Second endpoint
            name: Optional segment name

        Returns:
            Segment object
        """
        if name is None:
            name = f"{point1.name}{point2.name}"

        if name in self.segments:
            return self.segments[name]

        segment = Segment(point1, point2)
        self.segments[name] = segment

        return segment

    def get_segment(self, name: str) -> Optional[Segment]:
        """Get segment by name."""
        return self.segments.get(name)

    def get_or_create_segment(self, name: str) -> Segment:
        """
        Get existing segment or create from point names.

        Args:
            name: Segment name (e.g., "AB")

        Returns:
            Segment object
        """
        if name in self.segments:
            return self.segments[name]

        # Extract points from name
        if len(name) >= 2:
            p1_name = name[0]
            p2_name = name[1]

            p1 = self.get_or_create_point(p1_name)
            p2 = self.get_or_create_point(p2_name)

            return self.add_segment(p1, p2, name)

        raise ValueError(f"Cannot create segment from name: {name}")

    # Circle management

    def add_circle(self, center: Point, radius: Optional[float] = None,
                   through_point: Optional[Point] = None,
                   name: Optional[str] = None,
                   declared: bool = True) -> Circle:
        """
        Add a circle to the model.

        Args:
            center: Center point
            radius: Optional radius
            through_point: Optional point on circle
            name: Optional circle name
            declared: Whether explicitly declared

        Returns:
            Circle object
        """
        if name is None:
            name = center.name

        if name in self.circles:
            return self.circles[name]

        circle = Circle(center, radius)
        self.circles[name] = circle

        if declared:
            self.declared_circles.add(name)

        return circle

    def get_circle(self, name: str) -> Optional[Circle]:
        """Get circle by name."""
        return self.circles.get(name)

    def has_circle(self, name: str) -> bool:
        """Check if circle exists."""
        return name in self.circles

    # Triangle management

    def add_triangle(self, p1: Point, p2: Point, p3: Point,
                     name: Optional[str] = None) -> Tuple[Point, Point, Point]:
        """
        Add a triangle to the model.

        Args:
            p1, p2, p3: Triangle vertices
            name: Optional triangle name

        Returns:
            Tuple of three points
        """
        if name is None:
            name = f"{p1.name}{p2.name}{p3.name}"

        triangle = (p1, p2, p3)
        self.triangles[name] = triangle

        # Also create the three sides as segments
        self.add_segment(p1, p2)
        self.add_segment(p2, p3)
        self.add_segment(p3, p1)

        return triangle

    def get_triangle(self, name: str) -> Optional[Tuple[Point, Point, Point]]:
        """Get triangle by name."""
        return self.triangles.get(name)

    # Angle management

    def add_angle(self, p1: Point, vertex: Point, p2: Point,
                  name: Optional[str] = None) -> Angle:
        """
        Add an angle to the model.

        Args:
            p1: First ray point
            vertex: Vertex point
            p2: Second ray point
            name: Optional angle name

        Returns:
            Angle object
        """
        if name is None:
            name = f"{p1.name}{vertex.name}{p2.name}"

        if name in self.angles:
            return self.angles[name]

        angle = Angle(p1, vertex, p2)
        self.angles[name] = angle

        return angle

    def get_angle(self, name: str) -> Optional[Angle]:
        """Get angle by name."""
        return self.angles.get(name)

    def get_or_create_angle(self, name: str) -> Angle:
        """
        Get existing angle or create from point names.

        Args:
            name: Angle name (e.g., "ABC" means angle at B)

        Returns:
            Angle object
        """
        if name in self.angles:
            return self.angles[name]

        # Extract points from name (ABC means angle at B)
        if len(name) >= 3:
            p1_name = name[0]
            vertex_name = name[1]
            p2_name = name[2]

            p1 = self.get_or_create_point(p1_name)
            vertex = self.get_or_create_point(vertex_name)
            p2 = self.get_or_create_point(p2_name)

            return self.add_angle(p1, vertex, p2, name)

        raise ValueError(f"Cannot create angle from name: {name}")

    # Constraint and goal management

    def add_constraint(self, fact: Fact):
        """
        Add a constraint fact to the model.

        Args:
            fact: Constraint fact
        """
        self.constraints.append(fact)

    def add_prove_goal(self, fact: Fact):
        """
        Add a prove goal to the model.

        Args:
            fact: Goal fact to prove
        """
        self.prove_goals.append(fact)

    # Query methods

    def get_all_points(self) -> List[Point]:
        """Get all points in model."""
        return list(self.points.values())

    def get_all_lines(self) -> List[Line]:
        """Get all lines in model."""
        return list(self.lines.values())

    def get_all_circles(self) -> List[Circle]:
        """Get all circles in model."""
        return list(self.circles.values())

    def get_all_triangles(self) -> List[Tuple[Point, Point, Point]]:
        """Get all triangles in model."""
        return list(self.triangles.values())

    def get_declared_points(self) -> Set[str]:
        """Get names of explicitly declared points."""
        return self.declared_points.copy()

    def get_declared_lines(self) -> Set[str]:
        """Get names of explicitly declared lines."""
        return self.declared_lines.copy()

    def get_declared_circles(self) -> Set[str]:
        """Get names of explicitly declared circles."""
        return self.declared_circles.copy()

    def summary(self) -> str:
        """
        Get a summary of the geometry model.

        Returns:
            Human-readable summary string
        """
        lines = ["GeometryModel Summary:"]
        lines.append(f"  Points: {len(self.points)} ({len(self.declared_points)} declared)")
        lines.append(f"  Lines: {len(self.lines)} ({len(self.declared_lines)} declared)")
        lines.append(f"  Circles: {len(self.circles)} ({len(self.declared_circles)} declared)")
        lines.append(f"  Triangles: {len(self.triangles)}")
        lines.append(f"  Segments: {len(self.segments)}")
        lines.append(f"  Angles: {len(self.angles)}")
        lines.append(f"  Constraints: {len(self.constraints)}")
        lines.append(f"  Prove Goals: {len(self.prove_goals)}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.summary()
