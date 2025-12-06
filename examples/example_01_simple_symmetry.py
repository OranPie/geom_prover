"""
Example 1: Simple Symmetry Proof
=================================

This example demonstrates the complete pipeline from DSL parsing through
automated proof generation for a simple symmetry proof.

Pipeline: DSL → Semantic → Theorems → Proof → Reasoning
"""

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import EqualSegment
from pathlib import Path

# Step 1: Define geometry problem in DSL
problem = """
# Simple Symmetry Example
# Given: AB = CD
# Prove: CD = AB

Point A, B, C, D
AB = CD
"""

print("=" * 70)
print("EXAMPLE 1: SIMPLE SYMMETRY PROOF")
print("=" * 70)
print("\nProblem (DSL):")
print(problem)

# Step 2: Parse DSL to AST
print("\n" + "=" * 70)
print("STEP 1: PARSING DSL")
print("=" * 70)
lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print(f"✓ Parsed {len(ast.statements)} statements")

# Step 3: Extract semantic information
print("\n" + "=" * 70)
print("STEP 2: SEMANTIC EXTRACTION")
print("=" * 70)
extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print(f"Points: {', '.join(model.points.keys())}")
print(f"Facts extracted: {len(facts)}")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Step 4: Load theorem library
print("\n" + "=" * 70)
print("STEP 3: LOADING THEOREMS")
print("=" * 70)
theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
if theorem_dir.exists():
    engine.load_library(str(theorem_dir))
    print(f"✓ Loaded {len(engine.theorems)} theorems")
    print(f"  Relevant: equality_symmetry, equality_transitivity")
else:
    print("⚠ Theorem library not found, using minimal theorems")
    from geometry_prover.theorems.theorem import TheoremBuilder
    from geometry_prover.theorems.pattern import Variable, PatternTemplate

    symmetry = (TheoremBuilder("symmetry")
                .add_variable(Variable("?AB", "segment"))
                .add_variable(Variable("?CD", "segment"))
                .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                .build())
    engine = TheoremEngine([symmetry])
    print(f"✓ Created {len(engine.theorems)} theorem(s)")

# Step 5: Create goal manually (CD = AB)
print("\n" + "=" * 70)
print("STEP 4: DEFINING GOAL")
print("=" * 70)
if len(facts) > 0 and facts[0].fact_type == "EqualSegment":
    seg1 = facts[0].parameters["segment1"]
    seg2 = facts[0].parameters["segment2"]
    goal = EqualSegment(seg2, seg1)
    goals = [goal]
    print(f"Goal: {goal}")
else:
    goals = []
    print("⚠ No goal could be created")

# Step 6: Run automated proof
print("\n" + "=" * 70)
print("STEP 5: AUTOMATED PROOF GENERATION")
print("=" * 70)
if goals:
    reasoner = BidirectionalReasoner(engine)
    result = reasoner.prove(facts, goals, max_depth=10)

    print(f"\nProof Result:")
    print(f"  Success: {result.success}")
    print(f"  Proven goals: {len(result.proven_goals)}")
    print(f"  Failed goals: {len(result.failed_goals)}")
    print(f"\nStatistics:")
    print(f"  Iterations: {result.statistics['iterations']}")
    print(f"  Forward steps: {result.statistics['forward_steps']}")
    print(f"  Backward steps: {result.statistics['backward_steps']}")
    print(f"  Total facts: {result.statistics['total_facts']}")
    print(f"  Derived facts: {result.statistics['derived_facts']}")
    print(f"  Time: {result.statistics['time_ms']}ms")
    print(f"\nTheorem usage:")
    for theorem, count in result.statistics['theorem_usage'].items():
        print(f"  {theorem}: {count} time(s)")

    if result.success:
        print(f"\n✓ PROOF SUCCESSFUL!")
        print(f"  Proved: {goals[0]}")
    else:
        print(f"\n✗ Proof failed")
else:
    print("⚠ No goals to prove")

print("\n" + "=" * 70)
print("EXAMPLE COMPLETE")
print("=" * 70)
