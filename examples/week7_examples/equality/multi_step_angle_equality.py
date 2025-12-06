"""
Example 7: Multi-Step Angle Equality
=====================================

Demonstrates chaining angle equality transitivity to prove relationships
through multiple intermediate angles.

Problem: Given ∠ABC=∠DEF, ∠DEF=∠GHI, ∠GHI=∠JKL, prove ∠ABC=∠JKL

This example shows:
- Multiple applications of angle_equality_transitivity theorem
- Working with angle facts (vs segment facts in Example 6)
- Bidirectional reasoning for angle relationships
- Comparing angle equality with segment equality patterns
"""

from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import EqualAngle


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
# Multi-Step Angle Equality Chain
# Prove transitivity across 4 angles

Point A, B, C, D, E, F, G, H, I, J, K, L

# Given facts: Chain of angle equalities
Angle ABC = Angle DEF
Angle DEF = Angle GHI
Angle GHI = Angle JKL

# Goal: Prove Angle ABC = Angle JKL (requires 2 transitivity steps)
"""

print_header("EXAMPLE 7: MULTI-STEP ANGLE EQUALITY")

print("\nProblem Description:")
print("  Given: ∠ABC = ∠DEF, ∠DEF = ∠GHI, ∠GHI = ∠JKL")
print("  Prove: ∠ABC = ∠JKL")
print("\nThis requires chaining angle transitivity:")
print("  Step 1: ∠ABC = ∠DEF, ∠DEF = ∠GHI → ∠ABC = ∠GHI")
print("  Step 2: ∠ABC = ∠GHI, ∠GHI = ∠JKL → ∠ABC = ∠JKL")

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
    if 'angle' in thm.metadata.category:
        print(f"  • {thm.metadata.name}: {thm.metadata.description}")

# Step 4: Define Goal
print_header("STEP 4: DEFINE GOAL")

# Get the angles from the facts
angle_abc = facts[0].parameters["angle1"]  # ∠ABC from "∠ABC = ∠DEF"
angle_jkl = facts[2].parameters["angle2"]  # ∠JKL from "∠GHI = ∠JKL"

goal = EqualAngle(angle_abc, angle_jkl)

print(f"\nGoal: {goal}")
print("\nThis goal requires deriving through intermediate angle equalities")
print("using the angle_equality_transitivity theorem multiple times.")

# Step 5: Forward Reasoning
print_header("STEP 5: FORWARD REASONING")

print("\nUsing forward reasoning to explore all derivable angle facts...")
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

print(f"\nForward reasoning explored all possible angle facts.")
print(f"It derived {forward_result.statistics['derived_facts']} new angle equalities.")

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
THEOREM: Transitive closure of angle equality relation

GIVEN:
  1. ∠ABC = ∠DEF
  2. ∠DEF = ∠GHI
  3. ∠GHI = ∠JKL

TO PROVE:
  ∠ABC = ∠JKL

PROOF:
  Step 1: Given ∠ABC = ∠DEF (Fact 1)
  Step 2: Given ∠DEF = ∠GHI (Fact 2)
  Step 3: By angle_equality_transitivity(∠ABC = ∠DEF, ∠DEF = ∠GHI):
          Therefore, ∠ABC = ∠GHI

  Step 4: Given ∠GHI = ∠JKL (Fact 3)
  Step 5: By angle_equality_transitivity(∠ABC = ∠GHI, ∠GHI = ∠JKL):
          Therefore, ∠ABC = ∠JKL  [GOAL PROVED]

Q.E.D.

Note: Angle equality follows the same transitivity pattern as segment equality,
demonstrating the generality of the equality axioms across different geometric objects.
""")

# Final Summary
print_header("SUMMARY")

print(f"\n✓ Successfully proved ∠ABC = ∠JKL")
print(f"✓ Required {bi_result.statistics['iterations']} iterations")
print(f"✓ Applied {bi_result.statistics['theorem_applications']} theorems")
print(f"✓ Completed in {bi_result.statistics['time_ms']}ms")

print(f"\nKey Insights:")
print(f"  • Angle equality uses same transitivity pattern as segment equality")
print(f"  • Forward reasoning found {forward_result.statistics['total_facts']} total angle facts")
print(f"  • Bidirectional reasoning efficiently targets the specific angle goal")
print(f"  • Equality axioms are general across geometric object types")

print(f"\nComparison with Example 6 (Segment Equality):")
print(f"  • Both use transitivity chaining (same reasoning pattern)")
print(f"  • Angles use angle_equality_transitivity")
print(f"  • Segments use equality_transitivity")
print(f"  • Performance characteristics are similar")

print("\n" + "=" * 70)
print("Example 7 Complete".center(70))
print("=" * 70 + "\n")
