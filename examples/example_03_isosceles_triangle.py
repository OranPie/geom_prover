"""
Example 3: Isosceles Triangle Properties
=========================================

This example demonstrates working with more complex geometric objects
like triangles and explores what facts can be derived.

Given: Triangle ABC with AB = AC (isosceles)
Goal: Explore all derivable facts using forward reasoning
"""

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from pathlib import Path

# Define isosceles triangle
problem = """
# Isosceles Triangle
# Triangle ABC where AB = AC
# The triangle has two equal sides

Point A, B, C
Triangle ABC
AB = AC
"""

print("=" * 70)
print("EXAMPLE 3: ISOSCELES TRIANGLE PROPERTIES")
print("=" * 70)
print("\nProblem (DSL):")
print(problem)

# Parse and extract
print("\n" + "=" * 70)
print("PARSING AND SEMANTIC EXTRACTION")
print("=" * 70)
lexer = Lexer(problem)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print(f"Parsed statements: {len(ast.statements)}")
for i, stmt in enumerate(ast.statements, 1):
    print(f"  {i}. {type(stmt).__name__}")

extractor = FactExtractor()
model = extractor.extract_from_program(ast)

print(f"\nGeometric Objects Created:")
print(f"  Points: {', '.join(model.points.keys())}")
print(f"  Triangles: {len(model.triangles)}")
if model.segments:
    print(f"  Segments: {', '.join([str(s) for s in model.segments.values()][:5])}")

facts = model.constraints
print(f"\nInitial Facts: {len(facts)}")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact.fact_type}: {fact}")

# Load theorems
print("\n" + "=" * 70)
print("LOADING THEOREM LIBRARY")
print("=" * 70)
theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()
if theorem_dir.exists():
    engine.load_library(str(theorem_dir))
    print(f"✓ Loaded {len(engine.theorems)} theorems")
    print(f"\nTheorem categories:")
    categories = {}
    for thm in engine.theorems:
        cat = thm.metadata.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(thm.metadata.name)
    for cat, theorems in sorted(categories.items()):
        print(f"  {cat}: {len(theorems)} theorem(s)")
else:
    print("⚠ Theorem library not found")

# Forward reasoning to explore
print("\n" + "=" * 70)
print("FORWARD REASONING - EXPLORING DERIVABLE FACTS")
print("=" * 70)
reasoner = ForwardReasoner(engine)
result = reasoner.reason(facts, max_depth=5, max_facts=50)

print(f"\nReasoning completed:")
print(f"  Iterations: {result.statistics['iterations']}")
print(f"  Initial facts: {len(facts)}")
print(f"  Total facts after reasoning: {result.statistics['total_facts']}")
print(f"  Newly derived facts: {result.statistics['derived_facts']}")
print(f"  Theorem applications: {result.statistics['theorem_applications']}")
print(f"  Time: {result.statistics['time_ms']}ms")
print(f"  Converged: {result.statistics['converged']}")

if result.statistics['theorem_usage']:
    print(f"\nTheorems Applied:")
    for theorem, count in sorted(result.statistics['theorem_usage'].items(),
                                  key=lambda x: x[1], reverse=True):
        print(f"  {theorem}: {count} time(s)")

# Show proof tree
print("\n" + "=" * 70)
print("PROOF TREE STRUCTURE")
print("=" * 70)
if result.proof_tree:
    all_nodes = result.proof_tree.get_all_nodes()
    print(f"Total nodes in proof tree: {len(all_nodes)}")
    print(f"Tree depth: {result.proof_tree.get_depth()}")

    # Show first few derivation steps
    print(f"\nFirst few derivation steps:")
    count = 0
    for node in all_nodes[:5]:
        if node.node_type.value == "theorem_application":
            count += 1
            if node.theorem and node.facts:
                print(f"  {count}. Applied {node.theorem.metadata.name}:")
                for fact in node.facts[:2]:  # Show first 2 facts
                    print(f"     → {fact}")

print("\n" + "=" * 70)
print("OBSERVATIONS")
print("=" * 70)
print(f"""
From an isosceles triangle (AB = AC), forward reasoning derived:
  - {result.statistics['derived_facts']} new facts
  - Most frequently used: {max(result.statistics['theorem_usage'].items(), key=lambda x: x[1])[0] if result.statistics['theorem_usage'] else 'N/A'}
  - Proof search converged: {result.statistics['converged']}

This demonstrates the system's ability to automatically explore
geometric consequences starting from basic facts.
""")

print("=" * 70)
print("EXAMPLE COMPLETE")
print("=" * 70)
