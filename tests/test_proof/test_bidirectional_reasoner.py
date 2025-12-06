"""
Tests for bidirectional reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 6, Day 5 - Test bidirectional search
"""

import pytest
from pathlib import Path

from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.facts.fact_types import EqualSegment
from geometry_prover.utils.geometry_objects import Point, Segment
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate
from geometry_prover.proof.search_strategy import BreadthFirstStrategy, DepthFirstStrategy


class TestBidirectionalReasoner:
    """Test BidirectionalReasoner class."""

    def test_create_reasoner(self):
        """Test creating a bidirectional reasoner."""
        engine = TheoremEngine()
        reasoner = BidirectionalReasoner(engine)

        assert reasoner.theorem_engine == engine
        assert reasoner.strategy is not None
        assert isinstance(reasoner.strategy, BreadthFirstStrategy)
        assert reasoner.forward_reasoner is not None
        assert reasoner.backward_reasoner is not None

    def test_create_reasoner_with_strategy(self):
        """Test creating reasoner with custom strategy."""
        engine = TheoremEngine()
        strategy = DepthFirstStrategy()
        reasoner = BidirectionalReasoner(engine, strategy=strategy)

        assert reasoner.strategy == strategy

    def test_prove_simple_goal(self):
        """Test proving simple goal with symmetry."""
        # Create symmetry theorem
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

        # Initial fact: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Goal: CD = AB
        goals = [EqualSegment(seg_cd, seg_ab)]

        # Run bidirectional reasoning
        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove the goal
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert len(result.failed_goals) == 0

    def test_prove_with_transitivity(self):
        """Test proving goal requiring transitivity."""
        # Create transitivity theorem
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
        reasoner = BidirectionalReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        # Known: AB = CD, CD = EF
        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Goal: AB = EF
        goals = [EqualSegment(seg_ab, seg_ef)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Should prove using transitivity
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert EqualSegment(seg_ab, seg_ef) in result.proven_goals

    def test_prove_multiple_goals(self):
        """Test proving multiple goals."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

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

    def test_prove_unprovable_goal(self):
        """Test that unprovable goals are detected."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

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

    def test_can_prove_true(self):
        """Test can_prove returns True when goal is provable."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_cd, seg_ab)

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
        reasoner = BidirectionalReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_ef, seg_ab)

        can_prove = reasoner.can_prove(initial_facts, goal)
        assert can_prove is False

    def test_statistics_tracking(self):
        """Test that statistics are tracked correctly."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Check statistics
        stats = result.statistics
        assert 'iterations' in stats
        assert 'forward_steps' in stats
        assert 'backward_steps' in stats
        assert 'total_facts' in stats
        assert 'proven_goals' in stats
        assert 'failed_goals' in stats
        assert 'theorem_applications' in stats
        assert 'time_ms' in stats
        assert 'theorem_usage' in stats

        assert stats['proven_goals'] == 1
        assert stats['failed_goals'] == 0

    def test_forward_backward_balance(self):
        """Test that forward and backward steps are balanced."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = BidirectionalReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        # Run with equal forward and backward steps
        result = reasoner.prove(
            initial_facts,
            goals,
            max_depth=10,
            forward_steps=1,
            backward_steps=1
        )

        assert result.success is True

        # Both forward and backward should contribute
        # (Though one might dominate depending on the problem)
        stats = result.statistics
        total_steps = stats['forward_steps'] + stats['backward_steps']
        assert total_steps > 0

    def test_prove_with_real_theorem_library(self):
        """Test bidirectional reasoning with actual theorem library."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        reasoner = BidirectionalReasoner(engine)

        # Initial facts: AB = CD, CD = EF
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Goal: AB = EF (requires transitivity)
        goals = [EqualSegment(seg_ab, seg_ef)]

        result = reasoner.prove(initial_facts, goals, max_depth=20, max_iterations=100)

        # Should prove the goal
        assert result.success is True
        assert len(result.proven_goals) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
