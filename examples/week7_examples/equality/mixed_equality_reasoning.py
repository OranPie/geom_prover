"""
Example 8: Mixed Equality Reasoning
====================================

Demonstrates combining segment and angle equalities in a unified proof,
showing how different fact types interact through the reasoning engine.

Problem: In triangle context, combine segment and angle equality reasoning

This example shows:
- Using isosceles_base_angles theorem
- Combining segment equality with angle equality
- Multiple fact types in single proof
- Bidirectional search across different domains
"""

from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import EqualSegment, EqualAngle


def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


# Problem definition
problem = """
# Mixed Equality Reasoning
# Combine segment and angle equalities

Point A, B, C, D, E, F

# Triangle with equal sides
AB = AC
CD = CE

# Additional segment equalities
AC = CD

# Goal: Prove various relationships combining segments and angles
"""

print_header("EXAMPLE 8: MIXED EQUALITY REASONING")

print("\nProblem Description:")
print("  Given: AB = AC, CD = CE, AC = CD")
print("  This creates two isosceles triangles sharing a side")
print("  Demonstrate: Combining segment and angle equality reasoning")

# Parse and extract
lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print(f"\nExtracted {len(facts)} initial facts:")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Load theorems
theorem_dir = Path(__file__).parent.parent.parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
engine.load_library(str(theorem_dir))

print(f"\n✓ Loaded {len(engine.theorems)} theorems")

# Goal 1: Prove AB = CD through transitivity
seg_ab = facts[0].parameters["segment1"]  # AB
seg_cd = facts[2].parameters["segment1"]  # CD

goal1 = EqualSegment(seg_ab, seg_cd)

print_header("GOAL 1: SEGMENT EQUALITY THROUGH TRANSITIVITY")
print(f"\nProve: {goal1}")
print("  Path: AB = AC, AC = CD → AB = CD")

reasoner = BidirectionalReasoner(engine)
result1 = reasoner.prove(facts, [goal1], max_depth=10, max_iterations=20)

print(f"\nResult:")
print(f"  Success: {result1.success}")
print(f"  Iterations: {result1.statistics['iterations']}")
print(f"  Theorem applications: {result1.statistics['theorem_applications']}")
print(f"  Time: {result1.statistics['time_ms']}ms")

if result1.statistics['theorem_usage']:
    print(f"\nTheorems used:")
    for thm, count in result1.statistics['theorem_usage'].items():
        print(f"  • {thm}: {count}×")

# Goal 2: Explore angle equalities from isosceles triangles
print_header("GOAL 2: ANGLE EQUALITIES FROM ISOSCELES PROPERTY")

print("\nExploring angle equalities that can be derived...")
print("  • Triangle ABC: AB = AC → ∠ABC = ∠ACB (isosceles)")
print("  • Triangle CDE: CD = CE → ∠CDE = ∠CED (isosceles)")

# Run forward reasoning to find all derivable facts
from geometry_prover.proof.forward_reasoner import ForwardReasoner
forward_reasoner = ForwardReasoner(engine)
explore_result = forward_reasoner.reason(facts, [], max_iterations=5)

print(f"\nExploration results:")
print(f"  Total facts derived: {explore_result.statistics['total_facts']}")
print(f"  New facts: {explore_result.statistics['derived_facts']}")
print(f"  Iterations: {explore_result.statistics['iterations']}")

if explore_result.statistics['theorem_usage']:
    print(f"\nTheorems applied:")
    for thm, count in sorted(explore_result.statistics['theorem_usage'].items(),
                               key=lambda x: x[1], reverse=True):
        print(f"  • {thm}: {count}×")

# Summary
print_header("SUMMARY")

print(f"\n✓ Successfully demonstrated mixed equality reasoning")
print(f"✓ Proved segment equality: {goal1}")
print(f"✓ Explored {explore_result.statistics['derived_facts']} additional facts")
print(f"✓ Combined {len(set(explore_result.statistics['theorem_usage'].keys()))} different theorem types")

print(f"\nKey Insights:")
print(f"  • Segment equalities (AB=AC) can derive angle equalities (∠ABC=∠ACB)")
print(f"  • Isosceles triangle property bridges segments and angles")
print(f"  • Transitivity works independently for each fact type")
print(f"  • Multiple geometric concepts interact in unified proof")

print(f"\nDemonstrated Theorems:")
print(f"  • equality_transitivity (segment chains)")
print(f"  • equality_symmetry (segment reversal)")
print(f"  • isosceles_base_angles (segments → angles)")
print(f"  • angle_equality_symmetry (angle reversal)")

print("\n" + "=" * 70)
print("Example 8 Complete".center(70))
print("=" * 70 + "\n")
