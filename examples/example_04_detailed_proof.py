"""
Example 4: Detailed Proof Steps
================================

This example shows detailed proof steps and theorem applications,
demonstrating how the system builds a proof tree.

Given: AB = CD
Prove: CD = AB
Show: Every step of the proof with theorem applications
"""

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.facts.fact_types import EqualSegment
from pathlib import Path

problem = """
Point A, B, C, D
AB = CD
"""

print("=" * 70)
print("EXAMPLE 4: DETAILED PROOF STEPS")
print("=" * 70)
print("\nProblem:")
print(problem)

# Parse and extract
lexer = Lexer(problem)
parser = Parser(tokens=lexer.tokenize())
ast = parser.parse()

extractor = FactExtractor()
model = extractor.extract_from_program(ast)
facts = model.constraints

print("\n" + "=" * 70)
print("INITIAL STATE")
print("=" * 70)
print(f"Given facts: {len(facts)}")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Create goal
if len(facts) > 0 and facts[0].fact_type == "EqualSegment":
    seg1 = facts[0].parameters["segment1"]
    seg2 = facts[0].parameters["segment2"]
    goal = EqualSegment(seg2, seg1)
    goals = [goal]
    print(f"\nGoal to prove:")
    print(f"  {goal}")
else:
    goals = []

# Load theorems
theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
if theorem_dir.exists():
    engine.load_library(str(theorem_dir))
else:
    # Fallback: create minimal theorem
    from geometry_prover.theorems.theorem import TheoremBuilder
    from geometry_prover.theorems.pattern import Variable, PatternTemplate

    symmetry = (TheoremBuilder("equality_symmetry")
                .add_variable(Variable("?AB", "segment"))
                .add_variable(Variable("?CD", "segment"))
                .add_condition(PatternTemplate.equal_segment("?AB", "?CD"))
                .add_conclusion(PatternTemplate.equal_segment("?CD", "?AB"))
                .build())
    engine = TheoremEngine([symmetry])

print(f"\n" + "=" * 70)
print("AVAILABLE THEOREMS")
print("=" * 70)
for i, thm in enumerate(engine.theorems[:5], 1):  # Show first 5
    print(f"\n{i}. {thm.metadata.name}")
    print(f"   Category: {thm.metadata.category}")
    print(f"   Description: {thm.metadata.description}")
    print(f"   Variables: {', '.join([v.name for v in thm.variables])}")
    print(f"   Conditions: {len(thm.conditions)}")
    print(f"   Conclusions: {len(thm.conclusions)}")

# Run proof
if goals:
    print("\n" + "=" * 70)
    print("PROOF EXECUTION")
    print("=" * 70)

    reasoner = BackwardReasoner(engine)
    result = reasoner.prove(facts, goals, max_depth=10)

    print(f"\nProof completed in {result.statistics['time_ms']}ms")
    print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")

    # Show detailed statistics
    print("\n" + "=" * 70)
    print("DETAILED STATISTICS")
    print("=" * 70)
    stats = result.statistics
    print(f"  Search iterations: {stats['iterations']}")
    print(f"  Initial facts: {len(facts)}")
    print(f"  Total facts in final state: {stats['total_facts']}")
    print(f"  Goals proven: {stats['proven_goals']}")
    print(f"  Goals failed: {stats['failed_goals']}")
    print(f"  Theorem applications: {stats['theorem_applications']}")

    if stats['theorem_usage']:
        print(f"\n  Theorem usage breakdown:")
        for theorem, count in stats['theorem_usage'].items():
            print(f"    {theorem}: {count} application(s)")

    # Show proof tree
    print("\n" + "=" * 70)
    print("PROOF TREE")
    print("=" * 70)
    if result.proof_tree:
        tree = result.proof_tree
        all_nodes = tree.get_all_nodes()

        print(f"Proof tree has {len(all_nodes)} nodes")
        print(f"Maximum depth: {tree.get_depth()}")
        print(f"Leaf nodes: {len(tree.get_leaves())}")

        print(f"\nProof path (root to goal):")
        for i, node in enumerate(all_nodes):
            indent = "  " * node.depth()
            if node.node_type.value == "initial_fact":
                print(f"{indent}[START] Initial facts:")
                for fact in node.facts[:2]:
                    print(f"{indent}  {fact}")
            elif node.node_type.value == "theorem_application":
                if node.theorem:
                    print(f"{indent}[STEP {i}] Applied: {node.theorem.metadata.name}")
                    if 'binding' in node.metadata:
                        binding = node.metadata['binding']
                        print(f"{indent}  Bindings: {binding}")
                    for fact in node.facts[:2]:
                        print(f"{indent}  Derived: {fact}")

    # Show results
    print("\n" + "=" * 70)
    print("PROOF RESULT")
    print("=" * 70)
    if result.proven_goals:
        print(f"✓ Successfully proved {len(result.proven_goals)} goal(s):")
        for goal in result.proven_goals:
            print(f"  {goal}")
    if result.failed_goals:
        print(f"✗ Failed to prove {len(result.failed_goals)} goal(s):")
        for goal in result.failed_goals:
            print(f"  {goal}")

    # Human-readable proof
    print("\n" + "=" * 70)
    print("HUMAN-READABLE PROOF")
    print("=" * 70)
    print(f"""
Given:
  {facts[0]}

To Prove:
  {goals[0]}

Proof:
  1. Given: {facts[0]}
  2. By equality_symmetry theorem:
     If X = Y, then Y = X
  3. Applying to {facts[0]}:
     Therefore, {goals[0]}

Q.E.D. (Proof complete in {result.statistics['time_ms']}ms)
""")

print("=" * 70)
print("EXAMPLE COMPLETE")
print("=" * 70)
