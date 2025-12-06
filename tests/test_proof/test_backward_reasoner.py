"""
Tests for backward reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 6, Day 4 - Test backward reasoning
"""

import pytest
from pathlib import Path

from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle
from geometry_prover.utils.geometry_objects import Point, Segment, Angle
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate
from geometry_prover.proof.search_strategy import BreadthFirstStrategy, DepthFirstStrategy


class TestBackwardReasoner:
    """Test BackwardReasoner class."""

    def test_create_reasoner(self):
        """Test creating a backward reasoner."""
        engine = TheoremEngine()
        reasoner = BackwardReasoner(engine)

        assert reasoner.theorem_engine == engine
        assert reasoner.strategy is not None
        assert isinstance(reasoner.strategy, BreadthFirstStrategy)

    def test_create_reasoner_with_strategy(self):
        """Test creating reasoner with custom strategy."""
        engine = TheoremEngine()
        strategy = DepthFirstStrategy()
        reasoner = BackwardReasoner(engine, strategy=strategy)

        assert reasoner.strategy == strategy

    def test_prove_simple_goal(self):
        """Test proving simple goal with symmetry."""
        # Create simple symmetry theorem: AB = CD => CD = AB
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        # Initial fact: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Goal: CD = AB
        goals = [EqualSegment(seg_cd, seg_ab)]

        # Run backward reasoning
        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove the goal
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert len(result.failed_goals) == 0
        assert result.statistics['theorem_applications'] >= 1

    def test_prove_already_known_fact(self):
        """Test proving goal that is already a known fact."""
        engine = TheoremEngine()
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        initial_facts = [fact]
        goals = [fact]  # Goal is already known

        result = reasoner.prove(initial_facts, goals, max_depth=5)

        # Should succeed immediately
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert result.statistics['theorem_applications'] == 0  # No need to apply theorems

    def test_prove_unprovable_goal(self):
        """Test proving goal that cannot be proven."""
        # Create symmetry theorem
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_ef, seg_ab)]  # Not provable

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should fail
        assert result.success is False
        assert len(result.proven_goals) == 0
        assert len(result.failed_goals) == 1

    def test_prove_multiple_goals(self):
        """Test proving multiple goals."""
        # Create symmetry theorem
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))
        seg_gh = Segment(Point("G"), Point("H"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_ef, seg_gh)
        ]

        goals = [
            EqualSegment(seg_cd, seg_ab),
            EqualSegment(seg_gh, seg_ef)
        ]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove both goals
        assert result.success is True
        assert len(result.proven_goals) == 2
        assert len(result.failed_goals) == 0

    def test_prove_with_subgoals(self):
        """Test proving goal that requires proving sub-goals."""
        # Create transitivity theorem: AB = CD, CD = EF => AB = EF
        transitivity = (TheoremBuilder("transitivity")
                        .add_variable(Variable("?AB", "segment"))
                        .add_variable(Variable("?CD", "segment"))
                        .add_variable(Variable("?EF", "segment"))
                        .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                        .add_condition(PatternTemplate.equal_segment("?CD", "?EF"))
                        .add_conclusion(PatternTemplate.equal_segment("?AB", "?EF"))
                        .build())

        # Create symmetry theorem
        symmetry = (TheoremBuilder("symmetry")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        engine = TheoremEngine([transitivity, symmetry])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        # Known: AB = CD, CD = EF
        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Goal: AB = EF (requires transitivity)
        goals = [EqualSegment(seg_ab, seg_ef)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove the goal using transitivity
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert EqualSegment(seg_ab, seg_ef) in result.proven_goals

    def test_prove_max_depth_limit(self):
        """Test that max_depth limit is respected."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        # Very low depth limit
        result = reasoner.prove(initial_facts, goals, max_depth=1)

        assert result.statistics['iterations'] <= 1

    def test_can_prove_true(self):
        """Test can_prove returns True when goal is provable."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_cd, seg_ab)

        # Should be able to prove goal
        can_prove = reasoner.can_prove(initial_facts, goal)
        assert can_prove is True

    def test_can_prove_false(self):
        """Test can_prove returns False when goal is not provable."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_ef, seg_ab)  # Not provable

        can_prove = reasoner.can_prove(initial_facts, goal)
        assert can_prove is False

    def test_prove_with_real_theorem_library(self):
        """Test backward reasoning with actual theorem library."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        reasoner = BackwardReasoner(engine)

        # Initial facts: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Goal: CD = AB (symmetry)
        goals = [EqualSegment(seg_cd, seg_ab)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove the goal
        assert result.success is True
        assert len(result.proven_goals) == 1

    def test_proof_tree_structure(self):
        """Test that proof tree is built correctly."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Check tree structure
        tree = result.proof_tree
        assert tree.root is not None
        assert tree.root.node_type.value == "initial_fact"
        assert len(tree.root.facts) == 1

        # Should have at least one child (theorem application)
        assert len(tree.root.children) >= 1
        child = tree.root.children[0]
        assert child.node_type.value == "theorem_application"
        assert child.theorem is not None

    def test_statistics_tracking(self):
        """Test that statistics are tracked correctly."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BackwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Check statistics
        stats = result.statistics
        assert 'iterations' in stats
        assert 'total_facts' in stats
        assert 'proven_goals' in stats
        assert 'failed_goals' in stats
        assert 'theorem_applications' in stats
        assert 'time_ms' in stats
        assert 'theorem_usage' in stats

        assert stats['proven_goals'] == 1
        assert stats['failed_goals'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
