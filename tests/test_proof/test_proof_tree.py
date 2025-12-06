"""
Tests for proof tree data structures.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 1-2 - Test proof tree
"""

import pytest

from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle
from geometry_prover.utils.geometry_objects import Point, Segment, Angle
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate


class TestProofNode:
    """Test ProofNode class."""

    def test_create_initial_fact_node(self):
        """Test creating an initial fact node."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        node = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[fact]
        )

        assert node.node_type == ProofNodeType.INITIAL_FACT
        assert len(node.facts) == 1
        assert node.facts[0] == fact
        assert node.theorem is None
        assert len(node.children) == 0
        assert node.parent is None

    def test_create_theorem_application_node(self):
        """Test creating a theorem application node."""
        # Create a simple theorem
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_cd, seg_ab)

        node = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[fact],
            theorem=theorem
        )

        assert node.node_type == ProofNodeType.THEOREM_APPLICATION
        assert node.theorem is not None
        assert node.theorem.metadata.name == "symmetry"

    def test_add_child(self):
        """Test adding child nodes."""
        parent = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        parent.add_child(child1)
        parent.add_child(child2)

        assert len(parent.children) == 2
        assert child1.parent == parent
        assert child2.parent == parent

    def test_is_leaf(self):
        """Test is_leaf method."""
        parent = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        child = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        assert parent.is_leaf() is True
        assert child.is_leaf() is True

        parent.add_child(child)

        assert parent.is_leaf() is False
        assert child.is_leaf() is True

    def test_is_root(self):
        """Test is_root method."""
        parent = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        child = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        assert parent.is_root() is True
        assert child.is_root() is True

        parent.add_child(child)

        assert parent.is_root() is True
        assert child.is_root() is False

    def test_depth(self):
        """Test depth calculation."""
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        root.add_child(child1)
        child1.add_child(child2)

        assert root.depth() == 0
        assert child1.depth() == 1
        assert child2.depth() == 2

    def test_to_dict(self):
        """Test serialization to dictionary."""
        seg_ab = Segment(Point("A"), Point("B"))
        fact = EqualSegment(seg_ab, seg_ab)

        node = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[fact],
            metadata={'test': 'value'}
        )

        d = node.to_dict()

        assert d['node_type'] == 'initial_fact'
        assert len(d['facts']) == 1
        assert d['theorem'] is None
        assert d['children'] == []
        assert d['metadata'] == {'test': 'value'}

    def test_to_dict_with_children(self):
        """Test serialization with children."""
        parent = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        child = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        parent.add_child(child)

        d = parent.to_dict()

        assert len(d['children']) == 1
        assert d['children'][0]['node_type'] == 'theorem_application'

    def test_repr(self):
        """Test string representation."""
        node = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        repr_str = repr(node)
        assert 'ProofNode' in repr_str
        assert 'initial_fact' in repr_str


class TestProofTree:
    """Test ProofTree class."""

    def test_create_empty_tree(self):
        """Test creating an empty tree."""
        tree = ProofTree()
        assert tree.root is None
        assert len(tree.get_all_nodes()) == 0

    def test_set_root(self):
        """Test setting root node."""
        tree = ProofTree()
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )

        tree.set_root(root)

        assert tree.root == root
        assert root.parent is None
        assert root.is_root() is True

    def test_add_node(self):
        """Test adding nodes to tree."""
        tree = ProofTree()
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )

        tree.add_node(root, child)

        assert len(root.children) == 1
        assert child.parent == root

    def test_get_path_to_root(self):
        """Test getting path from node to root."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child1)

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(child1, child2)

        path = tree.get_path_to_root(child2)

        assert len(path) == 3
        assert path[0] == child2
        assert path[1] == child1
        assert path[2] == root

    def test_get_all_nodes(self):
        """Test getting all nodes in tree."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child1)

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child2)

        grandchild = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(child1, grandchild)

        all_nodes = tree.get_all_nodes()

        assert len(all_nodes) == 4
        # Breadth-first order
        assert all_nodes[0] == root
        assert child1 in all_nodes[1:3]
        assert child2 in all_nodes[1:3]
        assert all_nodes[3] == grandchild

    def test_traverse(self):
        """Test tree traversal."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child1)

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(child1, child2)

        visited = []

        def visitor(node):
            visited.append(node)

        tree.traverse(visitor)

        assert len(visited) == 3
        # Pre-order traversal
        assert visited[0] == root
        assert visited[1] == child1
        assert visited[2] == child2

    def test_get_leaves(self):
        """Test getting leaf nodes."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child1)

        child2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child2)

        grandchild = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(child1, grandchild)

        leaves = tree.get_leaves()

        assert len(leaves) == 2
        assert child2 in leaves
        assert grandchild in leaves

    def test_get_depth(self):
        """Test getting tree depth."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        assert tree.get_depth() == 0

        child1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child1)

        assert tree.get_depth() == 1

        grandchild = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(child1, grandchild)

        assert tree.get_depth() == 2

    def test_to_dict(self):
        """Test tree serialization."""
        tree = ProofTree()

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        child = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, child)

        d = tree.to_dict()

        assert 'root' in d
        assert d['depth'] == 1
        assert d['node_count'] == 2

    def test_to_dict_empty_tree(self):
        """Test serialization of empty tree."""
        tree = ProofTree()
        d = tree.to_dict()

        assert d['root'] is None

    def test_repr(self):
        """Test string representation."""
        tree = ProofTree()
        assert 'empty' in repr(tree)

        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        repr_str = repr(tree)
        assert 'ProofTree' in repr_str
        assert 'nodes=1' in repr_str

    def test_complex_tree_structure(self):
        """Test building a complex tree structure."""
        tree = ProofTree()

        # Root: initial facts
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[]
        )
        tree.set_root(root)

        # Level 1: two theorem applications
        app1 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, app1)

        app2 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(root, app2)

        # Level 2: auxiliary construction from app1
        aux1 = ProofNode(
            node_type=ProofNodeType.AUX_CONSTRUCTION,
            facts=[]
        )
        tree.add_node(app1, aux1)

        # Level 2: theorem application from app2
        app3 = ProofNode(
            node_type=ProofNodeType.THEOREM_APPLICATION,
            facts=[]
        )
        tree.add_node(app2, app3)

        # Verify structure
        assert len(tree.get_all_nodes()) == 5
        assert tree.get_depth() == 2
        assert len(tree.get_leaves()) == 2  # aux1 and app3

        # Verify paths
        path_to_aux1 = tree.get_path_to_root(aux1)
        assert len(path_to_aux1) == 3
        assert path_to_aux1[0] == aux1
        assert path_to_aux1[1] == app1
        assert path_to_aux1[2] == root


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
