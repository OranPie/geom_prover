"""
Proof state management.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 2-3 - ProofState implementation

This module provides the ProofState class which tracks the current
state of a proof search, including known facts, goals to prove,
the proof tree, and theorem usage.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from copy import deepcopy

from geometry_prover.facts.fact_types import Fact
from geometry_prover.facts.fact_base import FactBase
from geometry_prover.proof.proof_tree import ProofTree
from geometry_prover.theorems.theorem import Theorem


@dataclass
class ProofState:
    """
    Represents the current state of a proof search.

    A proof state tracks:
    - Known facts (in a FactBase)
    - Goals to prove (stack/queue)
    - Proof tree (reasoning history)
    - Search depth (for limiting recursion)
    - Theorem usage (to prevent infinite loops)

    Example:
        state = ProofState()
        state.add_fact(EqualSegment(seg_ab, seg_cd))
        state.add_goal(EqualSegment(seg_cd, seg_ab))

        # Check if goal is satisfied
        if state.is_goal_satisfied(state.goals[0]):
            print("Goal proven!")

        # Clone for backtracking
        new_state = state.clone()
    """

    fact_base: FactBase = field(default_factory=FactBase)
    goals: List[Fact] = field(default_factory=list)
    proof_tree: ProofTree = field(default_factory=ProofTree)
    depth: int = 0
    theorem_usage: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_fact(self, fact: Fact) -> bool:
        """
        Add a fact to the known facts.

        Args:
            fact: Fact to add

        Returns:
            True if fact was new (not already known), False otherwise
        """
        return self.fact_base.add(fact)

    def add_facts(self, facts: List[Fact]) -> int:
        """
        Add multiple facts to the known facts.

        Args:
            facts: List of facts to add

        Returns:
            Number of new facts added
        """
        count = 0
        for fact in facts:
            if self.add_fact(fact):
                count += 1
        return count

    def has_fact(self, fact: Fact) -> bool:
        """
        Check if a fact is known.

        Args:
            fact: Fact to check

        Returns:
            True if fact is in fact_base
        """
        return fact in self.fact_base._facts

    def add_goal(self, goal: Fact) -> None:
        """
        Add a goal to prove.

        Goals are added to the end of the list (queue-like).

        Args:
            goal: Goal fact to prove
        """
        if goal not in self.goals:
            self.goals.append(goal)

    def add_goals(self, goals: List[Fact]) -> None:
        """
        Add multiple goals to prove.

        Args:
            goals: List of goal facts
        """
        for goal in goals:
            self.add_goal(goal)

    def remove_goal(self, goal: Fact) -> bool:
        """
        Remove a goal from the goals list.

        Args:
            goal: Goal to remove

        Returns:
            True if goal was removed, False if not found
        """
        if goal in self.goals:
            self.goals.remove(goal)
            return True
        return False

    def pop_goal(self) -> Optional[Fact]:
        """
        Remove and return the first goal (FIFO queue).

        Returns:
            First goal, or None if no goals
        """
        if self.goals:
            return self.goals.pop(0)
        return None

    def has_goal(self, goal: Fact) -> bool:
        """
        Check if a goal is in the goals list.

        Args:
            goal: Goal to check

        Returns:
            True if goal is in goals
        """
        return goal in self.goals

    def is_goal_satisfied(self, goal: Fact) -> bool:
        """
        Check if a goal is satisfied by current facts.

        A goal is satisfied if it's in the fact_base.

        Args:
            goal: Goal to check

        Returns:
            True if goal is proven
        """
        return self.has_fact(goal)

    def get_satisfied_goals(self) -> List[Fact]:
        """
        Get all goals that are currently satisfied.

        Returns:
            List of satisfied goals
        """
        return [goal for goal in self.goals if self.is_goal_satisfied(goal)]

    def get_unsatisfied_goals(self) -> List[Fact]:
        """
        Get all goals that are not yet satisfied.

        Returns:
            List of unsatisfied goals
        """
        return [goal for goal in self.goals if not self.is_goal_satisfied(goal)]

    def all_goals_satisfied(self) -> bool:
        """
        Check if all goals are satisfied.

        Returns:
            True if all goals are proven
        """
        return len(self.get_unsatisfied_goals()) == 0

    def increment_theorem_usage(self, theorem_id: str) -> None:
        """
        Increment the usage count for a theorem.

        Used to track and limit theorem applications.

        Args:
            theorem_id: Theorem identifier (usually theorem.metadata.name)
        """
        if theorem_id not in self.theorem_usage:
            self.theorem_usage[theorem_id] = 0
        self.theorem_usage[theorem_id] += 1

    def get_theorem_usage(self, theorem_id: str) -> int:
        """
        Get the usage count for a theorem.

        Args:
            theorem_id: Theorem identifier

        Returns:
            Number of times theorem has been used (0 if never used)
        """
        return self.theorem_usage.get(theorem_id, 0)

    def can_use_theorem(self, theorem: Theorem, max_uses: Optional[int] = None) -> bool:
        """
        Check if a theorem can be used.

        A theorem can be used if it hasn't exceeded its usage limit.

        Args:
            theorem: Theorem to check
            max_uses: Maximum allowed uses (None = unlimited)

        Returns:
            True if theorem can be used
        """
        if max_uses is None:
            return True

        theorem_id = theorem.metadata.name
        current_usage = self.get_theorem_usage(theorem_id)
        return current_usage < max_uses

    def clone(self) -> 'ProofState':
        """
        Create a deep copy of this state for backtracking.

        Returns:
            New ProofState with copied data
        """
        return ProofState(
            fact_base=deepcopy(self.fact_base),
            goals=self.goals.copy(),  # Shallow copy of list (facts are immutable)
            proof_tree=deepcopy(self.proof_tree),
            depth=self.depth,
            theorem_usage=self.theorem_usage.copy(),
            metadata=deepcopy(self.metadata)
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'facts': [str(f) for f in self.fact_base._facts],
            'goals': [str(g) for g in self.goals],
            'depth': self.depth,
            'theorem_usage': self.theorem_usage,
            'satisfied_goals': len(self.get_satisfied_goals()),
            'unsatisfied_goals': len(self.get_unsatisfied_goals()),
            'metadata': self.metadata
        }

    def __repr__(self) -> str:
        return (
            f"ProofState("
            f"facts={len(self.fact_base._facts)}, "
            f"goals={len(self.goals)}, "
            f"depth={self.depth}, "
            f"satisfied={len(self.get_satisfied_goals())})"
        )
