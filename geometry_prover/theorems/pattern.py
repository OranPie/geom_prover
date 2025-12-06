"""
Pattern matching data structures for theorem system.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 16-17 - Pattern and Variable classes for theorem matching

Patterns represent fact templates with variables (e.g., ?A, ?B) that can be
matched against concrete facts. Variables bind to actual geometric objects
during the matching process.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    """
    Represents a pattern variable in a theorem.

    Variables use the ? prefix (e.g., ?A, ?ABC) and can bind to
    geometric objects during pattern matching.

    Examples:
        ?A - point variable
        ?ABC - angle variable
        ?AB - segment variable

    Attributes:
        name: Variable name (e.g., "?A")
        type: Expected type ("point", "segment", "angle", "line", "circle", "triangle")
        description: Optional human-readable description
        derived_from: Optional list of component variable names (e.g., ["?A", "?B"] for a line)
    """
    name: str
    type: str
    description: str = ""
    derived_from: Optional[List[str]] = None

    def __post_init__(self):
        """Validate variable after initialization."""
        if not self.name.startswith("?"):
            raise ValueError(f"Variable name must start with ?: {self.name}")

        valid_types = {"point", "segment", "angle", "line", "circle", "triangle", "any"}
        if self.type not in valid_types:
            raise ValueError(f"Invalid variable type: {self.type}. Must be one of {valid_types}")

    def matches_type(self, obj: Any) -> bool:
        """
        Check if object type matches this variable's expected type.

        Args:
            obj: Object to check

        Returns:
            True if object type matches, False otherwise
        """
        if self.type == "any":
            return True

        # Check object type by class name
        obj_type = type(obj).__name__.lower()
        return obj_type == self.type


class Pattern:
    """
    Represents a fact pattern with variables.

    Patterns are templates for facts that can contain variables.
    During matching, variables are bound to actual objects.

    Examples:
        EqualSegment(?AB, ?CD) - matches any EqualSegment fact
        RightAngle(?ABC) - matches any RightAngle fact
        On(?P, ?AB) - matches point on line facts

    Attributes:
        fact_type: Type of fact (e.g., "EqualSegment", "RightAngle")
        parameters: Dictionary of parameter names to values (variables or constants)
    """

    def __init__(self, fact_type: str, parameters: Dict[str, Any]):
        """
        Initialize pattern.

        Args:
            fact_type: Name of the fact type (e.g., "EqualSegment")
            parameters: Parameter names to values (can include Variable instances)
        """
        self.fact_type = fact_type
        self.parameters = parameters

    def get_variables(self) -> List[Variable]:
        """
        Extract all variables from this pattern.

        Returns:
            List of Variable instances in the pattern
        """
        variables = []
        for value in self.parameters.values():
            if isinstance(value, Variable):
                variables.append(value)
            elif isinstance(value, str) and value.startswith("?"):
                # String representation of variable - should be converted to Variable
                # This is for backward compatibility
                pass
        return variables

    def has_variables(self) -> bool:
        """Check if pattern contains any variables."""
        return len(self.get_variables()) > 0

    def __repr__(self) -> str:
        """String representation for debugging."""
        params_str = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        return f"Pattern({self.fact_type}({params_str}))"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, Pattern):
            return False
        return (self.fact_type == other.fact_type and
                self.parameters == other.parameters)

    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""
        # Convert parameters dict to hashable tuple
        param_items = tuple(sorted(
            (k, v if not isinstance(v, (list, dict)) else str(v))
            for k, v in self.parameters.items()
        ))
        return hash((self.fact_type, param_items))


class PatternTemplate:
    """
    Template for creating patterns from string representations.

    Provides convenient constructors for common pattern types.
    """

    @staticmethod
    def equal_segment(seg1: str, seg2: str) -> Pattern:
        """Create EqualSegment pattern."""
        return Pattern("EqualSegment", {
            "segment1": seg1,
            "segment2": seg2
        })

    @staticmethod
    def equal_angle(angle1: str, angle2: str) -> Pattern:
        """Create EqualAngle pattern."""
        return Pattern("EqualAngle", {
            "angle1": angle1,
            "angle2": angle2
        })

    @staticmethod
    def right_angle(angle: str) -> Pattern:
        """Create RightAngle pattern."""
        return Pattern("RightAngle", {
            "angle": angle
        })

    @staticmethod
    def parallel(line1: str, line2: str) -> Pattern:
        """Create Parallel pattern."""
        return Pattern("Parallel", {
            "line1": line1,
            "line2": line2
        })

    @staticmethod
    def perpendicular(line1: str, line2: str) -> Pattern:
        """Create Perpendicular pattern."""
        return Pattern("Perpendicular", {
            "line1": line1,
            "line2": line2
        })

    @staticmethod
    def on_point(point: str, line: str) -> Pattern:
        """Create On (point on line) pattern."""
        return Pattern("On", {
            "point": point,
            "line": line
        })

    @staticmethod
    def on_circle(point: str, circle: str) -> Pattern:
        """Create OnCircle pattern."""
        return Pattern("OnCircle", {
            "point": point,
            "circle": circle
        })
