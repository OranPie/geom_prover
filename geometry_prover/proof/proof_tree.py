"""
Proof tree data structures.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 1-2 - ProofTree implementation

This module provides data structures for representing proof trees,
which track the reasoning steps used to derive conclusions.
"""

from typing import List, Optional, Callable, Any, Dict
from dataclasses import dataclass, field
from enum import Enum

from geometry_prover.facts.fact_types import Fact
from geometry_prover.theorems.theorem import Theorem


class ProofNodeType(Enum):
    """Type of proof node."""
    INITIAL_FACT = "initial_fact"
    THEOREM_APPLICATION = "theorem_application"
    AUX_CONSTRUCTION = "aux_construction"


@dataclass
class ProofNode:
    """
    A node in a proof tree.

    Represents a single step in a proof, such as:
    - An initial fact (axiom or given)
    - Application of a theorem
    - An auxiliary construction

    Attributes:
        node_type: Type of this node
        facts: Facts established at this node
        theorem: Theorem applied (if type is theorem_application)
        premises: Facts used as input to derive these facts (前置条件)
        children: Child nodes (subsequent steps)
        parent: Parent node (previous step)
        metadata: Additional information (bindings, justification, etc.)
    """
    node_type: ProofNodeType
    facts: List[Fact]
    theorem: Optional[Theorem] = None
    premises: List[Fact] = field(default_factory=list)
    children: List['ProofNode'] = field(default_factory=list)
    parent: Optional['ProofNode'] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, child: 'ProofNode') -> 'ProofNode':
        """
        Add a child node to this node.

        Args:
            child: Child node to add

        Returns:
            The child node (for chaining)
        """
        self.children.append(child)
        child.parent = self
        return child

    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children)."""
        return len(self.children) == 0

    def is_root(self) -> bool:
        """Check if this node is the root (has no parent)."""
        return self.parent is None

    def depth(self) -> int:
        """
        Get the depth of this node (distance from root).

        Returns:
            Depth (root has depth 0)
        """
        if self.is_root():
            return 0
        return 1 + self.parent.depth()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert node to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'node_type': self.node_type.value,
            'facts': [str(f) for f in self.facts],
            'theorem': self.theorem.metadata.name if self.theorem else None,
            'premises': [str(p) for p in self.premises],
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata
        }

    def __repr__(self) -> str:
        type_str = self.node_type.value
        if self.theorem:
            return f"ProofNode({type_str}, theorem={self.theorem.metadata.name}, {len(self.facts)} facts)"
        return f"ProofNode({type_str}, {len(self.facts)} facts)"


class ProofTree:
    """
    A tree structure representing a proof.

    The tree tracks how facts are derived through a series of
    reasoning steps (theorem applications, constructions, etc.).

    Example:
        tree = ProofTree()
        root = tree.set_root(ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[given_fact1, given_fact2]
        ))
        child = tree.add_node(root, ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[derived_fact],
            theorem=symmetry_theorem
        ))
    """

    def __init__(self):
        """Initialize empty proof tree."""
        self.root: Optional[ProofNode] = None

    def set_root(self, node: ProofNode) -> ProofNode:
        """
        Set the root node of the tree.

        Args:
            node: Node to use as root

        Returns:
            The root node
        """
        self.root = node
        node.parent = None
        return node

    def add_node(self, parent: ProofNode, node: ProofNode) -> ProofNode:
        """
        Add a node as a child of the given parent.

        Args:
            parent: Parent node
            node: Node to add

        Returns:
            The added node
        """
        return parent.add_child(node)

    def get_path_to_root(self, node: ProofNode) -> List[ProofNode]:
        """
        Get the path from a node to the root.

        Args:
            node: Starting node

        Returns:
            List of nodes from node to root (inclusive)
        """
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = current.parent
        return path

    def get_all_nodes(self) -> List[ProofNode]:
        """
        Get all nodes in the tree.

        Returns:
            List of all nodes (breadth-first order)
        """
        if self.root is None:
            return []

        nodes = []
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            nodes.append(node)
            queue.extend(node.children)

        return nodes

    def traverse(self, visitor: Callable[[ProofNode], None]) -> None:
        """
        Traverse the tree and apply visitor function to each node.

        Uses pre-order traversal (parent before children).

        Args:
            visitor: Function to call on each node
        """
        if self.root is None:
            return

        def traverse_node(node: ProofNode):
            visitor(node)
            for child in node.children:
                traverse_node(child)

        traverse_node(self.root)

    def get_leaves(self) -> List[ProofNode]:
        """
        Get all leaf nodes (nodes with no children).

        Returns:
            List of leaf nodes
        """
        return [node for node in self.get_all_nodes() if node.is_leaf()]

    def get_depth(self) -> int:
        """
        Get the maximum depth of the tree.

        Returns:
            Maximum depth (root has depth 0)
        """
        if self.root is None:
            return 0

        max_depth = 0
        for node in self.get_all_nodes():
            max_depth = max(max_depth, node.depth())

        return max_depth

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tree to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        if self.root is None:
            return {'root': None}

        return {
            'root': self.root.to_dict(),
            'depth': self.get_depth(),
            'node_count': len(self.get_all_nodes())
        }

    def __repr__(self) -> str:
        if self.root is None:
            return "ProofTree(empty)"
        return f"ProofTree(nodes={len(self.get_all_nodes())}, depth={self.get_depth()})"
