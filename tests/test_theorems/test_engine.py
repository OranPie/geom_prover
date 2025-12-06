"""
Tests for theorem engine.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 20 - Test theorem engine
"""

import pytest
from pathlib import Path

from geometry_prover.theorems.engine import TheoremEngine, DerivationStep, ForwardChainResult
from geometry_prover.theorems.theorem import TheoremBuilder
from geometry_prover.theorems.pattern import Variable, PatternTemplate
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle
from geometry_prover.utils.geometry_objects import Point, Segment, Angle


class TestTheoremEngine:
    """Test TheoremEngine class."""

    def test_create_empty_engine(self):
        """Test creating empty engine."""
        engine = TheoremEngine()
        assert len(engine.theorems) == 0
        assert len(engine.list_theorems()) == 0

    def test_create_engine_with_theorems(self):
        """Test creating engine with initial theorems."""
        theorem = (TheoremBuilder("test")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])
        assert len(engine.theorems) == 1
        assert "test" in engine.list_theorems()

    def test_add_theorem(self):
        """Test adding theorem to engine."""
        engine = TheoremEngine()

        theorem = (TheoremBuilder("test")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine.add_theorem(theorem)
        assert len(engine.theorems) == 1

    def test_get_theorem(self):
        """Test getting theorem by name."""
        theorem = (TheoremBuilder("test_theorem")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])

        found = engine.get_theorem("test_theorem")
        assert found is not None
        assert found.metadata.name == "test_theorem"

        not_found = engine.get_theorem("nonexistent")
        assert not_found is None

    def test_forward_chain_single_step(self):
        """Test forward chaining with single derivation step."""
        # Create symmetry theorem: AB = CD => CD = AB
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])

        # Initial facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Forward chain
        result = engine.forward_chain(facts)

        # Should derive one new fact (CD = AB)
        assert len(result.initial_facts) == 1
        assert len(result.derived_facts) == 1
        assert len(result.all_facts) == 2
        assert len(result.derivation_steps) == 1
        assert result.converged is True

    def test_forward_chain_multiple_steps(self):
        """Test forward chaining with multiple steps (transitivity)."""
        # Create two theorems: symmetry and transitivity
        symmetry = (TheoremBuilder("symmetry")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        transitivity = (TheoremBuilder("transitivity")
                       .add_variable(Variable("?AB", "segment"))
                       .add_variable(Variable("?CD", "segment"))
                       .add_variable(Variable("?EF", "segment"))
                       .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                       .add_condition(PatternTemplate.equal_segment("?CD", "?EF"))
                       .add_conclusion(PatternTemplate.equal_segment("?AB", "?EF"))
                       .build())

        engine = TheoremEngine([symmetry, transitivity])

        # Initial facts: AB = CD and CD = EF
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        # Forward chain
        result = engine.forward_chain(facts, max_iterations=10)

        # Should derive multiple facts through chaining
        # CD = AB (symmetry), AB = EF (transitivity)
        assert len(result.derived_facts) >= 2
        assert result.converged is True

    def test_forward_chain_no_derivations(self):
        """Test forward chaining when no theorems apply."""
        # Create theorem that won't match
        theorem = (TheoremBuilder("test")
                   .add_variable(Variable("?ABC", "angle"))
                   .add_variable(Variable("?DEF", "angle"))
                   .add_condition(PatternTemplate.equal_angle("?ABC", "?DEF"))
                   .add_conclusion(PatternTemplate.equal_angle("?DEF", "?ABC"))
                   .build())

        engine = TheoremEngine([theorem])

        # Provide segment facts (won't match angle theorem)
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        result = engine.forward_chain(facts)

        # No derivations
        assert len(result.derived_facts) == 0
        assert len(result.derivation_steps) == 0
        assert result.iterations == 1
        assert result.converged is True

    def test_forward_chain_deduplication(self):
        """Test that forward chaining doesn't create duplicate facts."""
        # Reflexive theorem: AB = AB => AB = AB
        theorem = (TheoremBuilder("reflexive")
                   .add_variable(Variable("?AB", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?AB"))
                   .add_conclusion(PatternTemplate.equal_segment("?AB", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])

        seg_ab = Segment(Point("A"), Point("B"))
        facts = [EqualSegment(seg_ab, seg_ab)]

        result = engine.forward_chain(facts, max_iterations=5)

        # Should not create duplicates
        assert len(result.all_facts) == 1  # Only the initial fact
        assert len(result.derived_facts) == 0

    def test_forward_chain_max_iterations(self):
        """Test that forward chaining respects max_iterations."""
        symmetry = (TheoremBuilder("symmetry")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        engine = TheoremEngine([symmetry])

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Limit iterations
        result = engine.forward_chain(facts, max_iterations=1)

        assert result.iterations <= 1

    def test_forward_chain_max_facts(self):
        """Test that forward chaining respects max_facts limit."""
        symmetry = (TheoremBuilder("symmetry")
                    .add_variable(Variable("?AB", "segment"))
                    .add_variable(Variable("?CD", "segment"))
                    .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                    .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                    .build())

        engine = TheoremEngine([symmetry])

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Limit total facts
        result = engine.forward_chain(facts, max_facts=5)

        assert len(result.all_facts) <= 5

    def test_apply_single_theorem(self):
        """Test applying a specific theorem by name."""
        theorem = (TheoremBuilder("symmetry")
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?CD", "segment"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                   .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                   .build())

        engine = TheoremEngine([theorem])

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        result = engine.apply_single_theorem("symmetry", facts)

        assert result is not None
        assert len(result.derived_facts) == 1

    def test_apply_single_theorem_not_found(self):
        """Test applying non-existent theorem."""
        engine = TheoremEngine()
        result = engine.apply_single_theorem("nonexistent", [])
        assert result is None

    def test_get_theorems_by_category(self):
        """Test getting theorems by category."""
        th1 = (TheoremBuilder("th1")
               .category("equality")
               .add_variable(Variable("?AB", "segment"))
               .add_variable(Variable("?CD", "segment"))
               .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
               .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
               .build())

        th2 = (TheoremBuilder("th2")
               .category("equality")
               .add_variable(Variable("?AB", "segment"))
               .add_variable(Variable("?CD", "segment"))
               .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
               .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
               .build())

        th3 = (TheoremBuilder("th3")
               .category("angles")
               .add_variable(Variable("?ABC", "angle"))
               .add_variable(Variable("?DEF", "angle"))
               .add_condition(PatternTemplate.equal_angle("?ABC", "?DEF"))
               .add_conclusion(PatternTemplate.equal_angle("?DEF", "?ABC"))
               .build())

        engine = TheoremEngine([th1, th2, th3])

        equality_theorems = engine.get_theorems_by_category("equality")
        assert len(equality_theorems) == 2

        angle_theorems = engine.get_theorems_by_category("angles")
        assert len(angle_theorems) == 1

    def test_derivation_step_repr(self):
        """Test DerivationStep repr."""
        step = DerivationStep(
            theorem_name="test",
            derived_facts=[],
            step_number=1
        )

        repr_str = repr(step)
        assert "Step 1" in repr_str
        assert "test" in repr_str

    def test_forward_chain_result_repr(self):
        """Test ForwardChainResult repr."""
        result = ForwardChainResult(
            initial_facts=[],
            all_facts=[],
            derived_facts=[],
            derivation_steps=[],
            iterations=1,
            converged=True
        )

        repr_str = repr(result)
        assert "ForwardChainResult" in repr_str
        assert "converged=True" in repr_str


class TestLoadTheoremLibrary:
    """Test loading actual theorem library."""

    def test_load_theorem_library(self):
        """Test loading theorem library from directory."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        count = engine.load_library(str(theorem_dir))

        # Should load 13 theorems (10 core + 3 examples)
        assert count >= 13
        assert len(engine.theorems) >= 13

    def test_forward_chain_with_loaded_library(self):
        """Test forward chaining with loaded theorem library."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        engine = TheoremEngine()
        engine.load_library(str(theorem_dir))

        # Create initial facts: AB = CD
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Forward chain
        result = engine.forward_chain(facts, max_iterations=10)

        # Should derive at least the symmetric fact (CD = AB)
        assert len(result.derived_facts) >= 1
        assert result.converged is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
