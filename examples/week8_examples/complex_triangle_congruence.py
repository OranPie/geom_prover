"""
Example 14: Complex Triangle Congruence and Similarity
======================================================

This example sets up two triangles with three pairs of equal sides (SSS)
and demonstrates how the theorem engine derives both congruent and
similar triangle relationships.

Highlights:
- Parses a triangle-heavy DSL problem with six points and two triangles
- Loads the full theorem library (including congruence + similarity)
- Uses forward reasoning to trigger SSS congruence and its downstream
  similarity deduction
- Reports derived facts and theorem usage so behavior is explicit
"""

from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.facts.fact_types import (
    Triangle,
    CongruentTriangle,
    SimilarTriangle,
)
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.theorems.engine import TheoremEngine


def print_header(title: str) -> None:
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def collect_all_facts(result) -> list:
    if not result.proof_tree:
        return []

    facts: list = []
    for node in result.proof_tree.get_all_nodes():
        facts.extend(node.facts)
    return facts


problem = """
Point A, B, C, D, E, F
Triangle ABC
Triangle DEF
AB = DE
BC = EF
CA = FD
"""

print_header("EXAMPLE 14: COMPLEX TRIANGLE CONGRUENCE")
print("Problem setup:")
print("  • Two triangles ABC and DEF")
print("  • Three equal side pairs: AB=DE, BC=EF, CA=FD")
print("  • Expect SSS to derive congruence, then similarity")

lexer = Lexer(problem)
parser = Parser(lexer.tokenize())
ast = parser.parse()

extractor = FactExtractor()
model = extractor.extract_from_program(ast)

triangle_facts = [
    Triangle(model.points["A"], model.points["B"], model.points["C"]),
    Triangle(model.points["D"], model.points["E"], model.points["F"]),
]
all_facts = model.constraints + triangle_facts

print("\nInitial facts:")
print(f"  • Points: {', '.join(sorted(model.points.keys()))}")
print(f"  • Triangles: {len(triangle_facts)} declared")
print(f"  • Constraints: {len(model.constraints)} (side equalities)")

print_header("LOADING THEOREM LIBRARY")
theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
engine.load_library(str(theorem_dir))
print(f"Loaded {len(engine.theorems)} theorems from {theorem_dir}")

print_header("FORWARD REASONING")
reasoner = ForwardReasoner(engine)
result = reasoner.reason(all_facts, max_depth=10, max_facts=200)

print("Reasoning statistics:")
for key, value in result.statistics.items():
    print(f"  • {key}: {value}")

derived_facts = collect_all_facts(result)
congruent = [f for f in derived_facts if isinstance(f, CongruentTriangle)]
similar = [f for f in derived_facts if isinstance(f, SimilarTriangle)]

print("\nDerived facts of interest:")
if congruent:
    print(f"  ✓ Derived congruent triangle: {congruent[0]}")
else:
    print("  ✗ No congruent triangle derived")

if similar:
    print(f"  ✓ Derived similar triangle: {similar[0]}")
else:
    print("  ✗ No similar triangle derived")

print_header("SUMMARY")
print("Key outcomes:")
print(f"  • SSS congruence applied: {'yes' if congruent else 'no'}")
print(f"  • Congruence → similarity applied: {'yes' if similar else 'no'}")
print(f"  • Total facts explored: {result.statistics['total_facts']}")
print(f"  • Theorem applications: {result.statistics['theorem_applications']}")

print("\n" + "=" * 70)
print("Example 14 Complete".center(70))
print("=" * 70)
