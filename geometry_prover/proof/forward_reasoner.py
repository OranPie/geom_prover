"""
Forward reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 8 - Forward Reasoning

This module provides a forward reasoning engine that automatically
applies theorems to derive new facts from initial facts. It uses
the proof infrastructure (ProofState, ProofTree, SearchStrategy)
and theorem system (TheoremEngine, TheoremApplicator) to perform
automated deduction.
"""

from typing import List, Optional, Dict, Any
import time

from geometry_prover.facts.fact_types import Fact, AngleMeasure
from geometry_prover.theorems.theorem import Theorem
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.theorems.applicator import TheoremApplicator
from geometry_prover.theorems.matcher import PatternMatcher
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.proof.proof_result import ProofResult
from geometry_prover.proof.search_strategy import SearchStrategy, BreadthFirstStrategy
from geometry_prover.solver.numeric_solver import NumericSolver
from geometry_prover.utils.geometry_objects import Angle


class ForwardReasoner:
    """
    Forward reasoning engine for automated fact derivation.

    The forward reasoner:
    - Starts with initial facts
    - Iteratively applies applicable theorems
    - Derives new facts until no more can be derived
    - Tracks derivation history in proof tree
    - Respects depth and fact limits

    Example:
        reasoner = ForwardReasoner(theorem_engine)
        result = reasoner.reason(
            initial_facts=[EqualSegment(AB, CD)],
            max_depth=10,
            max_facts=100
        )

        if result.success:
            print(f"Derived {len(result.derived_facts)} new facts")
    """

    def __init__(
        self,
        theorem_engine: TheoremEngine,
        strategy: Optional[SearchStrategy] = None
    ):
        """
        Initialize forward reasoner.

        Args:
            theorem_engine: Engine with loaded theorems
            strategy: Search strategy (default: BreadthFirstStrategy)
        """
        self.theorem_engine = theorem_engine
        self.strategy = strategy or BreadthFirstStrategy()
        # Use the theorem engine's applicator (which has auxiliary constructor set up)
        self.applicator = theorem_engine.applicator
        self.matcher = PatternMatcher()

    def reason(
        self,
        initial_facts: List[Fact],
        goals: Optional[List[Fact]] = None,
        max_depth: int = 100,
        max_facts: int = 1000,
        max_iterations: int = 100
    ) -> ProofResult:
        """
        Perform forward reasoning from initial facts.

        Args:
            initial_facts: Starting facts
            goals: Optional goals to prove (for goal checking)
            max_depth: Maximum search depth
            max_facts: Maximum total facts
            max_iterations: Maximum reasoning iterations

        Returns:
            ProofResult with derived facts and proof tree
        """
        start_time = time.time()

        # Initialize state
        state = ProofState()
        for fact in initial_facts:
            state.add_fact(fact)

        if goals:
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

        # Track current node for tree building
        current_node = root

        # Initialize numeric solver
        numeric_solver = NumericSolver()

        # Forward reasoning loop
        iteration = 0
        total_applications = 0
        numeric_derivations = 0
        new_facts_this_iteration = []  # Initialize before loop

        while iteration < max_iterations:
            iteration += 1
            state.depth = iteration

            # Check depth limit
            if iteration >= max_depth:
                break

            # Check fact limit
            if len(state.fact_base._facts) >= max_facts:
                break

            # If we have goals, check if all are satisfied
            if goals and len(state.get_unsatisfied_goals()) == 0:
                break

            # Try to apply each theorem
            new_facts_this_iteration = []

            for theorem in self.theorem_engine.theorems:
                # Check if we can use this theorem
                if not state.can_use_theorem(theorem, max_uses=None):
                    continue

                # Try to apply theorem with ALL possible bindings
                applications = self.applicator.apply_with_all_bindings(
                    theorem,
                    list(state.fact_base._facts)
                )

                for application in applications:
                    if application and application.derived_facts:
                        # Check which facts are actually new
                        new_facts = [
                            f for f in application.derived_facts
                            if not state.has_fact(f)
                        ]

                        if new_facts:
                            # Add to state
                            for fact in new_facts:
                                state.add_fact(fact)
                                new_facts_this_iteration.append(fact)

                            # Track theorem usage
                            state.increment_theorem_usage(theorem.metadata.name)
                            total_applications += 1

                            # Add to proof tree with premises (前置条件)
                            child = ProofNode(
                                node_type=ProofNodeType.THEOREM_APPLICATION,
                                facts=new_facts,
                                theorem=theorem,
                                premises=application.matched_facts,  # Track which facts were used
                                metadata={
                                    'iteration': iteration,
                                    'binding': application.binding
                                }
                            )
                            tree.add_node(current_node, child)

            # Run numeric solver every 3 iterations to derive angle values
            if iteration % 3 == 0:
                try:
                    numeric_results = numeric_solver.solve(list(state.fact_base._facts))

                    # Add derived AngleMeasure facts
                    for angle_key, measure in numeric_results['angles'].items():
                        # Parse angle key (e.g., "ABC" -> points A, B, C with vertex B)
                        if len(angle_key) == 3:
                            # Create angle from key
                            # Note: angle_key format is "point1 vertex point2"
                            # We need to construct an Angle object to create the fact
                            # This is a simplified approach - in practice we'd need to
                            # look up actual Point objects from the fact base

                            # Check if we already have this angle measurement
                            angle_fact_exists = False
                            for existing_fact in state.fact_base._facts:
                                if existing_fact.fact_type == "AngleMeasure":
                                    existing_angle = existing_fact.parameters.get("angle")
                                    if existing_angle:
                                        existing_key = f"{existing_angle.point1.name}{existing_angle.vertex.name}{existing_angle.point2.name}"
                                        if existing_key == angle_key:
                                            angle_fact_exists = True
                                            break

                            # If we don't have this measurement yet, we could add it
                            # For now, we'll skip adding facts directly since we need
                            # proper Point object references. The numeric solver serves
                            # primarily as a validation/computation tool for now.
                            # TODO: Enhance to create proper AngleMeasure facts

                except Exception as e:
                    # Silently handle numeric solver errors
                    # The solver is an enhancement, not critical to forward reasoning
                    pass

            # If no new facts, we've reached a fixed point
            if not new_facts_this_iteration:
                break

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Determine success
        if goals:
            proven_goals = state.get_satisfied_goals()
            failed_goals = state.get_unsatisfied_goals()
            success = len(failed_goals) == 0
        else:
            # No goals specified - success if we derived any facts
            proven_goals = []
            failed_goals = []
            success = len(state.fact_base._facts) > len(initial_facts)

        # Build result
        result = ProofResult(
            success=success,
            proof_tree=tree,
            proven_goals=proven_goals,
            failed_goals=failed_goals,
            description=f"Forward reasoning: {total_applications} theorem applications",
            statistics={
                'iterations': iteration,
                'total_facts': len(state.fact_base._facts),
                'derived_facts': len(state.fact_base._facts) - len(initial_facts),
                'theorem_applications': total_applications,
                'numeric_derivations': numeric_derivations,
                'time_ms': int(elapsed_time * 1000),
                'theorem_usage': dict(state.theorem_usage),
                'converged': len(new_facts_this_iteration) == 0 if iteration > 0 else True
            }
        )

        return result

    def can_derive(
        self,
        initial_facts: List[Fact],
        goal: Fact,
        max_depth: int = 100,
        max_facts: int = 1000
    ) -> bool:
        """
        Check if a goal can be derived from initial facts.

        Args:
            initial_facts: Starting facts
            goal: Goal fact to derive
            max_depth: Maximum search depth
            max_facts: Maximum total facts

        Returns:
            True if goal can be derived
        """
        result = self.reason(
            initial_facts=initial_facts,
            goals=[goal],
            max_depth=max_depth,
            max_facts=max_facts
        )

        return result.success and goal in result.proven_goals
