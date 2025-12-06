"""
Search strategy interfaces and implementations.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Days 4-5 - SearchStrategy implementation

This module provides search strategies for guiding proof search.
Different strategies explore the search space in different ways:
- Breadth-first: Explore all nodes at current depth before going deeper
- Depth-first: Explore deeply along one path before backtracking
- Best-first: Use heuristics to explore most promising paths first
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from geometry_prover.facts.fact_types import Fact
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.theorems.theorem import Theorem


class SearchOrder(Enum):
    """Order in which to explore goals."""
    FIFO = "fifo"  # First-in-first-out (breadth-first)
    LIFO = "lifo"  # Last-in-first-out (depth-first)
    PRIORITY = "priority"  # By heuristic score


@dataclass
class TheoremCandidate:
    """
    A candidate theorem application.

    Represents a theorem that could be applied to derive new facts.
    """
    theorem: Theorem
    score: float = 0.0
    metadata: dict = None

    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}


class SearchStrategy(ABC):
    """
    Abstract base class for search strategies.

    A search strategy guides the proof search by:
    - Selecting which goal to work on next
    - Ranking theorem candidates by promise
    - Deciding when to continue or stop search
    """

    @abstractmethod
    def select_goal(self, state: ProofState) -> Optional[Fact]:
        """
        Select the next goal to work on.

        Args:
            state: Current proof state

        Returns:
            Next goal to work on, or None if no goals remain
        """
        pass

    @abstractmethod
    def rank_candidates(
        self,
        candidates: List[TheoremCandidate],
        state: ProofState
    ) -> List[TheoremCandidate]:
        """
        Rank theorem candidates by promise.

        Args:
            candidates: List of candidate theorems
            state: Current proof state

        Returns:
            Candidates sorted by promise (best first)
        """
        pass

    @abstractmethod
    def should_continue(self, state: ProofState, **kwargs) -> bool:
        """
        Decide whether to continue search.

        Args:
            state: Current proof state
            **kwargs: Additional parameters (e.g., max_depth, time_limit)

        Returns:
            True if search should continue
        """
        pass


class BreadthFirstStrategy(SearchStrategy):
    """
    Breadth-first search strategy.

    Explores all nodes at the current depth before going deeper.
    - Goals: FIFO queue (first-in-first-out)
    - Candidates: Explore all at each level
    - Continue: Until depth limit or no goals
    """

    def select_goal(self, state: ProofState) -> Optional[Fact]:
        """
        Select first goal (FIFO).

        Args:
            state: Current proof state

        Returns:
            First goal in queue, or None if empty
        """
        if state.goals:
            return state.goals[0]
        return None

    def rank_candidates(
        self,
        candidates: List[TheoremCandidate],
        state: ProofState
    ) -> List[TheoremCandidate]:
        """
        Return candidates in original order (explore all).

        Args:
            candidates: List of candidates
            state: Current proof state

        Returns:
            Candidates in original order
        """
        return candidates

    def should_continue(self, state: ProofState, **kwargs) -> bool:
        """
        Continue until depth limit reached or no unsatisfied goals.

        Args:
            state: Current proof state
            **kwargs: May include 'max_depth'

        Returns:
            True if should continue searching
        """
        max_depth = kwargs.get('max_depth', 100)

        # Stop if depth limit reached
        if state.depth >= max_depth:
            return False

        # Stop if no more goals
        if len(state.get_unsatisfied_goals()) == 0:
            return False

        return True


class DepthFirstStrategy(SearchStrategy):
    """
    Depth-first search strategy.

    Explores deeply along one path before backtracking.
    - Goals: LIFO stack (last-in-first-out)
    - Candidates: Explore first candidate deeply
    - Continue: Until depth limit or no goals
    """

    def select_goal(self, state: ProofState) -> Optional[Fact]:
        """
        Select last goal (LIFO).

        Args:
            state: Current proof state

        Returns:
            Last goal in stack, or None if empty
        """
        if state.goals:
            return state.goals[-1]  # Last goal (LIFO)
        return None

    def rank_candidates(
        self,
        candidates: List[TheoremCandidate],
        state: ProofState
    ) -> List[TheoremCandidate]:
        """
        Return first candidate (explore deeply).

        Args:
            candidates: List of candidates
            state: Current proof state

        Returns:
            List with only first candidate
        """
        if candidates:
            return [candidates[0]]
        return []

    def should_continue(self, state: ProofState, **kwargs) -> bool:
        """
        Continue until depth limit or no goals.

        Args:
            state: Current proof state
            **kwargs: May include 'max_depth'

        Returns:
            True if should continue searching
        """
        max_depth = kwargs.get('max_depth', 100)

        if state.depth >= max_depth:
            return False

        if len(state.get_unsatisfied_goals()) == 0:
            return False

        return True


class BestFirstStrategy(SearchStrategy):
    """
    Best-first search strategy.

    Uses heuristics to explore most promising paths first.
    - Goals: Priority queue by heuristic score
    - Candidates: Sorted by score (best first)
    - Continue: Until depth limit or no goals

    Heuristics include:
    - Goal relevance (involves original problem points)
    - Theorem priority
    - Number of matched premises
    """

    def select_goal(self, state: ProofState) -> Optional[Fact]:
        """
        Select goal with highest score.

        Currently uses simple heuristic: first unsatisfied goal.
        Could be enhanced with scoring based on:
        - How many theorems could help prove it
        - How "close" it is to initial facts
        - Syntactic similarity to other goals

        Args:
            state: Current proof state

        Returns:
            Best goal by heuristic, or None if no goals
        """
        unsatisfied = state.get_unsatisfied_goals()
        if unsatisfied:
            # Simple heuristic: first unsatisfied goal
            # TODO: Implement proper goal scoring
            return unsatisfied[0]
        return None

    def rank_candidates(
        self,
        candidates: List[TheoremCandidate],
        state: ProofState
    ) -> List[TheoremCandidate]:
        """
        Sort candidates by score (best first).

        Score is based on:
        - Theorem priority (metadata)
        - Usage count (prefer less-used theorems)
        - Candidate's pre-computed score

        Args:
            candidates: List of candidates
            state: Current proof state

        Returns:
            Candidates sorted by score (descending)
        """
        # Score each candidate
        for candidate in candidates:
            score = 0.0

            # Theorem priority (higher is better)
            if hasattr(candidate.theorem.metadata, 'priority'):
                score += candidate.theorem.metadata.priority * 10

            # Usage count (prefer less-used theorems)
            usage = state.get_theorem_usage(candidate.theorem.metadata.name)
            score -= usage * 5  # Penalty for repeated use

            # Pre-computed score from candidate
            score += candidate.score

            candidate.score = score

        # Sort by score (descending)
        return sorted(candidates, key=lambda c: c.score, reverse=True)

    def should_continue(self, state: ProofState, **kwargs) -> bool:
        """
        Continue until depth limit or no goals.

        Args:
            state: Current proof state
            **kwargs: May include 'max_depth'

        Returns:
            True if should continue searching
        """
        max_depth = kwargs.get('max_depth', 100)

        if state.depth >= max_depth:
            return False

        if len(state.get_unsatisfied_goals()) == 0:
            return False

        return True


def create_strategy(strategy_name: str) -> SearchStrategy:
    """
    Factory function to create search strategies.

    Args:
        strategy_name: Name of strategy ("breadth", "depth", "best")

    Returns:
        Corresponding strategy instance

    Raises:
        ValueError: If strategy name is unknown
    """
    strategies = {
        "breadth": BreadthFirstStrategy,
        "breadth_first": BreadthFirstStrategy,
        "bfs": BreadthFirstStrategy,
        "depth": DepthFirstStrategy,
        "depth_first": DepthFirstStrategy,
        "dfs": DepthFirstStrategy,
        "best": BestFirstStrategy,
        "best_first": BestFirstStrategy,
    }

    strategy_class = strategies.get(strategy_name.lower())
    if strategy_class is None:
        raise ValueError(
            f"Unknown strategy: {strategy_name}. "
            f"Valid options: {list(strategies.keys())}"
        )

    return strategy_class()
