"""
Tests for forward reasoning engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 8 - Test forward reasoning
"""

import pytest
from pathlib import Path

from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.facts.fact_types import (
    EqualSegment,
    EqualAngle,
    Parallel,
    Triangle,
    CongruentTriangle,
    SimilarTriangle,
)
from geometry_prover.utils.geometry_objects import Point, Segment, Angle, Line
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate
from geometry_prover.proof.search_strategy import BreadthFirstStrategy, DepthFirstStrategy


class TestForwardReasoner:
    """Test ForwardReasoner class."""

    def test_create_reasoner(self):
        """Test creating a forward reasoner."""
        engine = TheoremEngine()
        reasoner = ForwardReasoner(engine)

        assert reasoner.theorem_engine == engine
        assert reasoner.strategy is not None
        assert isinstance(reasoner.strategy, BreadthFirstStrategy)

    def test_create_reasoner_with_strategy(self):
        """Test creating reasoner with custom strategy."""
        engine = TheoremEngine()
        strategy = DepthFirstStrategy()
        reasoner = ForwardReasoner(engine, strategy=strategy)

        assert reasoner.strategy == strategy

    def test_reason_simple_derivation(self):
        """Test simple forward reasoning with symmetry."""
        # Create simple symmetry theorem
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        # Initial fact: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Run forward reasoning
        result = reasoner.reason(initial_facts, max_depth=5)

        # Should derive CD = AB
        assert result.success is True
        assert len(result.proof_tree.get_all_nodes()) >= 2  # Root + at least one application
        assert result.statistics['derived_facts'] >= 1
        assert result.statistics['theorem_applications'] >= 1

    def test_reason_with_goals(self):
        """Test forward reasoning with specific goals."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        result = reasoner.reason(initial_facts, goals=goals, max_depth=5)

        # Goal should be proven
        assert result.success is True
        assert len(result.proven_goals) == 1
        assert len(result.failed_goals) == 0

    def test_reason_no_applicable_theorems(self):
        """Test reasoning when no theorems apply."""
        # Create angle theorem (won't match segment facts)
        theorem = (TheoremBuilder("angle_symmetry")
                   .add_variable(Variable("?ABC", "angle"))
                   .add_variable(Variable("?DEF", "angle"))
                   .add_condition(PatternTemplate.equal_angle("?ABC", "?DEF"))
                   .add_conclusion(PatternTemplate.equal_angle("?DEF", "?ABC"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        # Provide segment fact (won't match angle theorem)
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = reasoner.reason(initial_facts, max_depth=5)

        # Should converge immediately with no derivations
        assert result.statistics['derived_facts'] == 0
        assert result.statistics['theorem_applications'] == 0
        assert result.statistics['converged'] is True

    def test_reason_max_depth_limit(self):
        """Test that max_depth limit is respected."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        # Very low depth limit
        result = reasoner.reason(initial_facts, max_depth=1)

        assert result.statistics['iterations'] <= 1

    def test_reason_still_runs_on_depth_boundary(self):
        """The first iteration should execute when max_depth is 1."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = reasoner.reason(initial_facts, max_depth=1)

        assert result.statistics['iterations'] == 1
        assert result.statistics['derived_facts'] >= 1

    def test_reason_max_facts_limit(self):
        """Test that max_facts limit is respected."""
        # Create theorems that could generate many facts
        symmetry = (TheoremBuilder("symmetry")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        engine = TheoremEngine([symmetry])
        reasoner = ForwardReasoner(engine)

        # Multiple initial facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Low fact limit
        result = reasoner.reason(initial_facts, max_facts=5)

        assert result.statistics['total_facts'] <= 5

    def test_can_derive_true(self):
        """Test can_derive returns True when goal is derivable."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_cd, seg_ab)

        # Should be able to derive goal
        can_derive = reasoner.can_derive(initial_facts, goal)
        assert can_derive is True

    def test_can_derive_false(self):
        """Test can_derive returns False when goal is not derivable."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goal = EqualSegment(seg_ef, seg_ab)  # Not derivable

        can_derive = reasoner.can_derive(initial_facts, goal)
        assert can_derive is False

    def test_reason_with_real_theorem_library(self):
        """Test forward reasoning with actual theorem library."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        reasoner = ForwardReasoner(engine)

        # Initial facts: AB = CD, CD = EF
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        initial_facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Run forward reasoning
        result = reasoner.reason(initial_facts, max_depth=10)

        # Should derive multiple facts via symmetry and transitivity
        assert result.success is True
        assert result.statistics['derived_facts'] >= 2
        assert result.statistics['theorem_applications'] >= 2

        # Check that both symmetry and transitivity were used
        theorem_names = set(result.statistics['theorem_usage'].keys())
        assert 'equality_symmetry' in theorem_names or 'equality_transitivity' in theorem_names

    def test_proof_tree_structure(self):
        """Test that proof tree is built correctly."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = reasoner.reason(initial_facts, max_depth=5)

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
        reasoner = ForwardReasoner(engine)

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        initial_facts = [EqualSegment(seg_ab, seg_cd)]

        result = reasoner.reason(initial_facts, max_depth=5)

        # Check statistics
        stats = result.statistics
        assert 'iterations' in stats
        assert 'total_facts' in stats
        assert 'derived_facts' in stats
        assert 'theorem_applications' in stats
        assert 'time_ms' in stats
        assert 'theorem_usage' in stats
        assert 'converged' in stats

        assert stats['total_facts'] >= len(initial_facts)
        assert stats['derived_facts'] == stats['total_facts'] - len(initial_facts)

    def test_sss_congruence_yields_similarity(self):
        """SSS congruence should derive congruent and similar triangles."""

        theorem_dir = (
            Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
        )
        engine = TheoremEngine()
        if theorem_dir.exists():
            engine.load_library(str(theorem_dir))

        reasoner = ForwardReasoner(engine)

        # Triangles ABC and DEF with all three pairs of equal sides (SSS)
        a, b, c = Point("A"), Point("B"), Point("C")
        d, e, f = Point("D"), Point("E"), Point("F")

        triangle_facts = [Triangle(a, b, c), Triangle(d, e, f)]
        equality_facts = [
            EqualSegment(Segment(a, b), Segment(d, e)),
            EqualSegment(Segment(b, c), Segment(e, f)),
            EqualSegment(Segment(c, a), Segment(f, d)),
        ]

        result = reasoner.reason(triangle_facts + equality_facts, max_depth=8, max_facts=100)

        assert result.success is True

        derived_facts = []
        if result.proof_tree:
            for node in result.proof_tree.get_all_nodes():
                derived_facts.extend(node.facts)

        assert any(isinstance(f, CongruentTriangle) for f in derived_facts)
        assert any(isinstance(f, SimilarTriangle) for f in derived_facts)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
