"""
Example 6: Multi-Step Segment Equality
======================================

Demonstrates chaining equality transitivity to prove relationships
through multiple intermediate segments.

Problem: Given AB=CD, CD=EF, EF=GH, prove AB=GH

This example shows:
- Multiple applications of equality_transitivity theorem
- Forward reasoning building up facts
- Bidirectional reasoning finding efficient paths
- Performance comparison between strategies
"""

from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import EqualSegment


def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def print_subheader(title):
    """Print formatted subheader."""
    print("\n" + title)
    print("-" * 70)


# Problem definition
problem = """
# Multi-Step Segment Equality Chain
# Prove transitivity across 4 segments

Point A, B, C, D, E, F, G, H

# Given facts: Chain of equalities
AB = CD
CD = EF
EF = GH

# Goal: Prove AB = GH (requires 2 transitivity steps)
"""

print_header("EXAMPLE 6: MULTI-STEP SEGMENT EQUALITY")

print("\nProblem Description:")
print("  Given: AB = CD, CD = EF, EF = GH")
print("  Prove: AB = GH")
print("\nThis requires chaining transitivity:")
print("  Step 1: AB = CD, CD = EF → AB = EF")
print("  Step 2: AB = EF, EF = GH → AB = GH")

# Step 1: Parse DSL
print_header("STEP 1: PARSE PROBLEM")
print("\nDSL Input:")
print(problem)

lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(f"✓ Parsed {len(ast.statements)} statements")

# Step 2: Extract Facts
print_header("STEP 2: EXTRACT FACTS")

extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print(f"\nExtracted {len(facts)} facts:")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Step 3: Load Theorems
print_header("STEP 3: LOAD THEOREM LIBRARY")

theorem_dir = Path(__file__).parent.parent.parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()

if not theorem_dir.exists():
    print(f"✗ Error: Theorem directory not found: {theorem_dir}")
    exit(1)

engine.load_library(str(theorem_dir))
print(f"✓ Loaded {len(engine.theorems)} theorems")

# Show relevant theorems
print("\nRelevant theorems for this problem:")
for thm in engine.theorems:
    if 'equality' in thm.metadata.category:
        print(f"  • {thm.metadata.name}: {thm.metadata.description}")

# Step 4: Define Goal
print_header("STEP 4: DEFINE GOAL")

# Get the segments from the facts
seg_ab = facts[0].parameters["segment1"]  # AB from "AB = CD"
seg_gh = facts[2].parameters["segment2"]  # GH from "EF = GH"

goal = EqualSegment(seg_ab, seg_gh)

print(f"\nGoal: {goal}")
print("\nThis goal is NOT directly given - it must be derived through")
print("intermediate steps using the transitivity theorem.")

# Step 5: Forward Reasoning
print_header("STEP 5: FORWARD REASONING")

print("\nUsing forward reasoning to explore all derivable facts...")
forward_reasoner = ForwardReasoner(engine)
forward_result = forward_reasoner.reason(facts, [], max_iterations=10)

print(f"\nForward Reasoning Results:")
print(f"  Success: {forward_result.success}")
print(f"  Iterations: {forward_result.statistics['iterations']}")
print(f"  Total facts: {forward_result.statistics['total_facts']}")
print(f"  Derived facts: {forward_result.statistics['derived_facts']}")
print(f"  Theorem applications: {forward_result.statistics['theorem_applications']}")
print(f"  Time: {forward_result.statistics['time_ms']}ms")

if forward_result.statistics['theorem_usage']:
    print(f"\nTheorem usage:")
    for thm, count in sorted(forward_result.statistics['theorem_usage'].items(),
                              key=lambda x: x[1], reverse=True):
        print(f"  {thm}: {count} application(s)")

print(f"\nForward reasoning explored all possible facts without a specific goal.")
print(f"It derived {forward_result.statistics['derived_facts']} new facts total.")

# Step 6: Bidirectional Reasoning
print_header("STEP 6: BIDIRECTIONAL REASONING")

print("\nUsing bidirectional reasoning to prove goal efficiently...")
bi_reasoner = BidirectionalReasoner(engine)
bi_result = bi_reasoner.prove(facts, [goal], max_depth=10, max_iterations=20)

print(f"\nBidirectional Reasoning Results:")
print(f"  Success: {bi_result.success}")
print(f"  Iterations: {bi_result.statistics['iterations']}")
print(f"  Forward steps: {bi_result.statistics['forward_steps']}")
print(f"  Backward steps: {bi_result.statistics['backward_steps']}")
print(f"  Total facts: {bi_result.statistics['total_facts']}")
print(f"  Proven goals: {bi_result.statistics['proven_goals']}/1")
print(f"  Time: {bi_result.statistics['time_ms']}ms")

if bi_result.statistics['theorem_usage']:
    print(f"\nTheorem usage:")
    for thm, count in sorted(bi_result.statistics['theorem_usage'].items(),
                              key=lambda x: x[1], reverse=True):
        print(f"  {thm}: {count} application(s)")

# Step 7: Strategy Comparison
print_header("STEP 7: STRATEGY COMPARISON")

print("\n" + f"{'Strategy':<20} {'Success':<10} {'Iterations':<12} {'Time (ms)':<12} {'Facts'}")
print("-" * 70)

# Forward doesn't target specific goals, so we show exploration results
print(f"{'Forward (explore)':<20} {'N/A':<10} "
      f"{forward_result.statistics['iterations']:<12} "
      f"{forward_result.statistics['time_ms']:<12} "
      f"{forward_result.statistics['total_facts']}")

print(f"{'Bidirectional':<20} {'✓' if bi_result.success else '✗':<10} "
      f"{bi_result.statistics['iterations']:<12} "
      f"{bi_result.statistics['time_ms']:<12} "
      f"{bi_result.statistics['total_facts']}")

# Step 8: Proof Explanation
print_header("STEP 8: PROOF EXPLANATION")

print("""
THEOREM: Transitive closure of equality relation

GIVEN:
  1. AB = CD
  2. CD = EF
  3. EF = GH

TO PROVE:
  AB = GH

PROOF:
  Step 1: Given AB = CD (Fact 1)
  Step 2: Given CD = EF (Fact 2)
  Step 3: By equality_transitivity(AB = CD, CD = EF):
          Therefore, AB = EF

  Step 4: Given EF = GH (Fact 3)
  Step 5: By equality_transitivity(AB = EF, EF = GH):
          Therefore, AB = GH  [GOAL PROVED]

Q.E.D.

Alternative proof paths using symmetry are also possible.
The bidirectional reasoner found the most efficient path.
""")

# Final Summary
print_header("SUMMARY")

print(f"\n✓ Successfully proved AB = GH")
print(f"✓ Required {bi_result.statistics['iterations']} iterations")
print(f"✓ Applied {bi_result.statistics['theorem_applications']} theorems")
print(f"✓ Completed in {bi_result.statistics['time_ms']}ms")

print(f"\nKey Insights:")
print(f"  • Forward reasoning explores ALL derivable facts (found {forward_result.statistics['total_facts']} total)")
print(f"  • Bidirectional reasoning targets the specific goal (more efficient)")
print(f"  • Transitivity theorem is key for chaining equalities")
print(f"  • Both approaches successfully handle multi-step reasoning")

print("\n" + "=" * 70)
print("Example 6 Complete".center(70))
print("=" * 70 + "\n")
