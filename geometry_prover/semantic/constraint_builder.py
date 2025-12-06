"""
ConstraintBuilder - Converts AST constraint nodes into Facts.

The ConstraintBuilder takes constraint nodes from the AST and converts them
into Fact objects using the GeometryModel to resolve geometric objects.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 3, Task 3.2 - ConstraintBuilder Implementation
- Convert EqualConstraint → EqualSegment/EqualAngle facts
- Convert ParallelConstraint → Parallel facts
- Convert PerpendicularConstraint → Perpendicular facts
- Convert OnConstraint → On facts
"""

from typing import Optional
from geometry_prover.dsl.ast_nodes import (
    EqualConstraint, ParallelConstraint, PerpendicularConstraint,
    OnConstraint, SegmentExpr, AngleExpr, Number, Identifier
)
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.facts.fact_types import (
    EqualSegment, EqualAngle, Parallel, Perpendicular, On, OnCircle, RightAngle, Fact
)
from geometry_prover.utils.geometry_objects import Segment, Angle


class ConstraintBuilder:
    """
    Converts AST constraint nodes into Facts.

    Uses GeometryModel to resolve geometric objects and creates
    appropriate Fact instances.
    """

    def __init__(self, model: GeometryModel):
        """
        Initialize constraint builder.

        Args:
            model: GeometryModel to use for object resolution
        """
        self.model = model

    def build_constraint(self, constraint_node) -> Optional[Fact]:
        """
        Build a Fact from a constraint AST node.

        Args:
            constraint_node: AST constraint node

        Returns:
            Fact object, or None if constraint cannot be converted

        Raises:
            ValueError: If constraint is malformed or unsupported
        """
        if isinstance(constraint_node, EqualConstraint):
            return self.build_equal_constraint(constraint_node)
        elif isinstance(constraint_node, ParallelConstraint):
            return self.build_parallel_constraint(constraint_node)
        elif isinstance(constraint_node, PerpendicularConstraint):
            return self.build_perpendicular_constraint(constraint_node)
        elif isinstance(constraint_node, OnConstraint):
            return self.build_on_constraint(constraint_node)
        else:
            raise ValueError(f"Unsupported constraint type: {type(constraint_node)}")

    def build_equal_constraint(self, node: EqualConstraint) -> Fact:
        """
        Build fact from equality constraint.

        Handles:
        - Segment equality: AB = CD
        - Angle equality: angle(ABC) = angle(DEF)
        - Angle to number: angle(ABC) = 90

        Args:
            node: EqualConstraint AST node

        Returns:
            EqualSegment, EqualAngle, or RightAngle fact
        """
        left = node.left
        right = node.right

        # Segment equality: AB = CD
        if isinstance(left, SegmentExpr) and isinstance(right, SegmentExpr):
            seg1 = self._resolve_segment(left)
            seg2 = self._resolve_segment(right)
            return EqualSegment(seg1, seg2)

        # Angle equality: angle(ABC) = angle(DEF)
        elif isinstance(left, AngleExpr) and isinstance(right, AngleExpr):
            angle1 = self._resolve_angle(left)
            angle2 = self._resolve_angle(right)
            return EqualAngle(angle1, angle2)

        # Angle = 90: angle(ABC) = 90
        elif isinstance(left, AngleExpr) and isinstance(right, Number):
            angle = self._resolve_angle(left)
            value = right.value

            # Check for right angle (90 degrees)
            if value == 90.0 or value == 90:
                return RightAngle(angle)

            # For other angle values, we could create EqualAngleMeasure fact
            # For now, just create EqualAngle with a constructed angle
            # This is a simplification - in production we'd have AngleMeasure fact type
            return None  # Unsupported for now

        else:
            raise ValueError(f"Unsupported equality constraint: {type(left)} = {type(right)}")

    def build_parallel_constraint(self, node: ParallelConstraint) -> Parallel:
        """
        Build Parallel fact from parallel constraint.

        Example: AB || CD

        Args:
            node: ParallelConstraint AST node

        Returns:
            Parallel fact
        """
        # Get lines (not segments) from the segment expressions
        line1_name = node.segment1.identifier.name
        line2_name = node.segment2.identifier.name

        line1 = self.model.get_or_create_line(line1_name)
        line2 = self.model.get_or_create_line(line2_name)

        return Parallel(line1, line2)

    def build_perpendicular_constraint(self, node: PerpendicularConstraint) -> Perpendicular:
        """
        Build Perpendicular fact from perpendicular constraint.

        Example: AB ⊥ CD

        Args:
            node: PerpendicularConstraint AST node

        Returns:
            Perpendicular fact
        """
        # Get lines (not segments) from the segment expressions
        line1_name = node.segment1.identifier.name
        line2_name = node.segment2.identifier.name

        line1 = self.model.get_or_create_line(line1_name)
        line2 = self.model.get_or_create_line(line2_name)

        return Perpendicular(line1, line2)

    def build_on_constraint(self, node: OnConstraint) -> Fact:
        """
        Build On or OnCircle fact from on constraint.

        Examples:
            P on AB -> On fact
            P on circle O -> OnCircle fact

        Args:
            node: OnConstraint AST node

        Returns:
            On or OnCircle fact
        """
        # Get point
        point = self.model.get_or_create_point(node.point.name)

        # Get object from identifier - check if it's a circle
        obj_name = node.object.name

        # Check if it's a circle reference (format: "circle_O")
        if obj_name.startswith("circle_"):
            # Extract circle name
            circle_name = obj_name[7:]  # Remove "circle_" prefix
            circle = self.model.get_circle(circle_name)
            if circle is None:
                raise ValueError(f"Circle {circle_name} not found in model")
            return OnCircle(point, circle)
        else:
            # Regular line/segment
            line = self.model.get_or_create_line(obj_name)
            return On(point, line)

    # Helper methods

    def _resolve_segment(self, seg_expr: SegmentExpr) -> Segment:
        """
        Resolve segment from SegmentExpr AST node.

        Args:
            seg_expr: SegmentExpr node

        Returns:
            Segment object
        """
        seg_name = seg_expr.identifier.name
        return self.model.get_or_create_segment(seg_name)

    def _resolve_angle(self, angle_expr: AngleExpr) -> Angle:
        """
        Resolve angle from AngleExpr AST node.

        Args:
            angle_expr: AngleExpr node

        Returns:
            Angle object
        """
        angle_name = angle_expr.identifier.name
        return self.model.get_or_create_angle(angle_name)
