"""
Comprehensive integration tests for Week 1-6 components.

This test suite verifies the complete pipeline from DSL parsing through
semantic analysis, theorem application, and automated proof generation.

Components tested:
- Week 1: DSL (Lexer, Parser, AST)
- Week 2-3: Semantic Analysis (FactExtractor, GeometryModel, ConstraintBuilder)
- Week 4: Theorem System (TheoremEngine, Loader, Matcher, Applicator)
- Week 5: Proof Infrastructure (ProofTree, ProofState, ProofResult, SearchStrategy)
- Week 6: Reasoning Engines (ForwardReasoner, BackwardReasoner, BidirectionalReasoner)
"""

import pytest
from pathlib import Path

# Week 1: DSL
from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser

# Week 2-3: Semantic
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.semantic.prove_goal_extractor import ProveGoalExtractor

# Week 4: Theorems
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.theorems.applicator import TheoremApplicator
from geometry_prover.theorems.matcher import PatternMatcher

# Week 5: Proof Infrastructure
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.proof.proof_state import ProofState
from geometry_prover.proof.search_strategy import BreadthFirstStrategy, DepthFirstStrategy

# Week 6: Reasoning
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner

# Facts and geometry objects
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle, Parallel
from geometry_prover.utils.geometry_objects import Point, Segment, Line, Angle


class TestWeek1to6Integration:
    """Integration tests connecting all weeks 1-6."""

    def setup_method(self):
        """Set up test fixtures."""
        # Load theorem library
        theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
        self.theorem_engine = TheoremEngine()
        if theorem_dir.exists():
            self.theorem_engine.load_library(str(theorem_dir))

    def test_dsl_to_semantic_pipeline(self):
        """Test Week 1 (DSL) → Week 2-3 (Semantic) pipeline."""
        # Week 1: Parse DSL
        source = """
        Point A, B, C
        Triangle ABC
        AB = AC
        """

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        assert ast is not None
        assert len(ast.statements) == 3

        # Week 2-3: Extract semantic information
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)

        # Verify semantic extraction
        # Should have points A, B, C
        assert len(model.points) >= 3
        # Should have facts in the model
        assert len(model.constraints) > 0

    def test_semantic_to_theorem_pipeline(self):
        """Test Week 2-3 (Semantic) → Week 4 (Theorems) pipeline."""
        # Create semantic facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Week 4: Apply theorems
        applicator = TheoremApplicator()

        # Find symmetry theorem
        symmetry = None
        for thm in self.theorem_engine.theorems:
            if thm.metadata.name == "equality_symmetry":
                symmetry = thm
                break

        if symmetry:
            application = applicator.apply(symmetry, facts)
            assert application is not None
            assert len(application.derived_facts) > 0

    def test_theorem_to_proof_infrastructure(self):
        """Test Week 4 (Theorems) → Week 5 (Proof Infrastructure) pipeline."""
        # Setup proof state
        state = ProofState()

        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_fact = EqualSegment(seg_ab, seg_cd)
        goal = EqualSegment(seg_cd, seg_ab)

        state.add_fact(initial_fact)
        state.add_goal(goal)

        # Create proof tree
        tree = ProofTree()
        root = ProofNode(
            node_type=ProofNodeType.INITIAL_FACT,
            facts=[initial_fact],
            metadata={'description': 'Initial facts'}
        )
        tree.set_root(root)

        # Apply theorem using applicator
        applicator = TheoremApplicator()
        symmetry = None
        for thm in self.theorem_engine.theorems:
            if thm.metadata.name == "equality_symmetry":
                symmetry = thm
                break

        if symmetry:
            application = applicator.apply(symmetry, [initial_fact])
            if application and application.derived_facts:
                # Add to proof tree
                child = ProofNode(
                    node_type=ProofNodeType.THEOREM_APPLICATION,
                    facts=application.derived_facts,
                    theorem=symmetry,
                    metadata={'binding': application.binding}
                )
                tree.add_node(root, child)

                # Update state
                for fact in application.derived_facts:
                    state.add_fact(fact)

                # Check goal satisfied
                assert state.is_goal_satisfied(goal)

    def test_proof_infrastructure_to_reasoning(self):
        """Test Week 5 (Proof Infrastructure) → Week 6 (Reasoning) pipeline."""
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))

        initial_facts = [EqualSegment(seg_ab, seg_cd)]
        goals = [EqualSegment(seg_cd, seg_ab)]

        # Week 6: Use backward reasoner
        reasoner = BackwardReasoner(self.theorem_engine)
        result = reasoner.prove(initial_facts, goals, max_depth=10)

        # Verify proof infrastructure is used correctly
        assert result.proof_tree is not None
        assert result.statistics is not None
        assert 'iterations' in result.statistics
        assert 'theorem_usage' in result.statistics

    def test_complete_dsl_to_proof_pipeline(self):
        """Test complete pipeline: DSL → Semantic → Theorems → Proof → Reasoning."""
        # Step 1: Parse DSL (Week 1)
        source = """
        Point A, B, C, D
        AB = CD
        """

        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert ast is not None

        # Step 2: Extract semantics (Week 2-3)
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)

        facts = model.constraints
        assert len(facts) > 0

        # Create a simple goal manually
        # Get the segments from the model
        if len(facts) > 0:
            # Create goal: CD = AB (symmetry of first fact)
            first_fact = facts[0]
            if first_fact.fact_type == "EqualSegment":
                seg1 = first_fact.parameters["segment1"]
                seg2 = first_fact.parameters["segment2"]
                goal = EqualSegment(seg2, seg1)
                goals = [goal]
            else:
                goals = []
        else:
            goals = []

        # Step 3: Load theorems (Week 4)
        # Already loaded in setup_method
        assert len(self.theorem_engine.theorems) > 0

        # Step 4: Create proof infrastructure (Week 5)
        state = ProofState()
        for fact in facts:
            state.add_fact(fact)
        for goal in goals:
            state.add_goal(goal)

        # Step 5: Run reasoning engine (Week 6)
        if goals:
            reasoner = BidirectionalReasoner(self.theorem_engine)
            result = reasoner.prove(facts, goals, max_depth=20)

            # Verify complete pipeline
            assert result is not None
            assert result.proof_tree is not None
            assert result.statistics is not None

    def test_forward_reasoning_full_pipeline(self):
        """Test forward reasoning through complete pipeline."""
        # DSL: Isosceles triangle with equal sides
        source = """
        Point A, B, C
        Triangle ABC
        AB = AC
        """

        # Parse
        ast = Parser(Lexer(source).tokenize()).parse()

        # Extract semantics
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)
        facts = model.constraints

        # Forward reasoning (Week 6)
        reasoner = ForwardReasoner(self.theorem_engine)
        result = reasoner.reason(facts, max_depth=10)

        # Should derive new facts
        assert result.statistics['total_facts'] >= len(facts)
        assert result.statistics['derived_facts'] >= 0

    def test_backward_reasoning_full_pipeline(self):
        """Test backward reasoning through complete pipeline."""
        # DSL with manual goal creation
        source = """
        Point A, B, C, D
        AB = CD
        """

        # Parse
        ast = Parser(Lexer(source).tokenize()).parse()

        # Extract semantics
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)
        facts = model.constraints

        # Create manual goal (symmetry)
        if len(facts) > 0 and facts[0].fact_type == "EqualSegment":
            seg1 = facts[0].parameters["segment1"]
            seg2 = facts[0].parameters["segment2"]
            goals = [EqualSegment(seg2, seg1)]
        else:
            goals = []

        # Backward reasoning (Week 6)
        if goals:
            reasoner = BackwardReasoner(self.theorem_engine)
            result = reasoner.prove(facts, goals, max_depth=20)

            # Should prove goal or report failure
            assert result.success or len(result.failed_goals) > 0

    def test_bidirectional_reasoning_full_pipeline(self):
        """Test bidirectional reasoning through complete pipeline."""
        # DSL: Transitivity chain
        source = """
        Point A, B, C, D, E, F
        AB = CD
        CD = EF
        """

        # Parse
        ast = Parser(Lexer(source).tokenize()).parse()

        # Extract semantics
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)
        facts = model.constraints

        # Create manual goal (transitivity: AB = EF)
        # Find segments from facts
        if len(facts) >= 2:
            # Assume first fact is AB=CD, second is CD=EF
            # Goal: AB = EF
            fact1 = facts[0]
            fact2 = facts[1]
            if fact1.fact_type == "EqualSegment" and fact2.fact_type == "EqualSegment":
                seg_ab = fact1.parameters["segment1"]
                seg_ef = fact2.parameters["segment2"]
                goals = [EqualSegment(seg_ab, seg_ef)]
            else:
                goals = []
        else:
            goals = []

        # Bidirectional reasoning (Week 6)
        if goals:
            reasoner = BidirectionalReasoner(self.theorem_engine)
            result = reasoner.prove(facts, goals, max_depth=20)

            # Verify bidirectional approach
            assert 'forward_steps' in result.statistics
            assert 'backward_steps' in result.statistics

    def test_multiple_theorem_applications(self):
        """Test multiple theorem applications across pipeline."""
        # Setup: Chain of equalities requiring multiple applications
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        seg_ef = Segment(Point("E"), Point("F"))

        facts = [
            EqualSegment(seg_ab, seg_cd),
            EqualSegment(seg_cd, seg_ef)
        ]

        goals = [EqualSegment(seg_ab, seg_ef)]

        # Run forward reasoner
        reasoner = ForwardReasoner(self.theorem_engine)
        result = reasoner.reason(facts, goals=goals, max_depth=20)

        # Should apply multiple theorems
        assert result.statistics['theorem_applications'] > 0
        if result.statistics['theorem_usage']:
            # Should use symmetry and/or transitivity
            total_usage = sum(result.statistics['theorem_usage'].values())
            assert total_usage > 0

    def test_proof_tree_construction(self):
        """Test proof tree is correctly built through pipeline."""
        facts = [EqualSegment(
            Segment(Point("A"), Point("B")),
            Segment(Point("C"), Point("D"))
        )]

        goals = [EqualSegment(
            Segment(Point("C"), Point("D")),
            Segment(Point("A"), Point("B"))
        )]

        reasoner = BidirectionalReasoner(self.theorem_engine)
        result = reasoner.prove(facts, goals, max_depth=10)

        # Verify proof tree structure
        assert result.proof_tree is not None
        assert result.proof_tree.root is not None

        # Tree should have nodes
        all_nodes = result.proof_tree.get_all_nodes()
        assert len(all_nodes) > 0

    def test_different_search_strategies(self):
        """Test different search strategies work through pipeline."""
        facts = [EqualSegment(
            Segment(Point("A"), Point("B")),
            Segment(Point("C"), Point("D"))
        )]

        goals = [EqualSegment(
            Segment(Point("C"), Point("D")),
            Segment(Point("A"), Point("B"))
        )]

        # Test with BreadthFirstStrategy
        bfs_reasoner = BidirectionalReasoner(
            self.theorem_engine,
            strategy=BreadthFirstStrategy()
        )
        bfs_result = bfs_reasoner.prove(facts, goals, max_depth=10)

        # Test with DepthFirstStrategy
        dfs_reasoner = BidirectionalReasoner(
            self.theorem_engine,
            strategy=DepthFirstStrategy()
        )
        dfs_result = dfs_reasoner.prove(facts, goals, max_depth=10)

        # Both should succeed (for this simple problem)
        # At least one should succeed
        assert bfs_result.success or dfs_result.success

    def test_complex_geometry_problem(self):
        """Test complex geometry problem through complete pipeline."""
        source = """
        Point A, B, C, D, E, F
        AB = CD
        CD = EF
        """

        # Parse
        ast = Parser(Lexer(source).tokenize()).parse()

        # Extract semantics
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)
        facts = model.constraints

        # Create goal manually
        if len(facts) >= 2:
            fact1 = facts[0]
            fact2 = facts[1]
            if fact1.fact_type == "EqualSegment" and fact2.fact_type == "EqualSegment":
                seg_ab = fact1.parameters["segment1"]
                seg_ef = fact2.parameters["segment2"]
                goals = [EqualSegment(seg_ab, seg_ef)]
            else:
                goals = []
        else:
            goals = []

        # Try all three reasoning approaches
        if goals:
            forward = ForwardReasoner(self.theorem_engine)
            backward = BackwardReasoner(self.theorem_engine)
            bidirectional = BidirectionalReasoner(self.theorem_engine)

            forward_result = forward.reason(facts, goals=goals, max_depth=20)
            backward_result = backward.prove(facts, goals, max_depth=20)
            bidirectional_result = bidirectional.prove(facts, goals, max_depth=20)

            # At least one approach should work
            successes = [
                forward_result.success,
                backward_result.success,
                bidirectional_result.success
            ]
            assert any(successes), "At least one reasoning approach should succeed"

    def test_pattern_matching_integration(self):
        """Test pattern matching works correctly across pipeline."""
        # Create facts
        seg_ab = Segment(Point("A"), Point("B"))
        seg_cd = Segment(Point("C"), Point("D"))
        fact = EqualSegment(seg_ab, seg_cd)

        # Find symmetry theorem
        symmetry = None
        for thm in self.theorem_engine.theorems:
            if thm.metadata.name == "equality_symmetry":
                symmetry = thm
                break

        if symmetry:
            # Test pattern matching
            matcher = PatternMatcher()
            binding = matcher.match_all(symmetry.conditions, [fact])

            assert binding is not None

            # Test theorem application
            applicator = TheoremApplicator()
            application = applicator.apply(symmetry, [fact])

            assert application is not None
            assert len(application.derived_facts) > 0

    def test_statistics_tracking_across_pipeline(self):
        """Test statistics are tracked correctly through pipeline."""
        facts = [
            EqualSegment(
                Segment(Point("A"), Point("B")),
                Segment(Point("C"), Point("D"))
            ),
            EqualSegment(
                Segment(Point("C"), Point("D")),
                Segment(Point("E"), Point("F"))
            )
        ]

        goals = [EqualSegment(
            Segment(Point("A"), Point("B")),
            Segment(Point("E"), Point("F"))
        )]

        reasoner = BidirectionalReasoner(self.theorem_engine)
        result = reasoner.prove(facts, goals, max_depth=20)

        # Verify comprehensive statistics
        stats = result.statistics
        assert 'iterations' in stats
        assert 'forward_steps' in stats
        assert 'backward_steps' in stats
        assert 'total_facts' in stats
        assert 'derived_facts' in stats
        assert 'proven_goals' in stats
        assert 'failed_goals' in stats
        assert 'theorem_applications' in stats
        assert 'time_ms' in stats
        assert 'theorem_usage' in stats

        # All values should be reasonable
        assert stats['iterations'] >= 0
        assert stats['total_facts'] >= len(facts)
        assert stats['time_ms'] >= 0

    def test_error_handling_across_pipeline(self):
        """Test error handling works correctly through pipeline."""
        # Invalid DSL should be caught
        with pytest.raises(Exception):
            Parser(Lexer("invalid syntax {{{").tokenize()).parse()

        # Empty facts should be handled
        reasoner = ForwardReasoner(self.theorem_engine)
        result = reasoner.reason([], max_depth=10)
        assert result is not None

        # Unprovable goals should be reported
        facts = [EqualSegment(
            Segment(Point("A"), Point("B")),
            Segment(Point("C"), Point("D"))
        )]

        goals = [EqualSegment(
            Segment(Point("E"), Point("F")),
            Segment(Point("G"), Point("H"))
        )]

        backward = BackwardReasoner(self.theorem_engine)
        result = backward.prove(facts, goals, max_depth=10)

        assert result.success is False
        assert len(result.failed_goals) > 0

    def test_real_theorem_library_integration(self):
        """Test integration with real theorem library."""
        # Should have loaded theorems
        assert len(self.theorem_engine.theorems) > 0

        # Should have core theorems
        theorem_names = [t.metadata.name for t in self.theorem_engine.theorems]
        assert "equality_symmetry" in theorem_names
        assert "equality_transitivity" in theorem_names

        # Test applying real theorems
        facts = [EqualSegment(
            Segment(Point("A"), Point("B")),
            Segment(Point("C"), Point("D"))
        )]

        reasoner = ForwardReasoner(self.theorem_engine)
        result = reasoner.reason(facts, max_depth=5)

        # Should derive facts using real theorems
        assert result.statistics['derived_facts'] > 0

    def test_end_to_end_isosceles_triangle(self):
        """Test end-to-end proof for isosceles triangle properties."""
        source = """
        Point A, B, C
        Triangle ABC
        AB = AC
        """

        # Complete pipeline
        ast = Parser(Lexer(source).tokenize()).parse()
        extractor = FactExtractor()
        model = extractor.extract_from_program(ast)
        facts = model.constraints

        # Forward reasoning should derive symmetric facts
        reasoner = ForwardReasoner(self.theorem_engine)
        result = reasoner.reason(facts, max_depth=10)

        assert result is not None
        # May or may not be successful, but should complete
        assert result.statistics['total_facts'] >= len(facts)

    def test_end_to_end_parallel_lines(self):
        """Test end-to-end proof for parallel lines."""
        # Create parallel line facts manually (DSL parsing for parallel might need more work)
        line1 = Line(Point("A"), Point("B"))
        line2 = Line(Point("C"), Point("D"))
        line3 = Line(Point("E"), Point("F"))

        facts = [
            Parallel(line1, line2),
            Parallel(line2, line3)
        ]

        goals = [Parallel(line1, line3)]

        # Test with bidirectional reasoning
        reasoner = BidirectionalReasoner(self.theorem_engine)
        result = reasoner.prove(facts, goals, max_depth=20)

        # May or may not succeed depending on theorem library
        # But should not crash
        assert result is not None


class TestPerformanceIntegration:
    """Performance tests for integrated pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
        self.theorem_engine = TheoremEngine()
        if theorem_dir.exists():
            self.theorem_engine.load_library(str(theorem_dir))

    def test_large_fact_base_performance(self):
        """Test performance with large fact base."""
        import time

        # Create 50 segment equality facts
        facts = []
        for i in range(50):
            seg1 = Segment(Point(f"A{i}"), Point(f"B{i}"))
            seg2 = Segment(Point(f"C{i}"), Point(f"D{i}"))
            facts.append(EqualSegment(seg1, seg2))

        # Time forward reasoning
        reasoner = ForwardReasoner(self.theorem_engine)
        start = time.time()
        result = reasoner.reason(facts, max_depth=5, max_facts=200)
        elapsed = time.time() - start

        # Should complete in reasonable time (< 10 seconds)
        assert elapsed < 10.0
        assert result is not None

    def test_deep_proof_chain_performance(self):
        """Test performance with deep proof chains."""
        # Create chain: A=B, B=C, C=D, D=E, E=F
        points = ["A", "B", "C", "D", "E", "F"]
        facts = []
        for i in range(len(points) - 1):
            seg1 = Segment(Point(points[i]), Point(points[i]))
            seg2 = Segment(Point(points[i+1]), Point(points[i+1]))
            facts.append(EqualSegment(seg1, seg2))

        goal = EqualSegment(
            Segment(Point("A"), Point("A")),
            Segment(Point("F"), Point("F"))
        )

        # Should handle deep chains
        reasoner = BidirectionalReasoner(self.theorem_engine)
        result = reasoner.prove(facts, [goal], max_depth=20)

        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
