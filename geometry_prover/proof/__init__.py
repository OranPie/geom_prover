"""
Proof generation and search module.

This module provides:
- Proof tree data structures (proof_tree.py)
- Proof state management (proof_state.py)
- Proof result encapsulation (proof_result.py)
- Search strategies (search_strategy.py)
- Forward reasoning engine (forward_reasoner.py)
- Backward reasoning engine (backward_reasoner.py)
- Bidirectional reasoning engine (bidirectional_reasoner.py)
"""

from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.proof_result import ProofResult
from geometry_prover.proof.search_strategy import (
    SearchStrategy,
    BreadthFirstStrategy,
    DepthFirstStrategy,
    BestFirstStrategy,
    TheoremCandidate,
    SearchOrder,
    create_strategy
)
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner

__all__ = [
    'ProofTree',
    'ProofNode',
    'ProofNodeType',
    'ProofState',
    'ProofResult',
    'SearchStrategy',
    'BreadthFirstStrategy',
    'DepthFirstStrategy',
    'BestFirstStrategy',
    'TheoremCandidate',
    'SearchOrder',
    'create_strategy',
    'ForwardReasoner',
    'BackwardReasoner',
    'BidirectionalReasoner',
]
