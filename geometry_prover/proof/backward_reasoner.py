"""
Backward reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 6 - Backward Reasoning (Goal-Directed Search)

This module provides a backward reasoning engine that starts with goals
and works backwards to find proofs. It uses the proof infrastructure
(ProofState, ProofTree, SearchStrategy) and theorem system (TheoremEngine)
to perform goal-directed proof search.
"""

from typing import List, Optional, Set
import time
from collections import deque

from geometry_prover.facts.fact_types import Fact
from geometry_prover.theorems.theorem import Theorem
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.theorems.matcher import PatternMatcher, Unifier
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.proof.proof_result import ProofResult
from geometry_prover.proof.search_strategy import SearchStrategy, BreadthFirstStrategy


class BackwardReasoner:
    """
    Backward reasoning engine for goal-directed proof search.

    The backward reasoner:
    - Starts with goals to prove
    - Works backwards to find theorems that could prove them
    - Recursively proves sub-goals
    - Uses known facts as base cases
    - Tracks proof history in proof tree
    - Respects depth and iteration limits

    Example:
        reasoner = BackwardReasoner(theorem_engine)
        result = reasoner.prove(
            initial_facts=[EqualSegment(AB, CD)],
            goals=[EqualSegment(CD, AB)],
            max_depth=10
        )

        if result.success:
            print(f\"Proved {len(result.proven_goals)} goals\")
    """

    def __init__(
        self,
        theorem_engine: TheoremEngine,
        strategy: Optional[SearchStrategy] = None
    ):
        """
        Initialize backward reasoner.

        Args:
            theorem_engine: Engine with loaded theorems
            strategy: Search strategy (default: BreadthFirstStrategy)
        """
        self.theorem_engine = theorem_engine
        self.strategy = strategy or BreadthFirstStrategy()
        # Reuse the theorem engine's applicator so auxiliary construction
        # and matcher configuration stay consistent across reasoners.
        self.applicator = theorem_engine.applicator
        self.matcher = PatternMatcher()
        self.unifier = Unifier()

    def prove(
        self,
        initial_facts: List[Fact],
        goals: List[Fact],
        max_depth: int = 100,
        max_iterations: int = 1000
    ) -> ProofResult:
        """
        Perform backward reasoning to prove goals.

        Args:
            initial_facts: Known facts (base cases)
            goals: Goals to prove
            max_depth: Maximum search depth
            max_iterations: Maximum reasoning iterations

        Returns:
            ProofResult with proven/failed goals and proof tree
        """
        start_time = time.time()

        # Keep track of original goals
        original_goals = list(goals)

        # Initialize state
        state = ProofState()
        for fact in initial_facts:
            state.add_fact(fact)

        for goal in goals:
            state.add_goal(goal)

        # Initialize proof tree
        tree = ProofTree()
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=list(initial_facts),
            metadata={'description': 'Initial facts (given)'}
        )
        tree.set_root(root)
        state.proof_tree = tree

        # Backward reasoning loop
        iteration = 0
        total_applications = 0

        while iteration < max_iterations and iteration < max_depth:
            iteration += 1
            state.depth = iteration

            # Check if all goals satisfied
            if not self.strategy.should_continue(state, max_depth=max_depth):
                break

            # Select next goal to work on
            current_goal = self.strategy.select_goal(state)
            if not current_goal:
                break

            # Check if goal is already satisfied by known facts
            if state.has_fact(current_goal):
                state.remove_goal(current_goal)
                continue

            # Find theorems that could prove this goal
            applicable_theorems = self._find_theorems_for_goal(current_goal, state)

            if not applicable_theorems:
                # Can't prove this goal, try next one
                # Move to back of queue for retry later
                state.remove_goal(current_goal)
                state.add_goal(current_goal)
                continue

            # Try first applicable theorem
            theorem, sub_goals = applicable_theorems[0]

            # Check if sub-goals are all satisfied
            if all(state.has_fact(sg) for sg in sub_goals):
                # All sub-goals satisfied, can derive goal
                state.add_fact(current_goal)
                state.remove_goal(current_goal)
                state.increment_theorem_usage(theorem.metadata.name)
                total_applications += 1

                # Add to proof tree
                child = ProofNode(
                    node_type=ProofNodeType.THEOREM_APPLICATION,
                    facts=[current_goal],
                    theorem=theorem,
                    metadata={
                        'iteration': iteration,
                        'sub_goals': sub_goals
                    }
                )
                tree.add_node(root, child)
            else:
                # Add unsatisfied sub-goals to goal queue
                for sub_goal in sub_goals:
                    if not state.has_fact(sub_goal) and sub_goal not in state.goals:
                        state.add_goal(sub_goal)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Determine which original goals were proven
        proven_goals = [g for g in original_goals if state.has_fact(g)]
        failed_goals = [g for g in original_goals if not state.has_fact(g)]
        success = len(failed_goals) == 0

        # Build result
        result = ProofResult(
            success=success,
            proof_tree=tree,
            proven_goals=proven_goals,
            failed_goals=failed_goals,
            description=f"Backward reasoning: {total_applications} theorem applications",
            statistics={
                'iterations': iteration,
                'total_facts': len(state.fact_base._facts),
                'proven_goals': len(proven_goals),
                'failed_goals': len(failed_goals),
                'theorem_applications': total_applications,
                'time_ms': int(elapsed_time * 1000),
                'theorem_usage': dict(state.theorem_usage)
            }
        )

        return result

    def _find_theorems_for_goal(
        self,
        goal: Fact,
        state: ProofState
    ) -> List[tuple[Theorem, List[Fact]]]:
        """
        Find theorems that could prove the given goal.

        Args:
            goal: Goal to prove
            state: Current proof state

        Returns:
            List of (theorem, sub_goals) tuples
        """
        applicable = []

        for theorem in self.theorem_engine.theorems:
            # Check if we can use this theorem
            if not state.can_use_theorem(theorem, max_uses=None):
                continue

            # Check if theorem conclusion matches goal
            for conclusion_pattern in theorem.conclusions:
                # Try to match goal to conclusion
                binding = self.matcher.match(conclusion_pattern, goal, None)

                if binding:
                    # Found a theorem that could prove goal
                    # Now determine what sub-goals we need to prove
                    # IMPORTANT: Use the binding from conclusion match for consistency

                    sub_goals = []
                    current_binding = binding  # Start with binding from conclusion match

                    for condition_pattern in theorem.conditions:
                        # Try to instantiate condition with current binding
                        try:
                            instantiated_pattern = self.unifier.substitute(condition_pattern, current_binding)

                            # If pattern is ground (no variables), convert to fact
                            if self.unifier.is_ground(instantiated_pattern):
                                condition_fact = self._pattern_to_fact(instantiated_pattern)
                                if condition_fact is None:
                                    sub_goals = None
                                    break

                                # Check if this fact is already known
                                if not state.has_fact(condition_fact):
                                    # Need to prove this sub-goal
                                    sub_goals.append(condition_fact)
                                # else: condition already satisfied, skip
                            else:
                                # Pattern still has variables - try to unify with known facts
                                # to find possible bindings for those variables
                                matched = False
                                for fact in state.fact_base._facts:
                                    extended_binding = self.matcher.match(condition_pattern, fact, current_binding)
                                    if extended_binding:
                                        # Found a match - this condition is satisfied
                                        matched = True
                                        # Update binding for next conditions
                                        current_binding = extended_binding
                                        break

                                if not matched:
                                    # Can't satisfy this condition with known facts
                                    # Need to prove it as a sub-goal
                                    # But it still has unbound variables, so we can't create a concrete sub-goal
                                    # For now, skip theorems with unbound variables in conditions
                                    sub_goals = None
                                    break
                        except Exception:
                            sub_goals = None
                            break

                    if sub_goals is not None:
                        applicable.append((theorem, sub_goals))
                        break  # Found match for this theorem

        return applicable

    def _pattern_to_fact(self, pattern) -> Optional[Fact]:
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
            return None

        fact_class = getattr(fact_types, fact_class_name)

        # Create fact instance
        # Extract parameter values in the order expected by the constructor
        params = list(pattern.parameters.values())
        try:
            return fact_class(*params)
        except Exception:
            return None

    def can_prove(
        self,
        initial_facts: List[Fact],
        goal: Fact,
        max_depth: int = 100
    ) -> bool:
        """
        Check if a goal can be proven from initial facts.

        Args:
            initial_facts: Known facts
            goal: Goal to prove
            max_depth: Maximum search depth

        Returns:
            True if goal can be proven
        """
        result = self.prove(
            initial_facts=initial_facts,
            goals=[goal],
            max_depth=max_depth
        )

        return result.success and goal in result.proven_goals
