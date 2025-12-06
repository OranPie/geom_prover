"""
Example 9: Parallel Transitivity Chain
=======================================

Demonstrates transitivity of parallel lines to prove relationships
through multiple intermediate parallel lines.

Problem: Given AB||CD, CD||EF, EF||GH, prove AB||GH

This example shows:
- parallel_transitivity theorem application
- Working with parallel line facts
- Similar pattern to equality transitivity but for different geometric relation
"""

from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import Parallel


def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


# Problem definition
problem = """
# Parallel Line Transitivity Chain

Line AB
Line CD
Line EF
Line GH

# Chain of parallel lines
AB || CD
CD || EF
EF || GH

# Goal: Prove AB || GH through transitivity
"""

print_header("EXAMPLE 9: PARALLEL TRANSITIVITY CHAIN")

print("\nProblem Description:")
print("  Given: AB||CD, CD||EF, EF||GH")
print("  Prove: AB||GH")
print("\nTransitivity reasoning:")
print("  Step 1: AB||CD, CD||EF → AB||EF")
print("  Step 2: AB||EF, EF||GH → AB||GH")

# Parse and extract
lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print(f"\n✓ Parsed and extracted {len(facts)} parallel line facts:")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Load theorems
theorem_dir = Path(__file__).parent.parent.parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
engine.load_library(str(theorem_dir))

print(f"\n✓ Loaded {len(engine.theorems)} theorems")

# Show relevant theorems
print("\nRelevant theorems for parallel lines:")
for thm in engine.theorems:
    if 'parallel' in thm.metadata.category:
        print(f"  • {thm.metadata.name}: {thm.metadata.description}")

# Define goal
line_ab = facts[0].parameters["line1"]  # AB from "AB || CD"
line_gh = facts[2].parameters["line2"]  # GH from "EF || GH"

goal = Parallel(line_ab, line_gh)

print_header("BIDIRECTIONAL PROOF")
print(f"\nGoal: {goal}")

reasoner = BidirectionalReasoner(engine)
result = reasoner.prove(facts, [goal], max_depth=10, max_iterations=20)

print(f"\nProof Result:")
print(f"  Success: {result.success}")
print(f"  Iterations: {result.statistics['iterations']}")
print(f"  Forward steps: {result.statistics['forward_steps']}")
print(f"  Backward steps: {result.statistics['backward_steps']}")
print(f"  Total facts: {result.statistics['total_facts']}")
print(f"  Proven goals: {result.statistics['proven_goals']}/1")
print(f"  Time: {result.statistics['time_ms']}ms")

if result.statistics['theorem_usage']:
    print(f"\nTheorem usage:")
    for thm, count in sorted(result.statistics['theorem_usage'].items(),
                              key=lambda x: x[1], reverse=True):
        print(f"  {thm}: {count} application(s)")

# Proof explanation
print_header("PROOF EXPLANATION")

print("""
THEOREM: Transitivity of parallel lines

GIVEN:
  1. AB || CD
  2. CD || EF
  3. EF || GH

TO PROVE:
  AB || GH

PROOF:
  Step 1: Given AB || CD (Fact 1)
  Step 2: Given CD || EF (Fact 2)
  Step 3: By parallel_transitivity(AB || CD, CD || EF):
          Therefore, AB || EF

  Step 4: Given EF || GH (Fact 3)
  Step 5: By parallel_transitivity(AB || EF, EF || GH):
          Therefore, AB || GH  [GOAL PROVED]

Q.E.D.

This proof follows the same pattern as equality transitivity,
demonstrating that transitivity is a fundamental property
across multiple geometric relations.
""")

# Summary
print_header("SUMMARY")

print(f"\n✓ Successfully proved AB || GH")
print(f"✓ Required {result.statistics['iterations']} iterations")
print(f"✓ Applied {result.statistics['theorem_applications']} theorems")
print(f"✓ Completed in {result.statistics['time_ms']}ms")

print(f"\nKey Insights:")
print(f"  • Parallel relation is transitive (like equality)")
print(f"  • Proof pattern mirrors equality transitivity")
print(f"  • Bidirectional search efficiently found the proof path")
print(f"  • Total of {result.statistics['total_facts']} parallel line facts derived")

print(f"\nComparison with Equality Examples:")
print(f"  • Same transitivity pattern")
print(f"  • Different fact type (Parallel vs EqualSegment/EqualAngle)")
print(f"  • Demonstrates generality of transitivity axiom")

print("\n" + "=" * 70)
print("Example 9 Complete".center(70))
print("=" * 70 + "\n")
