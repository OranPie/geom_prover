"""
Tests for proof state management.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 7, Day 2-3 - Test proof state
"""

import pytest

from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle, Parallel
from geometry_prover.facts.fact_base import FactBase
from geometry_prover.utils.geometry_objects import Point, Segment, Angle, Line
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate


class TestProofState:
    """Test ProofState class."""

    def test_create_empty_state(self):
        """Test creating an empty proof state."""
        state = ProofState()

        assert len(state.fact_base._facts) == 0
        assert len(state.goals) == 0
        assert state.depth == 0
        assert len(state.theorem_usage) == 0
        assert isinstance(state.proof_tree, ProofTree)

    def test_create_state_with_fact_base(self):
        """Test creating state with existing fact base."""
        fact_base = FactBase()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact_base.add(EqualSegment(seg_ab, seg_cd))

        state = ProofState(fact_base=fact_base)

        assert len(state.fact_base._facts) == 1

    def test_add_fact(self):
        """Test adding a fact to the state."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        # Add new fact
        result = state.add_fact(fact)
        assert result is True
        assert len(state.fact_base._facts) == 1

        # Add duplicate fact
        result = state.add_fact(fact)
        assert result is False
        assert len(state.fact_base._facts) == 1

    def test_add_facts(self):
        """Test adding multiple facts."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef),
            EqualSegment(seg_ab, seg_cd)  # Duplicate
        ]

        count = state.add_facts(facts)

        assert count == 2  # Only 2 new facts added
        assert len(state.fact_base._facts) == 2

    def test_has_fact(self):
        """Test checking if a fact exists."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        assert state.has_fact(fact) is False

        state.add_fact(fact)

        assert state.has_fact(fact) is True

    def test_add_goal(self):
        """Test adding a goal."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        state.add_goal(goal)

        assert len(state.goals) == 1
        assert goal in state.goals

    def test_add_goal_duplicate(self):
        """Test adding duplicate goals."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        state.add_goal(goal)
        state.add_goal(goal)  # Duplicate

        assert len(state.goals) == 1

    def test_add_goals(self):
        """Test adding multiple goals."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goals = [
            EqualSegment(seg_cd, seg_ab),
            EqualSegment(seg_ef, seg_cd)
        ]

        state.add_goals(goals)

        assert len(state.goals) == 2

    def test_remove_goal(self):
        """Test removing a goal."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        state.add_goal(goal)
        assert len(state.goals) == 1

        result = state.remove_goal(goal)
        assert result is True
        assert len(state.goals) == 0

        # Remove non-existent goal
        result = state.remove_goal(goal)
        assert result is False

    def test_pop_goal(self):
        """Test popping goals (FIFO)."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)

        state.add_goal(goal1)
        state.add_goal(goal2)

        # Pop first goal (FIFO)
        popped = state.pop_goal()
        assert popped == goal1
        assert len(state.goals) == 1

        popped = state.pop_goal()
        assert popped == goal2
        assert len(state.goals) == 0

        # Pop from empty
        popped = state.pop_goal()
        assert popped is None

    def test_has_goal(self):
        """Test checking if goal exists."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        assert state.has_goal(goal) is False

        state.add_goal(goal)

        assert state.has_goal(goal) is True

    def test_is_goal_satisfied(self):
        """Test checking if goal is satisfied."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        goal = EqualSegment(seg_cd, seg_ab)

        state.add_goal(goal)

        # Goal not satisfied yet
        assert state.is_goal_satisfied(goal) is False

        # Add fact that satisfies goal
        state.add_fact(goal)

        # Goal now satisfied
        assert state.is_goal_satisfied(goal) is True

    def test_get_satisfied_goals(self):
        """Test getting satisfied goals."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)

        state.add_goal(goal1)
        state.add_goal(goal2)

        # Satisfy first goal
        state.add_fact(goal1)

        satisfied = state.get_satisfied_goals()
        assert len(satisfied) == 1
        assert goal1 in satisfied

    def test_get_unsatisfied_goals(self):
        """Test getting unsatisfied goals."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)

        state.add_goal(goal1)
        state.add_goal(goal2)

        # Satisfy first goal
        state.add_fact(goal1)

        unsatisfied = state.get_unsatisfied_goals()
        assert len(unsatisfied) == 1
        assert goal2 in unsatisfied

    def test_all_goals_satisfied(self):
        """Test checking if all goals are satisfied."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        goal1 = EqualSegment(seg_ab, seg_cd)
        goal2 = EqualSegment(seg_cd, seg_ef)

        state.add_goal(goal1)
        state.add_goal(goal2)

        assert state.all_goals_satisfied() is False

        # Satisfy first goal
        state.add_fact(goal1)
        assert state.all_goals_satisfied() is False

        # Satisfy second goal
        state.add_fact(goal2)
        assert state.all_goals_satisfied() is True

    def test_increment_theorem_usage(self):
        """Test incrementing theorem usage."""
        state = ProofState()

        state.increment_theorem_usage("theorem1")
        assert state.get_theorem_usage("theorem1") == 1

        state.increment_theorem_usage("theorem1")
        assert state.get_theorem_usage("theorem1") == 2

        state.increment_theorem_usage("theorem2")
        assert state.get_theorem_usage("theorem2") == 1

    def test_get_theorem_usage(self):
        """Test getting theorem usage count."""
        state = ProofState()

        # Unused theorem returns 0
        assert state.get_theorem_usage("theorem1") == 0

        state.increment_theorem_usage("theorem1")
        assert state.get_theorem_usage("theorem1") == 1

    def test_can_use_theorem(self):
        """Test checking if theorem can be used."""
        state = ProofState()

        theorem = TheoremBuilder("test") \
            .add_variable(Variable("?AB", "segment")) \
            .add_variable(Variable("?CD", "segment")) \
            .add_condition(PatternTemplate.equal_segment("?AB", "?CD")) \
            .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB")) \
            .build()

        # No limit - always can use
        assert state.can_use_theorem(theorem, max_uses=None) is True

        # With limit - can use initially
        assert state.can_use_theorem(theorem, max_uses=2) is True

        state.increment_theorem_usage("test")
        assert state.can_use_theorem(theorem, max_uses=2) is True

        state.increment_theorem_usage("test")
        assert state.can_use_theorem(theorem, max_uses=2) is False

    def test_clone(self):
        """Test cloning state for backtracking."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        state.add_fact(EqualSegment(seg_ab, seg_cd))
        state.add_goal(EqualSegment(seg_cd, seg_ab))
        state.depth = 5
        state.increment_theorem_usage("theorem1")
        state.metadata['test'] = 'value'

        # Clone state
        cloned = state.clone()

        # Verify cloned state matches original
        assert len(cloned.fact_base._facts) == len(state.fact_base._facts)
        assert len(cloned.goals) == len(state.goals)
        assert cloned.depth == state.depth
        assert cloned.get_theorem_usage("theorem1") == 1
        assert cloned.metadata['test'] == 'value'

        # Verify independence (modifying clone doesn't affect original)
        cloned.add_fact(EqualSegment(seg_cd, seg_ab))
        assert len(cloned.fact_base._facts) == 2
        assert len(state.fact_base._facts) == 1

        cloned.goals.append(EqualSegment(seg_ab, seg_ab))
        assert len(cloned.goals) == 2
        assert len(state.goals) == 1

    def test_to_dict(self):
        """Test serialization to dictionary."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        state.add_fact(EqualSegment(seg_ab, seg_cd))
        state.add_goal(EqualSegment(seg_cd, seg_ab))
        state.depth = 3
        state.increment_theorem_usage("theorem1")
        state.metadata['test'] = 'value'

        d = state.to_dict()

        assert len(d['facts']) == 1
        assert len(d['goals']) == 1
        assert d['depth'] == 3
        assert d['theorem_usage'] == {'theorem1': 1}
        assert d['satisfied_goals'] == 0
        assert d['unsatisfied_goals'] == 1
        assert d['metadata'] == {'test': 'value'}

    def test_repr(self):
        """Test string representation."""
        state = ProofState()
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        state.add_fact(EqualSegment(seg_ab, seg_cd))
        state.add_goal(EqualSegment(seg_cd, seg_ab))

        repr_str = repr(state)

        assert 'ProofState' in repr_str
        assert 'facts=1' in repr_str
        assert 'goals=1' in repr_str

    def test_complex_state_workflow(self):
        """Test a complex workflow with multiple operations."""
        state = ProofState()

        # Add initial facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        state.add_facts([
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ])

        # Add goals
        goal1 = EqualSegment(seg_cd, seg_ab)  # Provable by symmetry
        goal2 = EqualSegment(seg_ab, seg_ef)  # Provable by transitivity
        state.add_goals([goal1, goal2])

        # Track theorem usage
        state.increment_theorem_usage("symmetry")

        # Verify initial state
        assert len(state.fact_base._facts) == 2
        assert len(state.goals) == 2
        assert state.all_goals_satisfied() is False

        # Prove first goal
        state.add_fact(goal1)
        assert state.is_goal_satisfied(goal1) is True
        assert len(state.get_satisfied_goals()) == 1

        # Prove second goal
        state.add_fact(goal2)
        state.increment_theorem_usage("transitivity")

        assert state.all_goals_satisfied() is True
        assert len(state.get_satisfied_goals()) == 2
        assert state.get_theorem_usage("symmetry") == 1
        assert state.get_theorem_usage("transitivity") == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
