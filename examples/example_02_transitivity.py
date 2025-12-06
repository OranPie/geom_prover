"""
Example 2: Transitivity Chain Proof
====================================

This example demonstrates a more complex proof requiring transitivity.
It shows how the bidirectional reasoner combines forward and backward
reasoning to prove a multi-step goal.

Given: AB = CD, CD = EF
Prove: AB = EF
"""

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.facts.fact_types import EqualSegment
from pathlib import Path

# Define problem in DSL
problem = """
# Transitivity Chain Example
# Given: AB = CD and CD = EF
# Prove: AB = EF (requires transitivity theorem)

Point A, B, C, D, E, F
AB = CD
CD = EF
"""

print("=" * 70)
print("EXAMPLE 2: TRANSITIVITY CHAIN PROOF")
print("=" * 70)
print("\nProblem (DSL):")
print(problem)

# Parse and extract
lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print(f"\nExtracted Facts:")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Load theorems
theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
if theorem_dir.exists():
    engine.load_library(str(theorem_dir))
    print(f"\n✓ Loaded {len(engine.theorems)} theorems")
else:
    print("\n⚠ Theorem library not found")

# Create goal: AB = EF
if len(facts) >= 2:
    fact1 = facts[0]
    fact2 = facts[1]
    if fact1.fact_type == "EqualSegment" and fact2.fact_type == "EqualSegment":
        seg_ab = fact1.parameters["segment1"]
        seg_ef = fact2.parameters["segment2"]
        goal = EqualSegment(seg_ab, seg_ef)
        goals = [goal]
        print(f"\nGoal: {goal}")
    else:
        goals = []
else:
    goals = []

if goals:
    print("\n" + "=" * 70)
    print("TESTING DIFFERENT REASONING APPROACHES")
    print("=" * 70)

    # Test 1: Forward Reasoning
    print("\n1. FORWARD REASONING:")
    print("-" * 70)
    forward = ForwardReasoner(engine)
    forward_result = forward.reason(facts, goals=goals, max_depth=20)
    print(f"  Success: {forward_result.success}")
    print(f"  Iterations: {forward_result.statistics['iterations']}")
    print(f"  Derived facts: {forward_result.statistics['derived_facts']}")
    print(f"  Time: {forward_result.statistics['time_ms']}ms")
    if forward_result.statistics['theorem_usage']:
        print(f"  Theorems used: {', '.join(forward_result.statistics['theorem_usage'].keys())}")

    # Test 2: Backward Reasoning
    print("\n2. BACKWARD REASONING:")
    print("-" * 70)
    backward = BackwardReasoner(engine)
    backward_result = backward.prove(facts, goals, max_depth=20)
    print(f"  Success: {backward_result.success}")
    print(f"  Iterations: {backward_result.statistics['iterations']}")
    print(f"  Proven goals: {len(backward_result.proven_goals)}")
    print(f"  Time: {backward_result.statistics['time_ms']}ms")
    if backward_result.statistics['theorem_usage']:
        print(f"  Theorems used: {', '.join(backward_result.statistics['theorem_usage'].keys())}")

    # Test 3: Bidirectional Reasoning
    print("\n3. BIDIRECTIONAL REASONING:")
    print("-" * 70)
    bidirectional = BidirectionalReasoner(engine)
    bidirectional_result = bidirectional.prove(facts, goals, max_depth=20)
    print(f"  Success: {bidirectional_result.success}")
    print(f"  Iterations: {bidirectional_result.statistics['iterations']}")
    print(f"  Forward steps: {bidirectional_result.statistics['forward_steps']}")
    print(f"  Backward steps: {bidirectional_result.statistics['backward_steps']}")
    print(f"  Total facts: {bidirectional_result.statistics['total_facts']}")
    print(f"  Derived facts: {bidirectional_result.statistics['derived_facts']}")
    print(f"  Time: {bidirectional_result.statistics['time_ms']}ms")
    if bidirectional_result.statistics['theorem_usage']:
        print(f"  Theorems used:")
        for theorem, count in bidirectional_result.statistics['theorem_usage'].items():
            print(f"    - {theorem}: {count} time(s)")

    # Summary
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    results = [
        ("Forward", forward_result),
        ("Backward", backward_result),
        ("Bidirectional", bidirectional_result)
    ]

    print(f"\n{'Approach':<15} {'Success':<10} {'Time (ms)':<12} {'Iterations'}")
    print("-" * 70)
    for name, result in results:
        print(f"{name:<15} {str(result.success):<10} {result.statistics['time_ms']:<12} {result.statistics['iterations']}")

    successful = [name for name, result in results if result.success]
    if successful:
        print(f"\n✓ Successful approaches: {', '.join(successful)}")
    else:
        print(f"\n✗ No approach succeeded")

print("\n" + "=" * 70)
print("EXAMPLE COMPLETE")
print("=" * 70)
