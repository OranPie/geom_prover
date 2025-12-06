"""
Proof result data structure.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 3 - ProofResult implementation

This module provides the ProofResult class which encapsulates
the result of a proof attempt, including success/failure status,
proof tree, statistics, and error messages.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json

from geometry_prover.facts.fact_types import Fact
from geometry_prover.proof.proof_tree import ProofTree


@dataclass
class ProofResult:
    """
    Result of a proof attempt.

    Encapsulates all information about a proof search:
    - Success/failure status
    - Proof tree (if successful)
    - Proven and failed goals
    - Statistics (nodes explored, time, etc.)
    - Error messages (if failed)

    Example:
        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal1, goal2],
            failed_goals=[],
            statistics={'nodes_explored': 15, 'time_ms': 42}
        )

        if result.is_complete_success():
            print(f"Proof complete in {result.statistics['time_ms']}ms")
            print(f"Proof tree depth: {result.proof_tree.get_depth()}")
    """

    success: bool
    proof_tree: Optional[ProofTree] = None
    proven_goals: List[Fact] = None
    failed_goals: List[Fact] = None
    description: str = ""
    statistics: Dict[str, Any] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.proven_goals is None:
            self.proven_goals = []
        if self.failed_goals is None:
            self.failed_goals = []
        if self.statistics is None:
            self.statistics = {}

    def is_complete_success(self) -> bool:
        """
        Check if proof was completely successful.

        A complete success means:
        - success=True
        - All goals proven (proven_goals non-empty, failed_goals empty)
        - Proof tree exists

        Returns:
            True if proof was completely successful
        """
        return (
            self.success and
            len(self.proven_goals) > 0 and
            len(self.failed_goals) == 0 and
            self.proof_tree is not None
        )

    def is_partial_success(self) -> bool:
        """
        Check if proof was partially successful.

        A partial success means:
        - Some goals proven (proven_goals non-empty)
        - Some goals failed (failed_goals non-empty)

        Returns:
            True if proof was partially successful
        """
        return (
            len(self.proven_goals) > 0 and
            len(self.failed_goals) > 0
        )

    def is_complete_failure(self) -> bool:
        """
        Check if proof completely failed.

        A complete failure means:
        - success=False
        - No goals proven (proven_goals empty)
        - All goals failed (failed_goals non-empty)

        Returns:
            True if proof completely failed
        """
        return (
            not self.success and
            len(self.proven_goals) == 0 and
            len(self.failed_goals) > 0
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'success': self.success,
            'proof_tree': self.proof_tree.to_dict() if self.proof_tree else None,
            'proven_goals': [str(g) for g in self.proven_goals],
            'failed_goals': [str(g) for g in self.failed_goals],
            'description': self.description,
            'statistics': self.statistics,
            'error_message': self.error_message,
            'status': {
                'complete_success': self.is_complete_success(),
                'partial_success': self.is_partial_success(),
                'complete_failure': self.is_complete_failure()
            }
        }

    def to_json(self) -> str:
        """
        Convert result to JSON string.

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=2)

    def print_summary(self) -> None:
        """Print human-readable summary of proof result."""
        print(f"\n=== Proof Result ===")
        print(f"Success: {self.success}")
        print(f"Proven goals: {len(self.proven_goals)}")
        print(f"Failed goals: {len(self.failed_goals)}")

        if self.is_complete_success():
            print("Status: Complete success ✓")
        elif self.is_partial_success():
            print("Status: Partial success ⚠")
        elif self.is_complete_failure():
            print("Status: Complete failure ✗")

        if self.proof_tree:
            print(f"\n=== Proof Tree ===")
            print(f"Nodes: {len(self.proof_tree.get_all_nodes())}")
            print(f"Depth: {self.proof_tree.get_depth()}")

        if self.statistics:
            print(f"\n=== Statistics ===")
            for key, value in self.statistics.items():
                print(f"  {key}: {value}")

        if self.description:
            print(f"\n=== Description ===")
            print(self.description)

        if self.error_message:
            print(f"\n=== Error ===")
            print(self.error_message)

        if self.proven_goals:
            print(f"\n=== Proven Goals ===")
            for i, goal in enumerate(self.proven_goals, 1):
                print(f"  {i}. {goal}")

        if self.failed_goals:
            print(f"\n=== Failed Goals ===")
            for i, goal in enumerate(self.failed_goals, 1):
                print(f"  {i}. {goal}")

    def __repr__(self) -> str:
        status = "success" if self.success else "failure"
        return (
            f"ProofResult("
            f"{status}, "
            f"proven={len(self.proven_goals)}, "
            f"failed={len(self.failed_goals)})"
        )
