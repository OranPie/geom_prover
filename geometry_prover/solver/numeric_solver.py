"""
Numeric constraint solver for angle and length computation.

This module implements a constraint propagation solver that derives numeric
values for angles and lengths from geometric facts. It handles:

Angle Constraints:
- Triangle angle sum: ∠A + ∠B + ∠C = 180°
- Supplementary angles: ∠A + ∠B = 180°
- Complementary angles: ∠A + ∠B = 90°
- Right angles: ∠A = 90°
- Vertical angles: ∠A = ∠B
- Equal angles: ∠A = ∠B
- Angle bisector: ∠BAD = ∠DAC = ∠BAC/2

Length Constraints:
- Equal segments: |AB| = |CD|
- Length values: |AB| = value

The solver uses iterative constraint propagation to derive as many numeric
values as possible from the given facts.
"""

from typing import Dict, List, Optional, Tuple, Callable
from geometry_prover.facts.fact_types import Fact
from geometry_prover.utils.geometry_objects import Point, Angle, Line


class NumericSolver:
    """Constraint propagation solver for numeric values."""

    def __init__(self):
        """Initialize empty solver state."""
        self.angle_values: Dict[str, float] = {}
        self.length_values: Dict[str, float] = {}
        self.constraints: List[Tuple[str, Callable[[], bool]]] = []

    def solve(self, facts: List[Fact], max_iterations: int = 20) -> Dict[str, any]:
        """
        Derive all computable numeric values from facts.

        Args:
            facts: List of geometric facts
            max_iterations: Maximum number of constraint propagation iterations

        Returns:
            Dictionary with 'angles' and 'lengths' subdicts containing
            derived numeric values
        """
        # Reset state
        self.angle_values = {}
        self.length_values = {}
        self.constraints = []

        # Extract constraints from facts
        self._extract_from_facts(facts)

        # Iterative constraint propagation
        changed = True
        iteration = 0
        while changed and iteration < max_iterations:
            changed = self._propagate_constraints()
            iteration += 1

        return {
            'angles': self.angle_values,
            'lengths': self.length_values,
            'iterations': iteration
        }

    def _extract_from_facts(self, facts: List[Fact]) -> None:
        """Extract numeric constraints from geometric facts."""
        for fact in facts:
            fact_type = fact.fact_type

            if fact_type == "AngleMeasure":
                # Direct angle measurement
                angle = fact.parameters["angle"]
                measure = fact.parameters["measure"]
                key = self._angle_key(angle)
                self.angle_values[key] = measure

            elif fact_type == "AngleValue":
                # Alternative angle value fact
                angle = fact.parameters["angle"]
                value = fact.parameters["value"]
                key = self._angle_key(angle)
                self.angle_values[key] = value

            elif fact_type == "RightAngle":
                # Right angle = 90°
                angle = fact.parameters["angle"]
                key = self._angle_key(angle)
                self.angle_values[key] = 90.0

            elif fact_type == "Triangle":
                # Triangle angle sum constraint
                p1, p2, p3 = [fact.parameters[f"p{i}"] for i in range(1, 4)]
                self._add_triangle_angle_sum(p1, p2, p3)

            elif fact_type == "SupplementaryAngle":
                # Supplementary angles sum to 180°
                a1, a2 = fact.parameters["angle1"], fact.parameters["angle2"]
                self._add_supplementary_constraint(a1, a2)

            elif fact_type == "ComplementaryAngles":
                # Complementary angles sum to 90°
                a1, a2 = fact.parameters["angle1"], fact.parameters["angle2"]
                self._add_complementary_constraint(a1, a2)

            elif fact_type == "VerticalAngles":
                # Vertical angles are equal
                a1, a2 = fact.parameters["angle1"], fact.parameters["angle2"]
                self._add_equal_angles_constraint(a1, a2)

            elif fact_type == "EqualAngle":
                # Equal angles constraint
                a1, a2 = fact.parameters["angle1"], fact.parameters["angle2"]
                self._add_equal_angles_constraint(a1, a2)

            elif fact_type == "AngleBisector":
                # Angle bisector divides angle in half
                vertex = fact.parameters["vertex"]
                ray1 = fact.parameters["ray1"]
                ray2 = fact.parameters["ray2"]
                bisector = fact.parameters["bisector"]
                self._add_angle_bisector_constraint(vertex, ray1, ray2, bisector)

            elif fact_type == "LengthValue":
                # Direct length measurement
                segment = fact.parameters["segment"]
                value = fact.parameters["value"]
                key = self._segment_key(segment)
                self.length_values[key] = value

            elif fact_type == "EqualSegment":
                # Equal segments constraint
                s1, s2 = fact.parameters["segment1"], fact.parameters["segment2"]
                self._add_equal_segments_constraint(s1, s2)

    def _add_triangle_angle_sum(self, p1: Point, p2: Point, p3: Point) -> None:
        """
        Add constraint: ∠p1 + ∠p2 + ∠p3 = 180°

        For triangle with vertices p1, p2, p3, the sum of interior angles is 180°.
        """
        # Angle at p1: angle p2-p1-p3
        angle1_key = f"{p2.name}{p1.name}{p3.name}"
        # Angle at p2: angle p1-p2-p3
        angle2_key = f"{p1.name}{p2.name}{p3.name}"
        # Angle at p3: angle p1-p3-p2
        angle3_key = f"{p1.name}{p3.name}{p2.name}"

        def constraint() -> bool:
            angles = [angle1_key, angle2_key, angle3_key]
            known = [a for a in angles if a in self.angle_values]
            unknown = [a for a in angles if a not in self.angle_values]

            # If we know 2 angles, we can compute the third
            if len(known) == 2 and len(unknown) == 1:
                sum_known = sum(self.angle_values[a] for a in known)
                self.angle_values[unknown[0]] = 180.0 - sum_known
                return True
            return False

        self.constraints.append((f"Triangle angle sum ({p1.name},{p2.name},{p3.name})", constraint))

    def _add_supplementary_constraint(self, a1: Angle, a2: Angle) -> None:
        """
        Add constraint: ∠a1 + ∠a2 = 180°

        Supplementary angles sum to 180 degrees.
        """
        k1, k2 = self._angle_key(a1), self._angle_key(a2)

        def constraint() -> bool:
            if k1 in self.angle_values and k2 not in self.angle_values:
                self.angle_values[k2] = 180.0 - self.angle_values[k1]
                return True
            elif k2 in self.angle_values and k1 not in self.angle_values:
                self.angle_values[k1] = 180.0 - self.angle_values[k2]
                return True
            return False

        self.constraints.append((f"Supplementary angles", constraint))

    def _add_complementary_constraint(self, a1: Angle, a2: Angle) -> None:
        """
        Add constraint: ∠a1 + ∠a2 = 90°

        Complementary angles sum to 90 degrees.
        """
        k1, k2 = self._angle_key(a1), self._angle_key(a2)

        def constraint() -> bool:
            if k1 in self.angle_values and k2 not in self.angle_values:
                self.angle_values[k2] = 90.0 - self.angle_values[k1]
                return True
            elif k2 in self.angle_values and k1 not in self.angle_values:
                self.angle_values[k1] = 90.0 - self.angle_values[k2]
                return True
            return False

        self.constraints.append((f"Complementary angles", constraint))

    def _add_equal_angles_constraint(self, a1: Angle, a2: Angle) -> None:
        """
        Add constraint: ∠a1 = ∠a2

        Used for vertical angles, equal angles from congruent triangles, etc.
        """
        k1, k2 = self._angle_key(a1), self._angle_key(a2)

        def constraint() -> bool:
            changed = False
            if k1 in self.angle_values and k2 not in self.angle_values:
                self.angle_values[k2] = self.angle_values[k1]
                changed = True
            elif k2 in self.angle_values and k1 not in self.angle_values:
                self.angle_values[k1] = self.angle_values[k2]
                changed = True
            return changed

        self.constraints.append((f"Equal angles", constraint))

    def _add_angle_bisector_constraint(self, vertex: Point, ray1: Point,
                                       ray2: Point, bisector: Line) -> None:
        """
        Add constraint for angle bisector.

        If bisector divides angle at vertex between ray1 and ray2,
        then each half angle = full angle / 2.
        """
        full_angle = f"{ray1.name}{vertex.name}{ray2.name}"
        bisector_pt = bisector.point2
        half1 = f"{ray1.name}{vertex.name}{bisector_pt.name}"
        half2 = f"{bisector_pt.name}{vertex.name}{ray2.name}"

        def constraint() -> bool:
            changed = False

            # If we know full angle, compute halves
            if full_angle in self.angle_values:
                half_measure = self.angle_values[full_angle] / 2.0
                if half1 not in self.angle_values:
                    self.angle_values[half1] = half_measure
                    changed = True
                if half2 not in self.angle_values:
                    self.angle_values[half2] = half_measure
                    changed = True

            # If we know both halves, compute full angle
            elif half1 in self.angle_values and half2 in self.angle_values:
                total = self.angle_values[half1] + self.angle_values[half2]
                if full_angle not in self.angle_values:
                    self.angle_values[full_angle] = total
                    changed = True

            return changed

        self.constraints.append((f"Angle bisector at {vertex.name}", constraint))

    def _add_equal_segments_constraint(self, s1, s2) -> None:
        """
        Add constraint: |s1| = |s2|

        Equal segment lengths.
        """
        k1, k2 = self._segment_key(s1), self._segment_key(s2)

        def constraint() -> bool:
            changed = False
            if k1 in self.length_values and k2 not in self.length_values:
                self.length_values[k2] = self.length_values[k1]
                changed = True
            elif k2 in self.length_values and k1 not in self.length_values:
                self.length_values[k1] = self.length_values[k2]
                changed = True
            return changed

        self.constraints.append((f"Equal segments", constraint))

    def _propagate_constraints(self) -> bool:
        """
        Apply all constraints once.

        Returns:
            True if any constraint propagated new values, False otherwise
        """
        changed = False
        for description, constraint_fn in self.constraints:
            try:
                if constraint_fn():
                    changed = True
            except Exception as e:
                # Skip constraints that fail (e.g., missing data)
                pass
        return changed

    def _angle_key(self, angle: Angle) -> str:
        """Create unique string key for an angle."""
        return f"{angle.point1.name}{angle.vertex.name}{angle.point2.name}"

    def _segment_key(self, segment) -> str:
        """Create unique string key for a segment."""
        if hasattr(segment, 'point1') and hasattr(segment, 'point2'):
            # Normalize segment key (AB == BA)
            p1, p2 = segment.point1.name, segment.point2.name
            return f"{min(p1, p2)}{max(p1, p2)}"
        return str(segment)
