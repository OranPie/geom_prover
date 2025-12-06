"""
Theorem application - apply theorems to derive new facts.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 18 - Theorem application engine

This module implements theorem application logic that:
- Matches theorem conditions against available facts
- Produces new facts based on theorem conclusions
- Manages bindings across multiple conditions
"""

from typing import List, Optional
from geometry_prover.theorems.theorem import Theorem
from geometry_prover.theorems.matcher import PatternMatcher, Unifier, Binding
from geometry_prover.theorems.pattern import Pattern
from geometry_prover.facts.fact_types import Fact


class TheoremApplication:
    """
    Result of applying a theorem.

    Contains the binding that satisfied the theorem conditions,
    the facts that were matched, and the new facts derived.
    """

    def __init__(self, theorem: Theorem, binding: Binding, derived_facts: List[Fact], matched_facts: Optional[List[Fact]] = None):
        """
        Initialize theorem application result.

        Args:
            theorem: The theorem that was applied
            binding: Variable binding that satisfied conditions
            derived_facts: New facts derived from conclusions
            matched_facts: Facts that matched the theorem conditions (premises)
        """
        self.theorem = theorem
        self.binding = binding
        self.derived_facts = derived_facts
        self.matched_facts = matched_facts or []

    def __repr__(self) -> str:
        return (
            f"TheoremApplication(theorem={self.theorem.metadata.name}, "
            f"facts={len(self.derived_facts)}, premises={len(self.matched_facts)})"
        )


class TheoremApplicator:
    """
    Applies theorems to derive new facts.

    The applicator:
    1. Matches theorem conditions against available facts
    2. If all conditions match, instantiates conclusion patterns
    3. Converts instantiated patterns to concrete facts
    """

    def __init__(self):
        self.matcher = PatternMatcher()
        self.unifier = Unifier()

    def apply(self, theorem: Theorem, facts: List[Fact]) -> Optional[TheoremApplication]:
        """
        Apply theorem to derive new facts.

        Args:
            theorem: Theorem to apply
            facts: Available facts to match against

        Returns:
            TheoremApplication if theorem was applicable, None otherwise
        """
        # Try to match all conditions and get matched facts (pass theorem for auxiliary construction)
        match_result = self.matcher.match_all_with_facts(theorem.conditions, facts, theorem)

        if match_result is None:
            # Conditions not satisfied
            return None

        binding, matched_facts = match_result

        # Check constraints
        if not self._check_constraints(theorem, binding):
            return None

        # Conditions satisfied - instantiate conclusions
        derived_facts = []

        for conclusion_pattern in theorem.conclusions:
            # Substitute variables in conclusion
            instantiated = self.unifier.substitute(conclusion_pattern, binding)

            # Convert pattern to fact
            fact = self._pattern_to_fact(instantiated)
            if fact:
                derived_facts.append(fact)

        # If no facts could be derived, theorem doesn't apply
        if not derived_facts:
            return None

        return TheoremApplication(theorem, binding, derived_facts, matched_facts)

    def _check_constraints(self, theorem: Theorem, binding: Binding) -> bool:
        """
        Check if all constraints are satisfied for the given binding.

        Args:
            theorem: Theorem with constraints
            binding: Variable binding to check

        Returns:
            True if all constraints are satisfied, False otherwise
        """
        for constraint in theorem.constraints:
            if not self._evaluate_constraint(constraint, binding):
                return False
        return True

    def _evaluate_constraint(self, constraint, binding: Binding) -> bool:
        """
        Evaluate a single constraint against a binding.

        Args:
            constraint: Constraint to evaluate
            binding: Variable binding

        Returns:
            True if constraint is satisfied, False otherwise
        """
        constraint_type = constraint.constraint_type
        params = constraint.parameters

        if constraint_type == "not_equal":
            # Two variables must not be equal
            var1 = params.get("var1")
            var2 = params.get("var2")
            if var1 and var2:
                val1 = binding.get(var1)
                val2 = binding.get(var2)
                # If both are bound, check they're not equal
                if val1 is not None and val2 is not None:
                    return val1 != val2
            return True  # If not both bound, constraint doesn't apply

        elif constraint_type == "distinct":
            # All specified variables must have different values
            vars_list = params.get("vars", [])
            values = []
            for var in vars_list:
                val = binding.get(var)
                if val is not None:
                    values.append(val)
            # Check that all values are distinct
            return len(values) == len(set(values))

        # Unknown constraint type - treat as satisfied
        return True

    def _pattern_to_fact(self, pattern: Pattern) -> Optional[Fact]:
        """
        Convert an instantiated (ground) pattern to a concrete fact.

        Args:
            pattern: Pattern with all variables bound

        Returns:
            Fact instance or None if pattern is not ground
        """
        # Check that pattern is ground (no unbound variables)
        if not self.unifier.is_ground(pattern):
            return None

        # Import fact classes dynamically
        from geometry_prover.facts import fact_types

        # Get the fact class by name
        fact_class_name = pattern.fact_type
        if not hasattr(fact_types, fact_class_name):
            raise ValueError(f"Unknown fact type: {fact_class_name}")

        fact_class = getattr(fact_types, fact_class_name)

        # Create fact instance
        # Extract parameter values in the order expected by the constructor
        params = list(pattern.parameters.values())
        return fact_class(*params)

    def apply_all(self, theorems: List[Theorem], facts: List[Fact]) -> List[TheoremApplication]:
        """
        Apply all applicable theorems to facts.

        Args:
            theorems: List of theorems to try
            facts: Available facts

        Returns:
            List of successful theorem applications
        """
        applications = []

        for theorem in theorems:
            result = self.apply(theorem, facts)
            if result:
                applications.append(result)

        return applications

    def apply_with_all_bindings(self, theorem: Theorem, facts: List[Fact]) -> List[TheoremApplication]:
        """
        Apply theorem with ALL possible bindings.

        This finds all possible ways to match the theorem conditions against
        the facts, and derives facts for each valid binding. This ensures we
        don't miss valid applications due to fact ordering.

        Args:
            theorem: Theorem to apply
            facts: Available facts to match against

        Returns:
            List of all valid theorem applications (may be empty)
        """
        # Find all possible bindings with matched facts (pass theorem for auxiliary construction)
        binding_results = self.matcher.match_all_bindings_with_facts(theorem.conditions, facts, theorem)

        if not binding_results:
            return []

        applications = []

        for binding, matched_facts in binding_results:
            # Check constraints
            if not self._check_constraints(theorem, binding):
                continue

            # Instantiate conclusions with this binding
            derived_facts = []

            for conclusion_pattern in theorem.conclusions:
                # Substitute variables in conclusion
                instantiated = self.unifier.substitute(conclusion_pattern, binding)

                # Convert pattern to fact
                fact = self._pattern_to_fact(instantiated)
                if fact:
                    derived_facts.append(fact)

            # If we derived facts, create application
            if derived_facts:
                applications.append(TheoremApplication(theorem, binding, derived_facts, matched_facts))

        return applications
