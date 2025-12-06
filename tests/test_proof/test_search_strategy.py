"""
Tests for search strategies.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Days 4-5 - Test search strategies
"""

import pytest

from geometry_prover.proof.search_strategy import (
    SearchStrategy,
    BreadthFirstStrategy,
    DepthFirstStrategy,
    BestFirstStrategy,
    TheoremCandidate,
    SearchOrder,
    create_strategy
)
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.facts.fact_types import EqualSegment
from geometry_prover.utils.geometry_objects import Point, Segment
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate


class TestTheoremCandidate:
    """Test TheoremCandidate class."""

    def test_create_candidate(self):
        """Test creating a theorem candidate."""
        theorem = TheoremBuilder("test") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        candidate = TheoremCandidate(theorem=theorem)

        assert candidate.theorem == theorem
        assert candidate.score == 0.0
        assert candidate.metadata == {}

    def test_create_candidate_with_score(self):
        """Test creating candidate with score."""
        theorem = TheoremBuilder("test") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        candidate = TheoremCandidate(
            theorem=theorem,
            score=5.0,
            metadata={'test': 'value'}
        )

        assert candidate.score == 5.0
        assert candidate.metadata == {'test': 'value'}


class TestBreadthFirstStrategy:
    """Test BreadthFirstStrategy."""

    def test_select_goal_fifo(self):
        """Test selecting goal FIFO (first-in-first-out)."""
        strategy = BreadthFirstStrategy()
        state = ProofState()

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)
        goal3 = EqualSegment(seg_ab, seg_ef)

        state.add_goals([goal1, goal2, goal3])

        # Should select first goal
        selected = strategy.select_goal(state)
        assert selected == goal1

    def test_select_goal_empty(self):
        """Test selecting goal from empty state."""
        strategy = BreadthFirstStrategy()
        state = ProofState()

        selected = strategy.select_goal(state)
        assert selected is None

    def test_rank_candidates_no_change(self):
        """Test that breadth-first doesn't reorder candidates."""
        strategy = BreadthFirstStrategy()
        state = ProofState()

        theorem1 = TheoremBuilder("th1") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        theorem2 = TheoremBuilder("th2") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        candidates = [
            TheoremCandidate(theorem=theorem1, score=5.0),
            TheoremCandidate(theorem=theorem2, score=10.0)
        ]

        ranked = strategy.rank_candidates(candidates, state)

        # Should return in original order
        assert ranked[0].theorem == theorem1
        assert ranked[1].theorem == theorem2

    def test_should_continue_with_goals(self):
        """Test should_continue with unsatisfied goals."""
        strategy = BreadthFirstStrategy()
        state = ProofState()
        state.depth = 5

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_ab, seg_cd)
        state.add_goal(goal)

        assert strategy.should_continue(state, max_depth=10) is True

    def test_should_continue_depth_limit(self):
        """Test should_continue stops at depth limit."""
        strategy = BreadthFirstStrategy()
        state = ProofState()
        state.depth = 100

        assert strategy.should_continue(state, max_depth=100) is False

    def test_should_continue_no_goals(self):
        """Test should_continue stops when no goals."""
        strategy = BreadthFirstStrategy()
        state = ProofState()
        state.depth = 5

        assert strategy.should_continue(state, max_depth=10) is False


class TestDepthFirstStrategy:
    """Test DepthFirstStrategy."""

    def test_select_goal_lifo(self):
        """Test selecting goal LIFO (last-in-first-out)."""
        strategy = DepthFirstStrategy()
        state = ProofState()

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)
        goal3 = EqualSegment(seg_ab, seg_ef)

        state.add_goals([goal1, goal2, goal3])

        # Should select last goal (LIFO)
        selected = strategy.select_goal(state)
        assert selected == goal3

    def test_select_goal_empty(self):
        """Test selecting goal from empty state."""
        strategy = DepthFirstStrategy()
        state = ProofState()

        selected = strategy.select_goal(state)
        assert selected is None

    def test_rank_candidates_first_only(self):
        """Test that depth-first returns only first candidate."""
        strategy = DepthFirstStrategy()
        state = ProofState()

        theorem1 = TheoremBuilder("th1") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        theorem2 = TheoremBuilder("th2") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        candidates = [
            TheoremCandidate(theorem=theorem1),
            TheoremCandidate(theorem=theorem2)
        ]

        ranked = strategy.rank_candidates(candidates, state)

        # Should return only first candidate
        assert len(ranked) == 1
        assert ranked[0].theorem == theorem1

    def test_rank_candidates_empty(self):
        """Test ranking empty candidate list."""
        strategy = DepthFirstStrategy()
        state = ProofState()

        ranked = strategy.rank_candidates([], state)
        assert ranked == []

    def test_should_continue_with_goals(self):
        """Test should_continue with goals."""
        strategy = DepthFirstStrategy()
        state = ProofState()
        state.depth = 5

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_ab, seg_cd)
        state.add_goal(goal)

        assert strategy.should_continue(state, max_depth=10) is True

    def test_should_continue_depth_limit(self):
        """Test should_continue stops at depth limit."""
        strategy = DepthFirstStrategy()
        state = ProofState()
        state.depth = 100

        assert strategy.should_continue(state, max_depth=100) is False


class TestBestFirstStrategy:
    """Test BestFirstStrategy."""

    def test_select_goal_best(self):
        """Test selecting best goal (currently first unsatisfied)."""
        strategy = BestFirstStrategy()
        state = ProofState()

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)

        state.add_goals([goal1, goal2])
        state.add_fact(goal1)  # Satisfy first goal

        # Should select first unsatisfied goal
        selected = strategy.select_goal(state)
        assert selected == goal2

    def test_select_goal_empty(self):
        """Test selecting goal from empty state."""
        strategy = BestFirstStrategy()
        state = ProofState()

        selected = strategy.select_goal(state)
        assert selected is None

    def test_rank_candidates_by_score(self):
        """Test ranking candidates by score."""
        strategy = BestFirstStrategy()
        state = ProofState()

        theorem1 = TheoremBuilder("th1") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        theorem2 = TheoremBuilder("th2") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        candidates = [
            TheoremCandidate(theorem=theorem1, score=5.0),
            TheoremCandidate(theorem=theorem2, score=10.0)
        ]

        ranked = strategy.rank_candidates(candidates, state)

        # Should be sorted by score (descending)
        assert ranked[0].theorem == theorem2  # Higher score first
        assert ranked[1].theorem == theorem1

    def test_rank_candidates_usage_penalty(self):
        """Test that usage penalizes score."""
        strategy = BestFirstStrategy()
        state = ProofState()

        theorem = TheoremBuilder("th1") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        # Use theorem multiple times
        state.increment_theorem_usage("th1")
        state.increment_theorem_usage("th1")

        candidates = [TheoremCandidate(theorem=theorem, score=10.0)]
        ranked = strategy.rank_candidates(candidates, state)

        # Score should be penalized for usage
        # Original: 10.0, Penalty: 2 * 5 = 10, Final: 0.0
        assert ranked[0].score == 0.0

    def test_should_continue_with_goals(self):
        """Test should_continue with goals."""
        strategy = BestFirstStrategy()
        state = ProofState()
        state.depth = 5

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_ab, seg_cd)
        state.add_goal(goal)

        assert strategy.should_continue(state, max_depth=10) is True


class TestCreateStrategy:
    """Test strategy factory function."""

    def test_create_breadth_first(self):
        """Test creating breadth-first strategy."""
        strategy = create_strategy("breadth")
        assert isinstance(strategy, BreadthFirstStrategy)

        strategy = create_strategy("breadth_first")
        assert isinstance(strategy, BreadthFirstStrategy)

        strategy = create_strategy("bfs")
        assert isinstance(strategy, BreadthFirstStrategy)

    def test_create_depth_first(self):
        """Test creating depth-first strategy."""
        strategy = create_strategy("depth")
        assert isinstance(strategy, DepthFirstStrategy)

        strategy = create_strategy("depth_first")
        assert isinstance(strategy, DepthFirstStrategy)

        strategy = create_strategy("dfs")
        assert isinstance(strategy, DepthFirstStrategy)

    def test_create_best_first(self):
        """Test creating best-first strategy."""
        strategy = create_strategy("best")
        assert isinstance(strategy, BestFirstStrategy)

        strategy = create_strategy("best_first")
        assert isinstance(strategy, BestFirstStrategy)

    def test_create_unknown_strategy(self):
        """Test creating unknown strategy raises error."""
        with pytest.raises(ValueError) as exc_info:
            create_strategy("unknown")

        assert "Unknown strategy" in str(exc_info.value)

    def test_create_case_insensitive(self):
        """Test strategy creation is case-insensitive."""
        strategy = create_strategy("BREADTH")
        assert isinstance(strategy, BreadthFirstStrategy)

        strategy = create_strategy("Depth_First")
        assert isinstance(strategy, DepthFirstStrategy)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
