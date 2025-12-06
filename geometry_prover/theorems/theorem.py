"""
Theorem representation for geometric reasoning.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 16-17 - Theorem class for representing geometric theorems

Theorems consist of:
- Conditions (patterns that must match)
- Conclusions (patterns that can be derived)
- Variables (pattern variables used in conditions and conclusions)
- Metadata (name, category, description)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from geometry_prover.theorems.pattern import Pattern, Variable
from geometry_prover.facts.fact_types import Fact


@dataclass
class Constraint:
    """
    Constraint that must be satisfied for theorem application.

    Types of constraints:
    - not_equal: Two bound variables must not be equal
    - distinct_points: A set of points must all be different
    - distinct_objects: A set of objects must all be different
    """
    constraint_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TheoremMetadata:
    """
    Metadata for a theorem.

    Attributes:
        name: Unique identifier for the theorem
        category: Category (e.g., "triangle_properties", "angle_properties")
        description: Human-readable description
        references: Optional list of references (textbooks, papers, etc.)
    """
    name: str
    category: str
    description: str
    references: List[str] = field(default_factory=list)


class Theorem:
    """
    Represents a geometric theorem.

    A theorem consists of:
    - Conditions: Patterns that must be matched in the facts
    - Conclusions: Patterns that can be derived when conditions are met
    - Variables: Pattern variables used in the theorem
    - Metadata: Name, category, description

    Example (Isosceles Triangle Base Angles):
        Conditions: EqualSegment(?AB, ?AC)
        Conclusions: EqualAngle(?ABC, ?ACB)
        Variables: ?A, ?B, ?C (points), ?AB, ?AC (segments), ?ABC, ?ACB (angles)

    The theorem can be applied when all condition patterns are matched
    against available facts, producing new facts based on conclusion patterns.
    """

    def __init__(
        self,
        metadata: TheoremMetadata,
        conditions: List[Pattern],
        conclusions: List[Pattern],
        variables: List[Variable],
        constraints: Optional[List[Constraint]] = None
    ):
        """
        Initialize theorem.

        Args:
            metadata: Theorem metadata (name, category, etc.)
            conditions: List of condition patterns (all must match)
            conclusions: List of conclusion patterns (derived facts)
            variables: List of variables used in patterns
            constraints: Optional list of constraints that must be satisfied

        Raises:
            ValueError: If theorem is malformed
        """
        self.metadata = metadata
        self.conditions = conditions
        self.conclusions = conclusions
        self.variables = variables
        self.constraints = constraints or []

        # Validate theorem
        self._validate()

    def _validate(self) -> None:
        """
        Validate theorem structure.

        Checks:
        - At least one condition and one conclusion
        - All variables in patterns are declared
        - No circular dependencies
        """
        if not self.conditions:
            raise ValueError(f"Theorem {self.metadata.name} has no conditions")

        if not self.conclusions:
            raise ValueError(f"Theorem {self.metadata.name} has no conclusions")

        # Collect all variable names
        declared_vars = {var.name for var in self.variables}

        # Check that all pattern variables are declared
        for pattern in self.conditions + self.conclusions:
            pattern_vars = self._extract_variable_names(pattern)
            undeclared = pattern_vars - declared_vars
            if undeclared:
                raise ValueError(
                    f"Theorem {self.metadata.name} uses undeclared variables: {undeclared}"
                )

    def _extract_variable_names(self, pattern: Pattern) -> set:
        """Extract variable names from a pattern."""
        var_names = set()
        for value in pattern.parameters.values():
            if isinstance(value, Variable):
                var_names.add(value.name)
            elif isinstance(value, str) and value.startswith("?"):
                var_names.add(value)
        return var_names

    def get_variable(self, name: str) -> Optional[Variable]:
        """
        Get variable by name.

        Args:
            name: Variable name (e.g., "?A")

        Returns:
            Variable instance or None if not found
        """
        for var in self.variables:
            if var.name == name:
                return var
        return None

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"Theorem(name={self.metadata.name}, "
            f"conditions={len(self.conditions)}, "
            f"conclusions={len(self.conclusions)}, "
            f"variables={len(self.variables)})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [
            f"Theorem: {self.metadata.name}",
            f"Category: {self.metadata.category}",
            f"Description: {self.metadata.description}",
            "",
            "Conditions:",
        ]

        for i, cond in enumerate(self.conditions, 1):
            lines.append(f"  {i}. {cond}")

        lines.append("")
        lines.append("Conclusions:")

        for i, concl in enumerate(self.conclusions, 1):
            lines.append(f"  {i}. {concl}")

        if self.variables:
            lines.append("")
            lines.append("Variables:")
            for var in self.variables:
                desc = f" - {var.description}" if var.description else ""
                lines.append(f"  {var.name}: {var.type}{desc}")

        return "\n".join(lines)


class TheoremBuilder:
    """
    Builder for constructing theorems programmatically.

    Provides a fluent interface for creating theorems without
    directly instantiating the Theorem class.

    Example:
        theorem = (TheoremBuilder("isosceles_base_angles")
                   .category("triangle_properties")
                   .description("Base angles of isosceles triangle are equal")
                   .add_variable(Variable("?A", "point"))
                   .add_variable(Variable("?B", "point"))
                   .add_variable(Variable("?C", "point"))
                   .add_condition(Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?AC"}))
                   .add_conclusion(Pattern("EqualAngle", {"angle1": "?ABC", "angle2": "?ACB"}))
                   .build())
    """

    def __init__(self, name: str):
        """Initialize builder with theorem name."""
        self.name = name
        self._category = ""
        self._description = ""
        self._references: List[str] = []
        self._conditions: List[Pattern] = []
        self._conclusions: List[Pattern] = []
        self._variables: List[Variable] = []
        self._constraints: List[Constraint] = []

    def category(self, category: str) -> 'TheoremBuilder':
        """Set theorem category."""
        self._category = category
        return self

    def description(self, description: str) -> 'TheoremBuilder':
        """Set theorem description."""
        self._description = description
        return self

    def add_reference(self, reference: str) -> 'TheoremBuilder':
        """Add a reference."""
        self._references.append(reference)
        return self

    def add_variable(self, variable: Variable) -> 'TheoremBuilder':
        """Add a variable."""
        self._variables.append(variable)
        return self

    def add_condition(self, pattern: Pattern) -> 'TheoremBuilder':
        """Add a condition pattern."""
        self._conditions.append(pattern)
        return self

    def add_conclusion(self, pattern: Pattern) -> 'TheoremBuilder':
        """Add a conclusion pattern."""
        self._conclusions.append(pattern)
        return self

    def add_constraint(self, constraint: Constraint) -> 'TheoremBuilder':
        """Add a constraint."""
        self._constraints.append(constraint)
        return self

    def build(self) -> Theorem:
        """
        Build the theorem.

        Returns:
            Constructed Theorem instance

        Raises:
            ValueError: If theorem is invalid
        """
        metadata = TheoremMetadata(
            name=self.name,
            category=self._category or "uncategorized",
            description=self._description or "No description",
            references=self._references
        )

        return Theorem(
            metadata=metadata,
            conditions=self._conditions,
            conclusions=self._conclusions,
            variables=self._variables,
            constraints=self._constraints
        )
