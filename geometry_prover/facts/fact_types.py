"""
Fact type system for the geometry prover.

This module defines the complete hierarchy of geometric facts (40+ types).
Facts are the "logical atoms" of geometric knowledge.

Fact Categories:
1. Structural Facts (geometric relationships)
2. Length/Ratio Facts (distance and proportion)
3. Angle Facts (angle measurements and relationships)
4. Line Relation Facts (parallel, perpendicular, etc.)
5. Shape Facts (triangles, polygons)
6. Circle Facts (tangents, chords, arcs)
7. Area Facts (area relationships)
8. Logic Facts (auxiliary conditions)
"""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
from geometry_prover.utils import Point, Line, Circle, Angle, Segment


class Fact(ABC):
    """
    Base class for all geometric facts.

    A Fact represents an atomic piece of geometric knowledge, such as:
    - "Point P is on line AB"
    - "Segment AB equals segment CD"
    - "Angle ABC is a right angle"

    All facts must be hashable and support equality checking for use in FactBase.
    """

    def __init__(self, fact_type: str, parameters: Dict[str, Any]):
        """
        Initialize a fact.

        Args:
            fact_type: String identifier for the fact type (e.g., "On", "EqualSegment")
            parameters: Dictionary of parameters defining the fact
        """
        self.fact_type = fact_type
        self.parameters = parameters
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """Validate that parameters are correct for this fact type."""
        pass

    @abstractmethod
    def to_string(self) -> str:
        """Convert fact to human-readable string."""
        pass

    @abstractmethod
    def get_involved_points(self) -> set[Point]:
        """Get all points involved in this fact."""
        pass

    def __eq__(self, other) -> bool:
        """Facts are equal if they have the same type and parameters."""
        if not isinstance(other, Fact):
            return False
        return self.fact_type == other.fact_type and self._params_equal(other.parameters)

    def _params_equal(self, other_params: Dict[str, Any]) -> bool:
        """Check if parameters are equal (handles geometric objects)."""
        if set(self.parameters.keys()) != set(other_params.keys()):
            return False
        for key in self.parameters:
            if self.parameters[key] != other_params[key]:
                return False
        return True

    def __hash__(self) -> int:
        """Hash based on fact type and parameters."""
        # Create a hashable representation of parameters
        param_items = []
        for key in sorted(self.parameters.keys()):
            val = self.parameters[key]
            if isinstance(val, (list, set)):
                val = tuple(sorted(val, key=lambda x: str(x)))
            param_items.append((key, val))
        return hash((self.fact_type, tuple(param_items)))

    def __repr__(self) -> str:
        return f"{self.fact_type}({self.to_string()})"


# ============================================================================
# STRUCTURAL FACTS (Geometric Relationships)
# ============================================================================


class On(Fact):
    """Point P is on line L."""

    def __init__(self, point: Point, line: Line):
        super().__init__("On", {"point": point, "line": line})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["line"], Line)

    def to_string(self) -> str:
        p = self.parameters["point"]
        l = self.parameters["line"]
        return f"{p.name} on {l}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["line"].point1,
                self.parameters["line"].point2}


class OnSegment(Fact):
    """Point P is on segment AB (between A and B)."""

    def __init__(self, point: Point, point1: Point, point2: Point):
        super().__init__("OnSegment", {"point": point, "point1": point1, "point2": point2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)

    def to_string(self) -> str:
        p = self.parameters["point"]
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        return f"{p.name} on segment {p1.name}{p2.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["point1"],
                self.parameters["point2"]}


class OnCircle(Fact):
    """Point P is on circle C."""

    def __init__(self, point: Point, circle: Circle):
        super().__init__("OnCircle", {"point": point, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        p = self.parameters["point"]
        c = self.parameters["circle"]
        return f"{p.name} on {c}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["circle"].center}


class Collinear(Fact):
    """Points A, B, C are collinear."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("Collinear", {"point1": point1, "point2": point2, "point3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)
        assert isinstance(self.parameters["point3"], Point)

    def to_string(self) -> str:
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        p3 = self.parameters["point3"]
        return f"{p1.name}, {p2.name}, {p3.name} are collinear"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point1"], self.parameters["point2"],
                self.parameters["point3"]}


class NotCollinear(Fact):
    """Points A, B, C are not collinear."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("NotCollinear", {"point1": point1, "point2": point2, "point3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)
        assert isinstance(self.parameters["point3"], Point)

    def to_string(self) -> str:
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        p3 = self.parameters["point3"]
        return f"{p1.name}, {p2.name}, {p3.name} are not collinear"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point1"], self.parameters["point2"],
                self.parameters["point3"]}


class Between(Fact):
    """Point B is between points A and C on a line."""

    def __init__(self, middle: Point, point1: Point, point2: Point):
        super().__init__("Between", {"middle": middle, "point1": point1, "point2": point2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["middle"], Point)
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)

    def to_string(self) -> str:
        m = self.parameters["middle"]
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        return f"{m.name} is between {p1.name} and {p2.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["middle"], self.parameters["point1"],
                self.parameters["point2"]}


class Midpoint(Fact):
    """M is the midpoint of segment AB."""

    def __init__(self, midpoint: Point, point1: Point, point2: Point):
        super().__init__("Midpoint", {"midpoint": midpoint, "point1": point1, "point2": point2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["midpoint"], Point)
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)

    def to_string(self) -> str:
        m = self.parameters["midpoint"]
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        return f"{m.name} is midpoint of {p1.name}{p2.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["midpoint"], self.parameters["point1"],
                self.parameters["point2"]}


class FootOfPerpendicular(Fact):
    """F is the foot of perpendicular from point P to line L."""

    def __init__(self, foot: Point, point: Point, line: Line):
        super().__init__("FootOfPerpendicular", {"foot": foot, "point": point, "line": line})

    def _validate(self) -> None:
        assert isinstance(self.parameters["foot"], Point)
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["line"], Line)

    def to_string(self) -> str:
        f = self.parameters["foot"]
        p = self.parameters["point"]
        l = self.parameters["line"]
        return f"{f.name} is foot of perpendicular from {p.name} to {l}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["foot"], self.parameters["point"],
                self.parameters["line"].point1, self.parameters["line"].point2}


class ReflectPoint(Fact):
    """P' is the reflection of point P across line L."""

    def __init__(self, reflected: Point, original: Point, line: Line):
        super().__init__("ReflectPoint", {"reflected": reflected, "original": original, "line": line})

    def _validate(self) -> None:
        assert isinstance(self.parameters["reflected"], Point)
        assert isinstance(self.parameters["original"], Point)
        assert isinstance(self.parameters["line"], Line)

    def to_string(self) -> str:
        r = self.parameters["reflected"]
        o = self.parameters["original"]
        l = self.parameters["line"]
        return f"{r.name} is reflection of {o.name} across {l}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["reflected"], self.parameters["original"],
                self.parameters["line"].point1, self.parameters["line"].point2}


class Intersect(Fact):
    """Two geometric objects intersect at point P."""

    def __init__(self, obj1: Line | Circle, obj2: Line | Circle, point: Point):
        super().__init__("Intersect", {"obj1": obj1, "obj2": obj2, "point": point})

    def _validate(self) -> None:
        assert isinstance(self.parameters["obj1"], (Line, Circle))
        assert isinstance(self.parameters["obj2"], (Line, Circle))
        assert isinstance(self.parameters["point"], Point)

    def to_string(self) -> str:
        o1 = self.parameters["obj1"]
        o2 = self.parameters["obj2"]
        p = self.parameters["point"]
        return f"{o1} intersects {o2} at {p.name}"

    def get_involved_points(self) -> set[Point]:
        points = {self.parameters["point"]}
        if isinstance(self.parameters["obj1"], Line):
            points.update({self.parameters["obj1"].point1, self.parameters["obj1"].point2})
        else:
            points.add(self.parameters["obj1"].center)
        if isinstance(self.parameters["obj2"], Line):
            points.update({self.parameters["obj2"].point1, self.parameters["obj2"].point2})
        else:
            points.add(self.parameters["obj2"].center)
        return points


class Concurrent(Fact):
    """Multiple lines meet at a single point."""

    def __init__(self, point: Point, lines: list[Line]):
        super().__init__("Concurrent", {
            "point": point,
            "lines": lines
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["lines"], list)
        assert all(isinstance(l, Line) for l in self.parameters["lines"])
        assert len(self.parameters["lines"]) >= 2

    def to_string(self) -> str:
        p = self.parameters["point"]
        lines = self.parameters["lines"]
        line_names = ", ".join(str(l) for l in lines)
        return f"Lines {line_names} meet at {p.name}"

    def get_involved_points(self) -> set[Point]:
        points = {self.parameters["point"]}
        for line in self.parameters["lines"]:
            points.add(line.point1)
            points.add(line.point2)
        return points


# ============================================================================
# LENGTH/RATIO FACTS
# ============================================================================


class EqualSegment(Fact):
    """Segment AB equals segment CD."""

    def __init__(self, segment1: Segment | tuple[Point, Point],
                 segment2: Segment | tuple[Point, Point]):
        # Handle both Segment objects and point tuples
        if isinstance(segment1, tuple):
            segment1 = Segment(segment1[0], segment1[1])
        if isinstance(segment2, tuple):
            segment2 = Segment(segment2[0], segment2[1])
        super().__init__("EqualSegment", {"segment1": segment1, "segment2": segment2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["segment1"], Segment)
        assert isinstance(self.parameters["segment2"], Segment)

    def to_string(self) -> str:
        s1 = self.parameters["segment1"]
        s2 = self.parameters["segment2"]
        return f"{s1} = {s2}"

    def get_involved_points(self) -> set[Point]:
        s1 = self.parameters["segment1"]
        s2 = self.parameters["segment2"]
        return {s1.point1, s1.point2, s2.point1, s2.point2}


class ProportionalSegment(Fact):
    """Segment AB is proportional to segment CD by ratio k: |AB| = k * |CD|."""

    def __init__(self, segment1: Segment | tuple[Point, Point],
                 segment2: Segment | tuple[Point, Point],
                 ratio: float):
        if isinstance(segment1, tuple):
            segment1 = Segment(segment1[0], segment1[1])
        if isinstance(segment2, tuple):
            segment2 = Segment(segment2[0], segment2[1])
        super().__init__("ProportionalSegment",
                        {"segment1": segment1, "segment2": segment2, "ratio": ratio})

    def _validate(self) -> None:
        assert isinstance(self.parameters["segment1"], Segment)
        assert isinstance(self.parameters["segment2"], Segment)
        assert isinstance(self.parameters["ratio"], (int, float))

    def to_string(self) -> str:
        s1 = self.parameters["segment1"]
        s2 = self.parameters["segment2"]
        r = self.parameters["ratio"]
        return f"|{s1}| = {r} * |{s2}|"

    def get_involved_points(self) -> set[Point]:
        s1 = self.parameters["segment1"]
        s2 = self.parameters["segment2"]
        return {s1.point1, s1.point2, s2.point1, s2.point2}


class SegmentRatio(Fact):
    """Ratio of segments: |AB| / |CD| = r."""

    def __init__(self, point1: Point, point2: Point, point3: Point, point4: Point, ratio: float):
        super().__init__("SegmentRatio",
                        {"p1": point1, "p2": point2, "p3": point3, "p4": point4, "ratio": ratio})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)
        assert isinstance(self.parameters["p4"], Point)
        assert isinstance(self.parameters["ratio"], (int, float))

    def to_string(self) -> str:
        p1, p2 = self.parameters["p1"], self.parameters["p2"]
        p3, p4 = self.parameters["p3"], self.parameters["p4"]
        r = self.parameters["ratio"]
        return f"|{p1.name}{p2.name}| / |{p3.name}{p4.name}| = {r}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"],
                self.parameters["p3"], self.parameters["p4"]}


class LengthValue(Fact):
    """Length of segment AB equals value v."""

    def __init__(self, segment: Segment | tuple[Point, Point], value: float):
        if isinstance(segment, tuple):
            segment = Segment(segment[0], segment[1])
        super().__init__("LengthValue", {"segment": segment, "value": value})

    def _validate(self) -> None:
        assert isinstance(self.parameters["segment"], Segment)
        assert isinstance(self.parameters["value"], (int, float))

    def to_string(self) -> str:
        s = self.parameters["segment"]
        v = self.parameters["value"]
        return f"|{s}| = {v}"

    def get_involved_points(self) -> set[Point]:
        s = self.parameters["segment"]
        return {s.point1, s.point2}


# ============================================================================
# ANGLE FACTS
# ============================================================================


class EqualAngle(Fact):
    """Angle ABC equals angle DEF."""

    def __init__(self, angle1: Angle, angle2: Angle):
        super().__init__("EqualAngle", {"angle1": angle1, "angle2": angle2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle1"], Angle)
        assert isinstance(self.parameters["angle2"], Angle)

    def to_string(self) -> str:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return f"∠{a1.point1.name}{a1.vertex.name}{a1.point2.name} = ∠{a2.point1.name}{a2.vertex.name}{a2.point2.name}"

    def get_involved_points(self) -> set[Point]:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return {a1.point1, a1.vertex, a1.point2, a2.point1, a2.vertex, a2.point2}


class RightAngle(Fact):
    """Angle ABC is a right angle (90 degrees)."""

    def __init__(self, angle: Angle):
        super().__init__("RightAngle", {"angle": angle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle"], Angle)

    def to_string(self) -> str:
        a = self.parameters["angle"]
        return f"∠{a.point1.name}{a.vertex.name}{a.point2.name} = 90°"

    def get_involved_points(self) -> set[Point]:
        a = self.parameters["angle"]
        return {a.point1, a.vertex, a.point2}


class SupplementaryAngle(Fact):
    """Two angles are supplementary (sum to 180 degrees)."""

    def __init__(self, angle1: Angle, angle2: Angle):
        super().__init__("SupplementaryAngle", {"angle1": angle1, "angle2": angle2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle1"], Angle)
        assert isinstance(self.parameters["angle2"], Angle)

    def to_string(self) -> str:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return f"∠{a1.point1.name}{a1.vertex.name}{a1.point2.name} + ∠{a2.point1.name}{a2.vertex.name}{a2.point2.name} = 180°"

    def get_involved_points(self) -> set[Point]:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return {a1.point1, a1.vertex, a1.point2, a2.point1, a2.vertex, a2.point2}


class AngleSum(Fact):
    """Sum of two angles equals a value."""

    def __init__(self, angle1: Angle, angle2: Angle, sum_value: float):
        super().__init__("AngleSum", {"angle1": angle1, "angle2": angle2, "sum": sum_value})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle1"], Angle)
        assert isinstance(self.parameters["angle2"], Angle)
        assert isinstance(self.parameters["sum"], (int, float))

    def to_string(self) -> str:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        s = self.parameters["sum"]
        return f"∠{a1.point1.name}{a1.vertex.name}{a1.point2.name} + ∠{a2.point1.name}{a2.vertex.name}{a2.point2.name} = {s}°"

    def get_involved_points(self) -> set[Point]:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return {a1.point1, a1.vertex, a1.point2, a2.point1, a2.vertex, a2.point2}


class AngleValue(Fact):
    """Angle ABC has a specific value."""

    def __init__(self, angle: Angle, value: float):
        super().__init__("AngleValue", {"angle": angle, "value": value})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle"], Angle)
        assert isinstance(self.parameters["value"], (int, float))

    def to_string(self) -> str:
        a = self.parameters["angle"]
        v = self.parameters["value"]
        return f"∠{a.point1.name}{a.vertex.name}{a.point2.name} = {v}°"

    def get_involved_points(self) -> set[Point]:
        a = self.parameters["angle"]
        return {a.point1, a.vertex, a.point2}


class VerticalAngles(Fact):
    """Two angles are vertical (formed by intersecting lines)."""

    def __init__(self, angle1: Angle, angle2: Angle, intersection: Point):
        super().__init__("VerticalAngles", {
            "angle1": angle1,
            "angle2": angle2,
            "intersection": intersection
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle1"], Angle)
        assert isinstance(self.parameters["angle2"], Angle)
        assert isinstance(self.parameters["intersection"], Point)

    def to_string(self) -> str:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return f"∠{a1.point1.name}{a1.vertex.name}{a1.point2.name} and ∠{a2.point1.name}{a2.vertex.name}{a2.point2.name} are vertical"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["angle1"].point1,
            self.parameters["angle1"].vertex,
            self.parameters["angle1"].point2,
            self.parameters["angle2"].point1,
            self.parameters["angle2"].vertex,
            self.parameters["angle2"].point2,
            self.parameters["intersection"]
        }


class ComplementaryAngles(Fact):
    """Two angles are complementary (sum = 90°)."""

    def __init__(self, angle1: Angle, angle2: Angle):
        super().__init__("ComplementaryAngles", {
            "angle1": angle1,
            "angle2": angle2
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle1"], Angle)
        assert isinstance(self.parameters["angle2"], Angle)

    def to_string(self) -> str:
        a1 = self.parameters["angle1"]
        a2 = self.parameters["angle2"]
        return f"∠{a1.vertex.name} + ∠{a2.vertex.name} = 90°"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["angle1"].point1,
            self.parameters["angle1"].vertex,
            self.parameters["angle1"].point2,
            self.parameters["angle2"].point1,
            self.parameters["angle2"].vertex,
            self.parameters["angle2"].point2
        }


class AngleBisector(Fact):
    """Line/segment bisects an angle."""

    def __init__(self, bisector: Line, vertex: Point, ray1: Point, ray2: Point):
        super().__init__("AngleBisector", {
            "bisector": bisector,
            "vertex": vertex,
            "ray1": ray1,
            "ray2": ray2
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["bisector"], Line)
        assert isinstance(self.parameters["vertex"], Point)
        assert isinstance(self.parameters["ray1"], Point)
        assert isinstance(self.parameters["ray2"], Point)

    def to_string(self) -> str:
        b = self.parameters["bisector"]
        v = self.parameters["vertex"]
        p1 = self.parameters["ray1"]
        p2 = self.parameters["ray2"]
        return f"{b} bisects ∠{p1.name}{v.name}{p2.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["vertex"],
            self.parameters["ray1"],
            self.parameters["ray2"]
        }


class AngleMeasure(Fact):
    """Angle has specific numeric measure in degrees."""

    def __init__(self, angle: Angle, measure: float):
        super().__init__("AngleMeasure", {
            "angle": angle,
            "measure": measure
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle"], Angle)
        assert isinstance(self.parameters["measure"], (int, float))

    def to_string(self) -> str:
        angle = self.parameters["angle"]
        measure = self.parameters["measure"]
        return f"∠{angle.vertex.name} = {measure}°"

    def get_involved_points(self) -> set[Point]:
        angle = self.parameters["angle"]
        return {angle.point1, angle.vertex, angle.point2}


# ============================================================================
# LINE RELATION FACTS
# ============================================================================


class Parallel(Fact):
    """Line AB is parallel to line CD."""

    def __init__(self, line1: Line, line2: Line):
        super().__init__("Parallel", {"line1": line1, "line2": line2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line1"], Line)
        assert isinstance(self.parameters["line2"], Line)

    def to_string(self) -> str:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return f"{l1} ∥ {l2}"

    def get_involved_points(self) -> set[Point]:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return {l1.point1, l1.point2, l2.point1, l2.point2}


class Perpendicular(Fact):
    """Line AB is perpendicular to line CD."""

    def __init__(self, line1: Line, line2: Line):
        super().__init__("Perpendicular", {"line1": line1, "line2": line2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line1"], Line)
        assert isinstance(self.parameters["line2"], Line)

    def to_string(self) -> str:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return f"{l1} ⊥ {l2}"

    def get_involved_points(self) -> set[Point]:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return {l1.point1, l1.point2, l2.point1, l2.point2}


class SameLine(Fact):
    """Two line segments represent the same line."""

    def __init__(self, line1: Line, line2: Line):
        super().__init__("SameLine", {"line1": line1, "line2": line2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line1"], Line)
        assert isinstance(self.parameters["line2"], Line)

    def to_string(self) -> str:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return f"{l1} is same as {l2}"

    def get_involved_points(self) -> set[Point]:
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return {l1.point1, l1.point2, l2.point1, l2.point2}


# ============================================================================
# SHAPE FACTS (Triangles and Polygons)
# ============================================================================


class Triangle(Fact):
    """Points A, B, C form a triangle (not collinear)."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("Triangle", {"p1": point1, "p2": point2, "p3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"△{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]}


class IsoscelesTriangle(Fact):
    """Triangle ABC is isosceles (typically with AB = AC)."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("IsoscelesTriangle", {"p1": point1, "p2": point2, "p3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"△{p1.name}{p2.name}{p3.name} is isosceles"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]}


class EquilateralTriangle(Fact):
    """Triangle ABC is equilateral (all sides equal)."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("EquilateralTriangle", {"p1": point1, "p2": point2, "p3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"△{p1.name}{p2.name}{p3.name} is equilateral"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]}


class SimilarTriangle(Fact):
    """Triangle ABC is similar to triangle DEF (△ABC ~ △DEF)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point, p5: Point, p6: Point):
        super().__init__("SimilarTriangle",
                        {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6})

    def _validate(self) -> None:
        for i in range(1, 7):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        p4, p5, p6 = self.parameters["p4"], self.parameters["p5"], self.parameters["p6"]
        return f"△{p1.name}{p2.name}{p3.name} ~ △{p4.name}{p5.name}{p6.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 7)}


class CongruentTriangle(Fact):
    """Triangle ABC is congruent to triangle DEF (△ABC ≅ △DEF)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point, p5: Point, p6: Point):
        super().__init__("CongruentTriangle",
                        {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6})

    def _validate(self) -> None:
        for i in range(1, 7):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        p4, p5, p6 = self.parameters["p4"], self.parameters["p5"], self.parameters["p6"]
        return f"△{p1.name}{p2.name}{p3.name} ≅ △{p4.name}{p5.name}{p6.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 7)}


class Orthocenter(Fact):
    """Point is orthocenter of triangle (altitude intersection)."""

    def __init__(self, orthocenter: Point, p1: Point, p2: Point, p3: Point):
        super().__init__("Orthocenter", {
            "orthocenter": orthocenter,
            "p1": p1, "p2": p2, "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["orthocenter"], Point)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        h = self.parameters["orthocenter"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{h.name} is orthocenter of △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["orthocenter"],
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class Centroid(Fact):
    """Point is centroid of triangle (median intersection)."""

    def __init__(self, centroid: Point, p1: Point, p2: Point, p3: Point):
        super().__init__("Centroid", {
            "centroid": centroid,
            "p1": p1, "p2": p2, "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["centroid"], Point)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        g = self.parameters["centroid"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{g.name} is centroid of △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["centroid"],
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class Incenter(Fact):
    """Point is incenter of triangle (angle bisector intersection)."""

    def __init__(self, incenter: Point, p1: Point, p2: Point, p3: Point):
        super().__init__("Incenter", {
            "incenter": incenter,
            "p1": p1, "p2": p2, "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["incenter"], Point)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        i = self.parameters["incenter"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{i.name} is incenter of △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["incenter"],
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class Circumcenter(Fact):
    """Point is circumcenter of triangle (perpendicular bisector intersection)."""

    def __init__(self, circumcenter: Point, p1: Point, p2: Point, p3: Point):
        super().__init__("Circumcenter", {
            "circumcenter": circumcenter,
            "p1": p1, "p2": p2, "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["circumcenter"], Point)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        o = self.parameters["circumcenter"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{o.name} is circumcenter of △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["circumcenter"],
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class Inside(Fact):
    """Point is inside triangle."""

    def __init__(self, point: Point, p1: Point, p2: Point, p3: Point):
        super().__init__("Inside", {
            "point": point,
            "p1": p1, "p2": p2, "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        pt = self.parameters["point"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{pt.name} is inside △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["point"],
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


# ============================================================================
# QUADRILATERAL FACTS (Week 8 Day 3 - Quadrilateral Support)
# ============================================================================

class Quadrilateral(Fact):
    """Quadrilateral ABCD (general four-sided polygon)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Quadrilateral", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Quadrilateral {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


class Rectangle(Fact):
    """Rectangle ABCD (quadrilateral with 4 right angles)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Rectangle", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Rectangle {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


class Square(Fact):
    """Square ABCD (rectangle with all sides equal)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Square", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Square {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


class Parallelogram(Fact):
    """Parallelogram ABCD (opposite sides parallel)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Parallelogram", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Parallelogram {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


class Rhombus(Fact):
    """Rhombus ABCD (parallelogram with all sides equal)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Rhombus", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Rhombus {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


class Trapezoid(Fact):
    """Trapezoid ABCD (at least one pair of parallel sides)."""

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        super().__init__("Trapezoid", {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4
        })

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Trapezoid {p1.name}{p2.name}{p3.name}{p4.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


# ============================================================================
# CIRCLE FACTS
# ============================================================================


class TangentAt(Fact):
    """Line L is tangent to circle C at point P."""

    def __init__(self, line: Line, circle: Circle, point: Point):
        super().__init__("TangentAt", {"line": line, "circle": circle, "point": point})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line"], Line)
        assert isinstance(self.parameters["circle"], Circle)
        assert isinstance(self.parameters["point"], Point)

    def to_string(self) -> str:
        l = self.parameters["line"]
        c = self.parameters["circle"]
        p = self.parameters["point"]
        return f"{l} is tangent to {c} at {p.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["line"].point1,
                self.parameters["line"].point2, self.parameters["circle"].center}


class Chord(Fact):
    """Segment AB is a chord of circle C."""

    def __init__(self, point1: Point, point2: Point, circle: Circle):
        super().__init__("Chord", {"p1": point1, "p2": point2, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        p1, p2 = self.parameters["p1"], self.parameters["p2"]
        c = self.parameters["circle"]
        return f"{p1.name}{p2.name} is a chord of {c}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["circle"].center}


class Diameter(Fact):
    """Segment AB is a diameter of circle C."""

    def __init__(self, point1: Point, point2: Point, circle: Circle):
        super().__init__("Diameter", {"p1": point1, "p2": point2, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        p1, p2 = self.parameters["p1"], self.parameters["p2"]
        c = self.parameters["circle"]
        return f"{p1.name}{p2.name} is a diameter of {c}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["circle"].center}


class Arc(Fact):
    """Arc from A to B on circle C."""

    def __init__(self, point1: Point, point2: Point, circle: Circle):
        super().__init__("Arc", {"p1": point1, "p2": point2, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        p1, p2 = self.parameters["p1"], self.parameters["p2"]
        c = self.parameters["circle"]
        return f"Arc {p1.name}{p2.name} on {c}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["circle"].center}


class CyclicQuadrilateral(Fact):
    """Quadrilateral ABCD is cyclic (all vertices on a circle)."""

    def __init__(self, point1: Point, point2: Point, point3: Point, point4: Point):
        super().__init__("CyclicQuadrilateral",
                        {"p1": point1, "p2": point2, "p3": point3, "p4": point4})

    def _validate(self) -> None:
        for i in range(1, 5):
            assert isinstance(self.parameters[f"p{i}"], Point)

    def to_string(self) -> str:
        p1, p2, p3, p4 = [self.parameters[f"p{i}"] for i in range(1, 5)]
        return f"Quadrilateral {p1.name}{p2.name}{p3.name}{p4.name} is cyclic"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters[f"p{i}"] for i in range(1, 5)}


# ============================================================================
# CIRCLE FACTS - Week 8 Day 3 Phase 2
# ============================================================================

class InscribedAngle(Fact):
    """Angle ABC is inscribed in circle (vertex B on circle, endpoints A,C on circle)."""

    def __init__(self, angle: Angle, circle: Circle):
        super().__init__("InscribedAngle", {"angle": angle, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle"], Angle)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        angle = self.parameters["angle"]
        circle = self.parameters["circle"]
        return f"∠{angle} is inscribed in {circle}"

    def get_involved_points(self) -> set[Point]:
        angle = self.parameters["angle"]
        circle = self.parameters["circle"]
        return {angle.vertex, angle.ray1, angle.ray2, circle.center}


class CentralAngle(Fact):
    """Angle AOB is central angle of circle (vertex O at center)."""

    def __init__(self, angle: Angle, circle: Circle):
        super().__init__("CentralAngle", {"angle": angle, "circle": circle})

    def _validate(self) -> None:
        assert isinstance(self.parameters["angle"], Angle)
        assert isinstance(self.parameters["circle"], Circle)

    def to_string(self) -> str:
        angle = self.parameters["angle"]
        circle = self.parameters["circle"]
        return f"∠{angle} is central angle of {circle}"

    def get_involved_points(self) -> set[Point]:
        angle = self.parameters["angle"]
        circle = self.parameters["circle"]
        return {angle.vertex, angle.ray1, angle.ray2, circle.center}


class InscribedCircle(Fact):
    """Circle is inscribed in triangle (incircle, tangent to all three sides)."""

    def __init__(self, circle: Circle, p1: Point, p2: Point, p3: Point):
        super().__init__("InscribedCircle", {
            "circle": circle,
            "p1": p1,
            "p2": p2,
            "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["circle"], Circle)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        c = self.parameters["circle"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{c} is inscribed in △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["circle"].center,
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class CircumscribedCircle(Fact):
    """Circle is circumscribed around triangle (circumcircle, all vertices on circle)."""

    def __init__(self, circle: Circle, p1: Point, p2: Point, p3: Point):
        super().__init__("CircumscribedCircle", {
            "circle": circle,
            "p1": p1,
            "p2": p2,
            "p3": p3
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["circle"], Circle)
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        c = self.parameters["circle"]
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"{c} is circumscribed around △{p1.name}{p2.name}{p3.name}"

    def get_involved_points(self) -> set[Point]:
        return {
            self.parameters["circle"].center,
            self.parameters["p1"],
            self.parameters["p2"],
            self.parameters["p3"]
        }


class RadiusValue(Fact):
    """Circle has radius r."""

    def __init__(self, circle: Circle, radius: float):
        super().__init__("RadiusValue", {"circle": circle, "radius": radius})

    def _validate(self) -> None:
        assert isinstance(self.parameters["circle"], Circle)
        assert isinstance(self.parameters["radius"], (int, float))
        assert self.parameters["radius"] > 0

    def to_string(self) -> str:
        c = self.parameters["circle"]
        r = self.parameters["radius"]
        return f"{c} has radius {r}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["circle"].center}


# ============================================================================
# AREA FACTS
# ============================================================================


class AreaValue(Fact):
    """Area of a geometric shape equals value v."""

    def __init__(self, shape: str, points: list[Point], value: float):
        """
        Args:
            shape: Type of shape ("triangle", "quadrilateral", etc.)
            points: List of points defining the shape
            value: Area value
        """
        super().__init__("AreaValue", {"shape": shape, "points": points, "value": value})

    def _validate(self) -> None:
        assert isinstance(self.parameters["shape"], str)
        assert isinstance(self.parameters["points"], list)
        assert all(isinstance(p, Point) for p in self.parameters["points"])
        assert isinstance(self.parameters["value"], (int, float))

    def to_string(self) -> str:
        shape = self.parameters["shape"]
        points = self.parameters["points"]
        value = self.parameters["value"]
        point_names = "".join(p.name for p in points)
        return f"Area({shape} {point_names}) = {value}"

    def get_involved_points(self) -> set[Point]:
        return set(self.parameters["points"])


class AreaRelation(Fact):
    """Ratio of areas of two shapes."""

    def __init__(self, shape1: str, points1: list[Point],
                 shape2: str, points2: list[Point], ratio: float):
        super().__init__("AreaRelation",
                        {"shape1": shape1, "points1": points1,
                         "shape2": shape2, "points2": points2, "ratio": ratio})

    def _validate(self) -> None:
        assert isinstance(self.parameters["shape1"], str)
        assert isinstance(self.parameters["shape2"], str)
        assert isinstance(self.parameters["points1"], list)
        assert isinstance(self.parameters["points2"], list)
        assert isinstance(self.parameters["ratio"], (int, float))

    def to_string(self) -> str:
        s1, p1 = self.parameters["shape1"], self.parameters["points1"]
        s2, p2 = self.parameters["shape2"], self.parameters["points2"]
        r = self.parameters["ratio"]
        n1 = "".join(p.name for p in p1)
        n2 = "".join(p.name for p in p2)
        return f"Area({s1} {n1}) / Area({s2} {n2}) = {r}"

    def get_involved_points(self) -> set[Point]:
        return set(self.parameters["points1"] + self.parameters["points2"])


# ============================================================================
# LOGIC/AUXILIARY FACTS
# ============================================================================


class Distinct(Fact):
    """Points P and Q are distinct (not the same point)."""

    def __init__(self, point1: Point, point2: Point):
        super().__init__("Distinct", {"p1": point1, "p2": point2})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)

    def to_string(self) -> str:
        p1, p2 = self.parameters["p1"], self.parameters["p2"]
        return f"{p1.name} ≠ {p2.name}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"]}


class NonDegenerateTriangle(Fact):
    """Triangle ABC is non-degenerate (vertices not collinear, positive area)."""

    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__("NonDegenerateTriangle", {"p1": point1, "p2": point2, "p3": point3})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        return f"△{p1.name}{p2.name}{p3.name} is non-degenerate"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]}


class Orientation(Fact):
    """Orientation of three points (clockwise/counterclockwise)."""

    def __init__(self, point1: Point, point2: Point, point3: Point, sign: int):
        """
        Args:
            sign: +1 for counterclockwise, -1 for clockwise, 0 for collinear
        """
        super().__init__("Orientation", {"p1": point1, "p2": point2, "p3": point3, "sign": sign})

    def _validate(self) -> None:
        assert isinstance(self.parameters["p1"], Point)
        assert isinstance(self.parameters["p2"], Point)
        assert isinstance(self.parameters["p3"], Point)
        assert self.parameters["sign"] in [-1, 0, 1]

    def to_string(self) -> str:
        p1, p2, p3 = self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]
        sign = self.parameters["sign"]
        orientation = "CCW" if sign > 0 else ("CW" if sign < 0 else "collinear")
        return f"Orientation({p1.name}, {p2.name}, {p3.name}) = {orientation}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["p1"], self.parameters["p2"], self.parameters["p3"]}


# ============================================================================
# COORDINATE GEOMETRY FACTS (Week 8 Day 3 - Phase 3)
# Support for 平面直角坐标系 (Cartesian coordinate system)
# ============================================================================

class Coordinates(Fact):
    """Point P has coordinates (x, y) in Cartesian plane."""

    def __init__(self, point: Point, x: float, y: float):
        super().__init__("Coordinates", {"point": point, "x": x, "y": y})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["x"], (int, float))
        assert isinstance(self.parameters["y"], (int, float))

    def to_string(self) -> str:
        p = self.parameters["point"]
        x = self.parameters["x"]
        y = self.parameters["y"]
        return f"{p.name}({x}, {y})"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"]}


class LineEquation(Fact):
    """Line L has equation ax + by + c = 0."""

    def __init__(self, line: Line, a: float, b: float, c: float):
        """
        Args:
            line: The line
            a, b, c: Coefficients in ax + by + c = 0

        Note: At least one of a, b must be non-zero
        """
        super().__init__("LineEquation", {"line": line, "a": a, "b": b, "c": c})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line"], Line)
        assert isinstance(self.parameters["a"], (int, float))
        assert isinstance(self.parameters["b"], (int, float))
        assert isinstance(self.parameters["c"], (int, float))
        # At least one of a, b must be non-zero
        assert self.parameters["a"] != 0 or self.parameters["b"] != 0

    def to_string(self) -> str:
        l = self.parameters["line"]
        a, b, c = self.parameters["a"], self.parameters["b"], self.parameters["c"]
        return f"{l}: {a}x + {b}y + {c} = 0"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["line"].point1, self.parameters["line"].point2}


class Slope(Fact):
    """Line L has slope m."""

    def __init__(self, line: Line, slope: float):
        """
        Args:
            line: The line
            slope: The slope value (can be float('inf') for vertical lines)
        """
        super().__init__("Slope", {"line": line, "slope": slope})

    def _validate(self) -> None:
        assert isinstance(self.parameters["line"], Line)
        # slope can be any float, including inf
        assert isinstance(self.parameters["slope"], (int, float))

    def to_string(self) -> str:
        l = self.parameters["line"]
        m = self.parameters["slope"]
        if m == float('inf'):
            return f"slope({l}) = ∞ (vertical)"
        return f"slope({l}) = {m}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["line"].point1, self.parameters["line"].point2}


class DistanceValue(Fact):
    """Distance between points P and Q equals d."""

    def __init__(self, point1: Point, point2: Point, distance: float):
        super().__init__("DistanceValue", {
            "point1": point1,
            "point2": point2,
            "distance": distance
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["point1"], Point)
        assert isinstance(self.parameters["point2"], Point)
        assert isinstance(self.parameters["distance"], (int, float))
        assert self.parameters["distance"] >= 0

    def to_string(self) -> str:
        p1 = self.parameters["point1"]
        p2 = self.parameters["point2"]
        d = self.parameters["distance"]
        return f"|{p1.name}{p2.name}| = {d}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point1"], self.parameters["point2"]}


class FunctionGraph(Fact):
    """Point (x, y) lies on function graph y = f(x) - 函数图像."""

    def __init__(self, point: Point, function_expr: str):
        """
        Args:
            point: Point on the graph
            function_expr: Function expression as string (e.g., "x^2", "2*x + 1")
        """
        super().__init__("FunctionGraph", {
            "point": point,
            "function": function_expr
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["function"], str)

    def to_string(self) -> str:
        p = self.parameters["point"]
        f = self.parameters["function"]
        return f"{p.name} on graph y = {f}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"]}


class CoordinateOrigin(Fact):
    """Point O is the origin (0, 0) of coordinate system."""

    def __init__(self, origin: Point):
        super().__init__("CoordinateOrigin", {"origin": origin})

    def _validate(self) -> None:
        assert isinstance(self.parameters["origin"], Point)

    def to_string(self) -> str:
        o = self.parameters["origin"]
        return f"{o.name} is origin (0, 0)"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["origin"]}


# ============================================================================
# DISTANCE FACTS (Week 8 Day 3 - Phase 1)
# ============================================================================

class DistanceToLine(Fact):
    """Distance from point P to line L equals value d."""

    def __init__(self, point: Point, line: Line, distance: float):
        super().__init__("DistanceToLine", {"point": point, "line": line, "distance": distance})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["line"], Line)
        assert isinstance(self.parameters["distance"], (int, float))
        assert self.parameters["distance"] >= 0

    def to_string(self) -> str:
        p = self.parameters["point"]
        l = self.parameters["line"]
        d = self.parameters["distance"]
        return f"Distance from {p.name} to {l} = {d}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["line"].point1,
                self.parameters["line"].point2}


class DistanceFromPointToLine(Fact):
    """Point P has perpendicular distance to line L (structural, without numeric value)."""

    def __init__(self, point: Point, line: Line):
        super().__init__("DistanceFromPointToLine", {"point": point, "line": line})

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["line"], Line)

    def to_string(self) -> str:
        p = self.parameters["point"]
        l = self.parameters["line"]
        return f"{p.name} has distance to {l}"

    def get_involved_points(self) -> set[Point]:
        return {self.parameters["point"], self.parameters["line"].point1,
                self.parameters["line"].point2}


class EqualDistancesToLines(Fact):
    """Two distances from point to lines are equal."""

    def __init__(self, point: Point, line1: Line, line2: Line):
        """
        Args:
            point: The point from which distances are measured
            line1: First line
            line2: Second line

        Represents: distance(point, line1) = distance(point, line2)
        """
        super().__init__("EqualDistancesToLines", {
            "point": point,
            "line1": line1,
            "line2": line2
        })

    def _validate(self) -> None:
        assert isinstance(self.parameters["point"], Point)
        assert isinstance(self.parameters["line1"], Line)
        assert isinstance(self.parameters["line2"], Line)

    def to_string(self) -> str:
        p = self.parameters["point"]
        l1 = self.parameters["line1"]
        l2 = self.parameters["line2"]
        return f"Distance from {p.name} to {l1} = distance from {p.name} to {l2}"

    def get_involved_points(self) -> set[Point]:
        pts = {self.parameters["point"]}
        pts.update({self.parameters["line1"].point1, self.parameters["line1"].point2})
        pts.update({self.parameters["line2"].point1, self.parameters["line2"].point2})
        return pts


# ============================================================================
# FACT TYPE REGISTRY
# ============================================================================

# Map fact type names to classes for dynamic instantiation
FACT_TYPES = {
    # Structural
    "On": On,
    "OnSegment": OnSegment,
    "OnCircle": OnCircle,
    "Collinear": Collinear,
    "NotCollinear": NotCollinear,
    "Between": Between,
    "Midpoint": Midpoint,
    "FootOfPerpendicular": FootOfPerpendicular,
    "ReflectPoint": ReflectPoint,
    "Intersect": Intersect,
    "Concurrent": Concurrent,

    # Length/Ratio
    "EqualSegment": EqualSegment,
    "ProportionalSegment": ProportionalSegment,
    "SegmentRatio": SegmentRatio,
    "LengthValue": LengthValue,
    "DistanceToLine": DistanceToLine,
    "DistanceFromPointToLine": DistanceFromPointToLine,
    "EqualDistancesToLines": EqualDistancesToLines,

    # Angle
    "EqualAngle": EqualAngle,
    "RightAngle": RightAngle,
    "SupplementaryAngle": SupplementaryAngle,
    "AngleSum": AngleSum,
    "AngleValue": AngleValue,
    "VerticalAngles": VerticalAngles,
    "ComplementaryAngles": ComplementaryAngles,
    "AngleBisector": AngleBisector,
    "AngleMeasure": AngleMeasure,

    # Line Relations
    "Parallel": Parallel,
    "Perpendicular": Perpendicular,
    "SameLine": SameLine,

    # Shapes
    "Triangle": Triangle,
    "IsoscelesTriangle": IsoscelesTriangle,
    "EquilateralTriangle": EquilateralTriangle,
    "SimilarTriangle": SimilarTriangle,
    "CongruentTriangle": CongruentTriangle,
    "Orthocenter": Orthocenter,
    "Centroid": Centroid,
    "Incenter": Incenter,
    "Circumcenter": Circumcenter,
    "Inside": Inside,

    # Quadrilaterals (NEW)
    "Quadrilateral": Quadrilateral,
    "Rectangle": Rectangle,
    "Square": Square,
    "Parallelogram": Parallelogram,
    "Rhombus": Rhombus,
    "Trapezoid": Trapezoid,

    # Circle
    "TangentAt": TangentAt,
    "Chord": Chord,
    "Diameter": Diameter,
    "Arc": Arc,
    "CyclicQuadrilateral": CyclicQuadrilateral,
    "InscribedAngle": InscribedAngle,
    "CentralAngle": CentralAngle,
    "InscribedCircle": InscribedCircle,
    "CircumscribedCircle": CircumscribedCircle,
    "RadiusValue": RadiusValue,

    # Area
    "AreaValue": AreaValue,
    "AreaRelation": AreaRelation,

    # Coordinate Geometry (平面直角坐标系)
    "Coordinates": Coordinates,
    "LineEquation": LineEquation,
    "Slope": Slope,
    "DistanceValue": DistanceValue,
    "FunctionGraph": FunctionGraph,
    "CoordinateOrigin": CoordinateOrigin,

    # Logic
    "Distinct": Distinct,
    "NonDegenerateTriangle": NonDegenerateTriangle,
    "Orientation": Orientation,
}


def get_fact_class(fact_type: str):
    """Get fact class by type name."""
    return FACT_TYPES.get(fact_type)
