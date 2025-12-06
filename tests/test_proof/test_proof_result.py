"""
Tests for proof result.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 3 - Test proof result
"""

import pytest
import json

from geometry_prover.proof.proof_result import ProofResult
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle
from geometry_prover.utils.geometry_objects import Point, Segment, Angle


class TestProofResult:
    """Test ProofResult class."""

    def test_create_successful_result(self):
        """Test creating a successful proof result."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        tree = ProofTree()
        root = ProofNode(node_type=ProofNodeType.INITIAL_FACT, facts=[])
        tree.set_root(root)

        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal],
            failed_goals=[]
        )

        assert result.success is True
        assert result.proof_tree == tree
        assert len(result.proven_goals) == 1
        assert len(result.failed_goals) == 0

    def test_create_failed_result(self):
        """Test creating a failed proof result."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=False,
            proven_goals=[],
            failed_goals=[goal],
            error_message="Could not find applicable theorem"
        )

        assert result.success is False
        assert result.proof_tree is None
        assert len(result.proven_goals) == 0
        assert len(result.failed_goals) == 1
        assert result.error_message is not None

    def test_default_values(self):
        """Test default values for optional fields."""
        result = ProofResult(success=True)

        assert result.proven_goals == []
        assert result.failed_goals == []
        assert result.statistics == {}
        assert result.description == ""
        assert result.error_message is None

    def test_is_complete_success(self):
        """Test checking complete success status."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        tree = ProofTree()
        root = ProofNode(node_type=ProofNodeType.INITIAL_FACT, facts=[])
        tree.set_root(root)

        # Complete success
        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal],
            failed_goals=[]
        )
        assert result.is_complete_success() is True
        assert result.is_partial_success() is False
        assert result.is_complete_failure() is False

        # Not complete (missing proof tree)
        result = ProofResult(
            success=True,
            proof_tree=None,
            proven_goals=[goal],
            failed_goals=[]
        )
        assert result.is_complete_success() is False

        # Not complete (no proven goals)
        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[],
            failed_goals=[]
        )
        assert result.is_complete_success() is False

        # Not complete (has failed goals)
        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal],
            failed_goals=[goal]
        )
        assert result.is_complete_success() is False

    def test_is_partial_success(self):
        """Test checking partial success status."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ab)

        # Partial success (some proven, some failed)
        result = ProofResult(
            success=False,
            proven_goals=[goal1],
            failed_goals=[goal2]
        )
        assert result.is_partial_success() is True
        assert result.is_complete_success() is False
        assert result.is_complete_failure() is False

        # Not partial (all proven)
        result = ProofResult(
            success=True,
            proven_goals=[goal1, goal2],
            failed_goals=[]
        )
        assert result.is_partial_success() is False

        # Not partial (all failed)
        result = ProofResult(
            success=False,
            proven_goals=[],
            failed_goals=[goal1, goal2]
        )
        assert result.is_partial_success() is False

    def test_is_complete_failure(self):
        """Test checking complete failure status."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        # Complete failure
        result = ProofResult(
            success=False,
            proven_goals=[],
            failed_goals=[goal]
        )
        assert result.is_complete_failure() is True
        assert result.is_partial_success() is False
        assert result.is_complete_success() is False

        # Not complete failure (some proven)
        result = ProofResult(
            success=False,
            proven_goals=[goal],
            failed_goals=[goal]
        )
        assert result.is_complete_failure() is False

    def test_to_dict(self):
        """Test serialization to dictionary."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        tree = ProofTree()
        root = ProofNode(node_type=ProofNodeType.INITIAL_FACT, facts=[])
        tree.set_root(root)

        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal],
            failed_goals=[],
            description="Test proof",
            statistics={'nodes_explored': 5, 'time_ms': 42},
            error_message=None
        )

        d = result.to_dict()

        assert d['success'] is True
        assert d['proof_tree'] is not None
        assert len(d['proven_goals']) == 1
        assert len(d['failed_goals']) == 0
        assert d['description'] == "Test proof"
        assert d['statistics'] == {'nodes_explored': 5, 'time_ms': 42}
        assert d['error_message'] is None
        assert d['status']['complete_success'] is True
        assert d['status']['partial_success'] is False
        assert d['status']['complete_failure'] is False

    def test_to_dict_no_tree(self):
        """Test serialization with no proof tree."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=False,
            proven_goals=[],
            failed_goals=[goal]
        )

        d = result.to_dict()

        assert d['proof_tree'] is None

    def test_to_json(self):
        """Test serialization to JSON."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=True,
            proven_goals=[goal],
            failed_goals=[]
        )

        json_str = result.to_json()

        # Parse back to verify valid JSON
        parsed = json.loads(json_str)
        assert parsed['success'] is True
        assert len(parsed['proven_goals']) == 1

    def test_print_summary(self, capsys):
        """Test printing summary."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        tree = ProofTree()
        root = ProofNode(node_type=ProofNodeType.INITIAL_FACT, facts=[])
        tree.set_root(root)

        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal],
            failed_goals=[],
            description="Symmetry proof",
            statistics={'nodes_explored': 3, 'time_ms': 10}
        )

        result.print_summary()

        captured = capsys.readouterr()
        assert "Proof Result" in captured.out
        assert "Success: True" in captured.out
        assert "Complete success" in captured.out
        assert "nodes_explored: 3" in captured.out
        assert "Symmetry proof" in captured.out

    def test_print_summary_with_error(self, capsys):
        """Test printing summary with error message."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=False,
            proven_goals=[],
            failed_goals=[goal],
            error_message="Timeout exceeded"
        )

        result.print_summary()

        captured = capsys.readouterr()
        assert "Success: False" in captured.out
        assert "Complete failure" in captured.out
        assert "Timeout exceeded" in captured.out

    def test_print_summary_partial_success(self, capsys):
        """Test printing summary for partial success."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=False,
            proven_goals=[goal1],
            failed_goals=[goal2]
        )

        result.print_summary()

        captured = capsys.readouterr()
        assert "Partial success" in captured.out
        assert "Proven goals: 1" in captured.out
        assert "Failed goals: 1" in captured.out

    def test_repr(self):
        """Test string representation."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        result = ProofResult(
            success=True,
            proven_goals=[goal],
            failed_goals=[]
        )

        repr_str = repr(result)
        assert "ProofResult" in repr_str
        assert "success" in repr_str
        assert "proven=1" in repr_str
        assert "failed=0" in repr_str

    def test_complex_result_workflow(self):
        """Test a complex result workflow."""
        # Build a proof tree
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

        # Create result with multiple goals
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_cd, seg_ab)
        goal2 = EqualSegment(seg_ab, seg_ef)
        goal3 = EqualSegment(seg_ef, seg_cd)

        result = ProofResult(
            success=True,
            proof_tree=tree,
            proven_goals=[goal1, goal2],
            failed_goals=[goal3],
            description="Multi-step equality proof",
            statistics={
                'nodes_explored': 10,
                'time_ms': 127,
                'theorems_applied': 5,
                'iterations': 3
            }
        )

        # Verify status
        assert result.is_partial_success() is True
        assert result.is_complete_success() is False

        # Verify tree
        assert result.proof_tree.get_depth() == 1
        assert len(result.proof_tree.get_all_nodes()) == 3

        # Verify serialization
        d = result.to_dict()
        assert len(d['proven_goals']) == 2
        assert len(d['failed_goals']) == 1
        assert d['statistics']['theorems_applied'] == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
