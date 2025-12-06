"""
Pattern matching and variable binding for theorem system.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 18 - Pattern matching and unification

This module implements:
- Pattern matching: Match patterns against concrete facts
- Variable binding: Bind pattern variables to actual objects
- Unification: Ensure consistent variable bindings across multiple patterns
"""

from typing import Dict, Any, Optional, List
from geometry_prover.theorems.pattern import Pattern, Variable
from geometry_prover.facts.fact_types import Fact


class Binding:
    """
    Represents a binding of variables to values.

    A binding maps variable names (e.g., "?A") to concrete objects
    (e.g., Point("A")).

    Example:
        binding = Binding()
        binding.bind("?A", point_a)
        binding.bind("?B", point_b)

        # Later, retrieve bindings
        point = binding.get("?A")  # Returns point_a
    """

    def __init__(self, bindings: Optional[Dict[str, Any]] = None):
        """
        Initialize binding.

        Args:
            bindings: Optional initial bindings dictionary
        """
        self.bindings: Dict[str, Any] = bindings or {}

    def bind(self, var_name: str, value: Any) -> bool:
        """
        Bind a variable to a value.

        Args:
            var_name: Variable name (e.g., "?A")
            value: Value to bind to

        Returns:
            True if binding succeeded, False if conflict
        """
        if var_name in self.bindings:
            # Variable already bound - check consistency
            return self.bindings[var_name] == value

        self.bindings[var_name] = value
        return True

    def get(self, var_name: str) -> Optional[Any]:
        """
        Get value bound to variable.

        Args:
            var_name: Variable name

        Returns:
            Bound value or None if not bound
        """
        return self.bindings.get(var_name)

    def is_bound(self, var_name: str) -> bool:
        """Check if variable is bound."""
        return var_name in self.bindings

    def copy(self) -> 'Binding':
        """Create a copy of this binding."""
        return Binding(self.bindings.copy())

    def __repr__(self) -> str:
        """String representation."""
        items = [f"{k}={v}" for k, v in self.bindings.items()]
        return f"Binding({', '.join(items)})"


class PatternMatcher:
    """
    Matches patterns against facts and produces variable bindings.

    The matcher attempts to unify a pattern (with variables) against
    a concrete fact (with actual objects), producing a binding that
    maps variables to their matched values.

    Example:
        pattern = Pattern("EqualSegment", {"segment1": "?AB", "segment2": "?CD"})
        fact = EqualSegment(segment_ab, segment_cd)

        matcher = PatternMatcher()
        binding = matcher.match(pattern, fact)

        if binding:
            print(f"?AB = {binding.get('?AB')}")  # segment_ab
            print(f"?CD = {binding.get('?CD')}")  # segment_cd
    """

    def __init__(self, auxiliary_constructor=None):
        """
        Initialize pattern matcher.

        Args:
            auxiliary_constructor: Optional AuxiliaryConstructor for handling derived_from
        """
        self.auxiliary_constructor = auxiliary_constructor

    def match(self, pattern: Pattern, fact: Fact, binding: Optional[Binding] = None) -> Optional[Binding]:
        """
        Match a pattern against a fact.

        Args:
            pattern: Pattern to match
            fact: Fact to match against
            binding: Existing binding (for multi-pattern matching)

        Returns:
            Binding if match succeeded, None if failed
        """
        # Create new binding or use existing
        result_binding = binding.copy() if binding else Binding()

        # Check fact type matches
        fact_type = type(fact).__name__
        if pattern.fact_type != fact_type:
            return None

        # Match each parameter
        for param_name, pattern_value in pattern.parameters.items():
            # Get corresponding value from fact parameters
            if param_name not in fact.parameters:
                return None

            fact_value = fact.parameters[param_name]

            # Try to match this parameter
            if not self._match_parameter(pattern_value, fact_value, result_binding):
                return None

        return result_binding

    def _match_parameter(self, pattern_value: Any, fact_value: Any, binding: Binding) -> bool:
        """
        Match a single parameter value.

        Args:
            pattern_value: Value from pattern (may be variable)
            fact_value: Value from fact (concrete object)
            binding: Current binding to update

        Returns:
            True if match succeeded, False otherwise
        """
        # Case 1: pattern_value is a Variable instance
        if isinstance(pattern_value, Variable):
            return binding.bind(pattern_value.name, fact_value)

        # Case 2: pattern_value is a string variable name (e.g., "?A")
        if isinstance(pattern_value, str) and pattern_value.startswith("?"):
            return binding.bind(pattern_value, fact_value)

        # Case 3: pattern_value is a concrete value - must match exactly
        return pattern_value == fact_value

    def match_all(self, patterns: List[Pattern], facts: List[Fact]) -> Optional[Binding]:
        """
        Match all patterns against facts with consistent bindings.

        Attempts to find a binding that satisfies all patterns against
        the given facts.

        Args:
            patterns: List of patterns to match
            facts: List of facts to match against

        Returns:
            Binding if all patterns matched, None otherwise
        """
        # Start with empty binding
        binding = Binding()
        used_fact_indices = set()  # Track which facts have been matched

        # Try to match each pattern
        for pattern in patterns:
            matched = False

            # Try each fact
            for i, fact in enumerate(facts):
                # Skip facts that have already been matched
                if i in used_fact_indices:
                    continue

                result = self.match(pattern, fact, binding)
                if result:
                    binding = result
                    used_fact_indices.add(i)  # Mark this fact as used
                    matched = True
                    break

            # If any pattern failed to match, return None
            if not matched:
                return None

        return binding

    def match_all_with_facts(
        self,
        patterns: List[Pattern],
        facts: List[Fact],
        theorem=None
    ) -> Optional[tuple[Binding, List[Fact]]]:
        """
        Match all patterns against facts and return binding with matched facts.

        Args:
            patterns: List of patterns to match
            facts: List of facts to match against
            theorem: Optional theorem for auxiliary construction via derived_from

        Returns:
            Tuple of (binding, matched_facts) if successful, None otherwise
        """
        binding = Binding()
        matched_facts = []
        used_fact_indices = set()  # Track which facts have been matched

        # Try to match each pattern
        for pattern in patterns:
            matched = False

            # Try each fact
            for i, fact in enumerate(facts):
                # Skip facts that have already been matched
                if i in used_fact_indices:
                    continue

                result = self.match(pattern, fact, binding)
                if result:
                    binding = result
                    matched_facts.append(fact)
                    used_fact_indices.add(i)  # Mark this fact as used
                    matched = True
                    break

            # If any pattern failed to match, return None
            if not matched:
                return None

        # AUGMENT BINDING with auxiliary construction
        if self.auxiliary_constructor and theorem:
            binding = self.auxiliary_constructor.augment_binding(binding, theorem)

        return (binding, matched_facts)

    def match_all_bindings(self, patterns: List[Pattern], facts: List[Fact]) -> List[Binding]:
        """
        Find ALL possible bindings that satisfy all patterns.

        This explores all possible ways to match patterns against facts,
        returning all valid bindings. This is more expensive than match_all
        but ensures we don't miss valid theorem applications.

        Args:
            patterns: List of patterns to match
            facts: List of facts to match against

        Returns:
            List of all valid bindings (may be empty)
        """
        if not patterns:
            return [Binding()]

        # Recursively find all bindings, passing empty set of used indices
        return self._match_patterns_recursive(patterns, facts, Binding(), set())

    def match_all_bindings_with_facts(
        self,
        patterns: List[Pattern],
        facts: List[Fact],
        theorem=None
    ) -> List[tuple[Binding, List[Fact]]]:
        """
        Find ALL possible bindings with matched facts.

        Args:
            patterns: List of patterns to match
            facts: List of facts to match against
            theorem: Optional theorem for auxiliary construction via derived_from

        Returns:
            List of (binding, matched_facts) tuples
        """
        if not patterns:
            return [(Binding(), [])]

        # Recursively find all bindings with facts, passing empty set of used indices
        results = self._match_patterns_recursive_with_facts(patterns, facts, Binding(), [], set())

        # AUGMENT BINDINGS with auxiliary construction
        if self.auxiliary_constructor and theorem:
            augmented_results = []
            for binding, matched_facts in results:
                augmented_binding = self.auxiliary_constructor.augment_binding(binding, theorem)
                augmented_results.append((augmented_binding, matched_facts))
            return augmented_results

        return results

    def _match_patterns_recursive(
        self,
        remaining_patterns: List[Pattern],
        facts: List[Fact],
        current_binding: Binding,
        used_fact_indices: set
    ) -> List[Binding]:
        """
        Recursively match patterns against facts to find all bindings.

        Args:
            remaining_patterns: Patterns left to match
            facts: Facts to match against
            current_binding: Binding accumulated so far
            used_fact_indices: Set of fact indices already used

        Returns:
            List of all valid complete bindings
        """
        # Base case: no more patterns to match
        if not remaining_patterns:
            return [current_binding]

        # Get next pattern to match
        pattern = remaining_patterns[0]
        rest_patterns = remaining_patterns[1:]

        all_bindings = []

        # Try matching this pattern against each fact
        for i, fact in enumerate(facts):
            # Skip facts that have already been matched in this branch
            if i in used_fact_indices:
                continue

            result = self.match(pattern, fact, current_binding)
            if result:
                # This fact matches - recurse with remaining patterns
                new_used_indices = used_fact_indices | {i}  # Add this index to used set
                bindings = self._match_patterns_recursive(rest_patterns, facts, result, new_used_indices)
                all_bindings.extend(bindings)

        return all_bindings

    def _match_patterns_recursive_with_facts(
        self,
        remaining_patterns: List[Pattern],
        facts: List[Fact],
        current_binding: Binding,
        current_matched_facts: List[Fact],
        used_fact_indices: set
    ) -> List[tuple[Binding, List[Fact]]]:
        """
        Recursively match patterns against facts, tracking matched facts.

        Args:
            remaining_patterns: Patterns left to match
            facts: Facts to match against
            current_binding: Binding accumulated so far
            current_matched_facts: Facts matched so far
            used_fact_indices: Set of fact indices already used

        Returns:
            List of (binding, matched_facts) tuples
        """
        # Base case: no more patterns to match
        if not remaining_patterns:
            return [(current_binding, current_matched_facts)]

        # Get next pattern to match
        pattern = remaining_patterns[0]
        rest_patterns = remaining_patterns[1:]

        all_results = []

        # Try matching this pattern against each fact
        for i, fact in enumerate(facts):
            # Skip facts that have already been matched in this branch
            if i in used_fact_indices:
                continue

            result = self.match(pattern, fact, current_binding)
            if result:
                # This fact matches - recurse with remaining patterns
                new_matched = current_matched_facts + [fact]
                new_used_indices = used_fact_indices | {i}  # Add this index to used set
                results = self._match_patterns_recursive_with_facts(
                    rest_patterns, facts, result, new_matched, new_used_indices
                )
                all_results.extend(results)

        return all_results


class Unifier:
    """
    Performs unification and substitution of variables.

    Unification ensures that variable bindings are consistent across
    multiple patterns and can substitute variables with their bound values.
    """

    def substitute(self, pattern: Pattern, binding: Binding) -> Pattern:
        """
        Substitute variables in pattern with their bound values.

        Args:
            pattern: Pattern with variables
            binding: Variable bindings

        Returns:
            New pattern with variables replaced by bound values
        """
        new_params = {}

        for param_name, param_value in pattern.parameters.items():
            # If it's a variable, substitute it
            if isinstance(param_value, Variable):
                bound_value = binding.get(param_value.name)
                new_params[param_name] = bound_value if bound_value is not None else param_value
            elif isinstance(param_value, str) and param_value.startswith("?"):
                bound_value = binding.get(param_value)
                new_params[param_name] = bound_value if bound_value is not None else param_value
            else:
                new_params[param_name] = param_value

        return Pattern(pattern.fact_type, new_params)

    def is_ground(self, pattern: Pattern) -> bool:
        """
        Check if pattern is ground (no unbound variables).

        Args:
            pattern: Pattern to check

        Returns:
            True if pattern has no variables, False otherwise
        """
        for value in pattern.parameters.values():
            if isinstance(value, Variable):
                return False
            if isinstance(value, str) and value.startswith("?"):
                return False

        return True
