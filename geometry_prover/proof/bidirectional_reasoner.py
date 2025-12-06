"""
Bidirectional reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 6, Day 5 - Bidirectional Search

This module provides a bidirectional reasoning engine that combines
forward and backward reasoning for more efficient proof search.
It works from both ends - deriving facts forward from initial facts
and working backward from goals - meeting in the middle.
"""

from typing import List, Optional
import time

from geometry_prover.facts.fact_types import Fact
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.proof.proof_result import ProofResult
from geometry_prover.proof.search_strategy import SearchStrategy, BreadthFirstStrategy


class BidirectionalReasoner:
    """
    Bidirectional reasoning engine combining forward and backward search.

    The bidirectional reasoner:
    - Starts forward reasoning from initial facts
    - Starts backward reasoning from goals
    - Alternates between forward and backward steps
    - Stops when goals are proven or limits reached
    - Often more efficient than pure forward or backward reasoning

    Example:
        reasoner = BidirectionalReasoner(theorem_engine)
        result = reasoner.prove(
            initial_facts=[EqualSegment(AB, CD)],
            goals=[EqualSegment(CD, AB)],
            max_depth=10
        )

        if result.success:
            print(f"Proved goals in {result.statistics['iterations']} iterations")
    """

    def __init__(
        self,
        theorem_engine: TheoremEngine,
        strategy: Optional[SearchStrategy] = None
    ):
        """
        Initialize bidirectional reasoner.

        Args:
            theorem_engine: Engine with loaded theorems
            strategy: Search strategy (default: BreadthFirstStrategy)
        """
        self.theorem_engine = theorem_engine
        self.strategy = strategy or BreadthFirstStrategy()
        self.forward_reasoner = ForwardReasoner(theorem_engine, strategy)
        self.backward_reasoner = BackwardReasoner(theorem_engine, strategy)

    def prove(
        self,
        initial_facts: List[Fact],
        goals: List[Fact],
        max_depth: int = 100,
        max_iterations: int = 1000,
        forward_steps: int = 1,
        backward_steps: int = 1
    ) -> ProofResult:
        """
        Perform bidirectional reasoning to prove goals.

        The algorithm alternates between:
        1. Forward steps: Derive new facts from known facts
        2. Backward steps: Work backward from goals to find sub-goals
        3. Check if goals are satisfied after each phase

        Args:
            initial_facts: Known facts (starting point)
            goals: Goals to prove
            max_depth: Maximum search depth
            max_iterations: Maximum total iterations
            forward_steps: Number of forward steps per iteration
            backward_steps: Number of backward steps per iteration

        Returns:
            ProofResult with proven/failed goals and combined proof tree
        """
        start_time = time.time()

        # Track original goals
        original_goals = list(goals)

        # Initialize shared state
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

        # Statistics
        total_forward_steps = 0
        total_backward_steps = 0
        total_applications = 0
        iteration = 0

        # Bidirectional search loop
        while iteration < max_iterations:
            iteration += 1
            state.depth = iteration

            # Check depth limit
            if iteration >= max_depth:
                break

            # Check if all goals are satisfied
            all_satisfied = all(state.has_fact(g) for g in original_goals)
            if all_satisfied:
                break

            # Phase 1: Forward reasoning steps
            for _ in range(forward_steps):
                new_facts = self._forward_step(state)
                if new_facts:
                    total_forward_steps += 1
                    total_applications += len(new_facts)

                    # Add facts to proof tree
                    for fact in new_facts:
                        child = ProofNode(
                            node_type=ProofNodeType.THEOREM_APPLICATION,
                            facts=[fact],
                            metadata={
                                'iteration': iteration,
                                'direction': 'forward'
                            }
                        )
                        tree.add_node(root, child)

                    # Check if goals satisfied after forward step
                    if all(state.has_fact(g) for g in original_goals):
                        break

            # Phase 2: Backward reasoning steps
            for _ in range(backward_steps):
                # Try to prove unsatisfied goals
                progress = self._backward_step(state, original_goals)
                if progress:
                    total_backward_steps += 1

                    # Check if goals satisfied after backward step
                    if all(state.has_fact(g) for g in original_goals):
                        break

            # Check for convergence (no progress in either direction)
            if total_forward_steps + total_backward_steps == 0:
                break

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Determine which goals were proven
        proven_goals = [g for g in original_goals if state.has_fact(g)]
        failed_goals = [g for g in original_goals if not state.has_fact(g)]
        success = len(failed_goals) == 0

        # Build result
        result = ProofResult(
            success=success,
            proof_tree=tree,
            proven_goals=proven_goals,
            failed_goals=failed_goals,
            description=f"Bidirectional reasoning: {total_forward_steps} forward + {total_backward_steps} backward steps",
            statistics={
                'iterations': iteration,
                'forward_steps': total_forward_steps,
                'backward_steps': total_backward_steps,
                'total_facts': len(state.fact_base._facts),
                'derived_facts': len(state.fact_base._facts) - len(initial_facts),
                'proven_goals': len(proven_goals),
                'failed_goals': len(failed_goals),
                'theorem_applications': total_applications,
                'time_ms': int(elapsed_time * 1000),
                'theorem_usage': dict(state.theorem_usage)
            }
        )

        return result

    def _forward_step(self, state: ProofState) -> List[Fact]:
        """
        Perform one forward reasoning step.

        Args:
            state: Current proof state

        Returns:
            List of newly derived facts (empty if no progress)
        """
        new_facts = []
        current_facts = list(state.fact_base._facts)

        # Try each theorem
        for theorem in self.theorem_engine.theorems:
            # Check if we can use this theorem
            if not state.can_use_theorem(theorem, max_uses=10):  # Limit usage
                continue

            # Try to apply theorem with ALL possible bindings
            applications = self.forward_reasoner.applicator.apply_with_all_bindings(
                theorem,
                current_facts
            )

            for application in applications:
                if application and application.derived_facts:
                    # Check which facts are actually new
                    for fact in application.derived_facts:
                        if not state.has_fact(fact):
                            state.add_fact(fact)
                            new_facts.append(fact)
                            state.increment_theorem_usage(theorem.metadata.name)

            # Only apply one theorem per step for balance
            if new_facts:
                break

        return new_facts

    def _backward_step(self, state: ProofState, original_goals: List[Fact]) -> bool:
        """
        Perform one backward reasoning step.

        Args:
            state: Current proof state
            original_goals: Original goals to prove

        Returns:
            True if progress was made, False otherwise
        """
        # Find an unsatisfied goal
        for goal in state.goals:
            if state.has_fact(goal):
                state.remove_goal(goal)
                continue

            # Find theorems that could prove this goal
            applicable = self.backward_reasoner._find_theorems_for_goal(goal, state)

            if not applicable:
                # Move to back of queue
                state.remove_goal(goal)
                state.add_goal(goal)
                continue

            # Try first applicable theorem
            theorem, sub_goals = applicable[0]

            # Check if all sub-goals are satisfied
            if all(state.has_fact(sg) for sg in sub_goals):
                # Can derive the goal
                state.add_fact(goal)
                state.remove_goal(goal)
                state.increment_theorem_usage(theorem.metadata.name)
                return True
            else:
                # Add unsatisfied sub-goals
                for sub_goal in sub_goals:
                    if not state.has_fact(sub_goal) and sub_goal not in state.goals:
                        state.add_goal(sub_goal)
                return True  # Made progress by adding sub-goals

        return False  # No progress

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
