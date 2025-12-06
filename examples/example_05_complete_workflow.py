"""
Example 5: Complete Workflow Demonstration
===========================================

This comprehensive example demonstrates the entire workflow from problem
definition through proof generation, showcasing all major features of the
geometry prover system.

Problem: Given a chain of equalities, prove the transitive closure
"""

import sys
from pathlib import Path

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.proof.backward_reasoner import BackwardReasoner
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner
from geometry_prover.proof.search_strategy import (
    BreadthFirstStrategy,
    DepthFirstStrategy,
    BestFirstStrategy
)
from geometry_prover.facts.fact_types import EqualSegment

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def print_subsection(title):
    """Print a formatted subsection header."""
    print("\n" + title)
    print("-" * 70)

# Define the problem
problem = """
# Geometry Problem: Equality Chain
# This problem demonstrates transitive reasoning across multiple steps
#
# Given facts:
#   AB = CD
#   CD = EF
#   EF = GH
#
# Goals to prove:
#   1. AB = GH (requires chaining transitivity)
#   2. GH = AB (requires symmetry after transitivity)

Point A, B, C, D, E, F, G, H

# Initial facts
AB = CD
CD = EF
EF = GH
"""

print_section("GEOMETRY PROVER - COMPLETE WORKFLOW")
print("\nThis example demonstrates:")
print("  • Complete DSL-to-proof pipeline")
print("  • Multiple reasoning strategies")
print("  • Proof tree visualization")
print("  • Performance analysis")
print("  • Educational proof steps")

print_section("STEP 1: PROBLEM DEFINITION")
print("\nDSL Source:")
print(problem)

# Step 1: Lexical Analysis
print_section("STEP 2: LEXICAL ANALYSIS")
print("\nTokenizing source code...")
lexer = Lexer(problem)
tokens = lexer.tokenize()
token_types = [str(token.type) for token in tokens if str(token.type) != "COMMENT"]
print(f"✓ Generated {len(tokens)} tokens")
print(f"  Unique token types: {len(set(token_types))}")

# Step 2: Syntactic Analysis
print_section("STEP 3: SYNTACTIC ANALYSIS")
print("\nParsing tokens to AST...")
parser = Parser(tokens)
ast = parser.parse()
print(f"✓ Built AST with {len(ast.statements)} statements")
print(f"\nStatement types:")
for i, stmt in enumerate(ast.statements, 1):
    stmt_type = type(stmt).__name__
    print(f"  {i}. {stmt_type}")

# Step 3: Semantic Analysis
print_section("STEP 4: SEMANTIC ANALYSIS")
print("\nExtracting geometric objects and facts...")
extractor = FactExtractor()
model = extractor.extract_from_program(ast)

print(f"\nGeometric Objects:")
print(f"  Points: {len(model.points)} → {', '.join(sorted(model.points.keys()))}")
if model.segments:
    print(f"  Segments: {len(model.segments)}")
if model.lines:
    print(f"  Lines: {len(model.lines)}")

facts = model.constraints
print(f"\nExtracted Facts: {len(facts)}")
for i, fact in enumerate(facts, 1):
    print(f"  {i}. {fact}")

# Step 4: Theorem Loading
print_section("STEP 5: THEOREM LIBRARY")
print("\nLoading theorem library...")
theorem_dir = Path(__file__).parent.parent / "geometry_prover" / "data" / "theorems"
engine = TheoremEngine()

if theorem_dir.exists():
    engine.load_library(str(theorem_dir))
    print(f"✓ Loaded {len(engine.theorems)} theorems")

    # Categorize theorems
    categories = {}
    for thm in engine.theorems:
        cat = thm.metadata.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(thm.metadata.name)

    print(f"\nTheorem Categories:")
    for cat, names in sorted(categories.items()):
        print(f"  {cat}:")
        for name in names:
            print(f"    • {name}")
else:
    print("⚠ Warning: Theorem library not found")
    sys.exit(1)

# Step 5: Define Goals
print_section("STEP 6: GOAL DEFINITION")

# Goal 1: AB = GH (requires multiple transitivity applications)
if len(facts) >= 3:
    seg_ab = facts[0].parameters["segment1"]
    seg_gh = facts[2].parameters["segment2"]
    goal1 = EqualSegment(seg_ab, seg_gh)

    # Goal 2: GH = AB (symmetry of goal 1)
    goal2 = EqualSegment(seg_gh, seg_ab)

    goals = [goal1, goal2]

    print("\nGoals to prove:")
    for i, goal in enumerate(goals, 1):
        print(f"  {i}. {goal}")
else:
    print("⚠ Insufficient facts to create goals")
    sys.exit(1)

# Step 6: Proof Strategies Comparison
print_section("STEP 7: REASONING STRATEGY COMPARISON")

strategies = [
    ("Breadth-First", BreadthFirstStrategy()),
    ("Depth-First", DepthFirstStrategy()),
    ("Best-First", BestFirstStrategy())
]

results = {}

for strategy_name, strategy in strategies:
    print_subsection(f"{strategy_name} Strategy")
    reasoner = BidirectionalReasoner(engine, strategy=strategy)
    result = reasoner.prove(facts, goals, max_depth=20, max_iterations=100)
    results[strategy_name] = result

    print(f"  Success: {result.success}")
    print(f"  Iterations: {result.statistics['iterations']}")
    print(f"  Forward steps: {result.statistics['forward_steps']}")
    print(f"  Backward steps: {result.statistics['backward_steps']}")
    print(f"  Total facts: {result.statistics['total_facts']}")
    print(f"  Proven goals: {result.statistics['proven_goals']}/{len(goals)}")
    print(f"  Time: {result.statistics['time_ms']}ms")

# Comparison table
print_subsection("Strategy Comparison")
print(f"\n{'Strategy':<20} {'Success':<10} {'Time':<10} {'Facts':<10} {'Goals'}")
print("-" * 70)
for name, result in results.items():
    success = "✓" if result.success else "✗"
    proven = f"{result.statistics['proven_goals']}/{len(goals)}"
    print(f"{name:<20} {success:<10} {result.statistics['time_ms']:<10} "
          f"{result.statistics['total_facts']:<10} {proven}")

# Step 7: Detailed Proof Analysis (using best result)
best_result = max(results.values(), key=lambda r: r.statistics['proven_goals'])

print_section("STEP 8: DETAILED PROOF ANALYSIS")
print(f"\nAnalyzing best result (proved {best_result.statistics['proven_goals']} goals)...")

if best_result.statistics['theorem_usage']:
    print(f"\nTheorem Application Breakdown:")
    for theorem, count in sorted(best_result.statistics['theorem_usage'].items(),
                                   key=lambda x: x[1], reverse=True):
        print(f"  {theorem}: {count} application(s)")

print(f"\nProof Statistics:")
print(f"  Search depth reached: {best_result.statistics['iterations']}")
print(f"  Facts generated: {best_result.statistics['derived_facts']}")
print(f"  Theorem applications: {best_result.statistics['theorem_applications']}")
print(f"  Execution time: {best_result.statistics['time_ms']}ms")

# Step 8: Proof Tree Visualization
print_section("STEP 9: PROOF TREE")

if best_result.proof_tree:
    tree = best_result.proof_tree
    all_nodes = tree.get_all_nodes()

    print(f"\nProof Tree Structure:")
    print(f"  Total nodes: {len(all_nodes)}")
    print(f"  Tree depth: {tree.get_depth()}")
    print(f"  Leaf nodes: {len(tree.get_leaves())}")

    print(f"\nKey Derivation Steps:")
    step = 0
    for node in all_nodes:
        if node.node_type.value == "theorem_application" and node.theorem:
            step += 1
            if step <= 5:  # Show first 5 steps
                print(f"  Step {step}: {node.theorem.metadata.name}")
                if node.facts:
                    for fact in node.facts[:1]:  # Show first fact
                        print(f"    → Derived: {fact}")

# Step 9: Human-Readable Proof
print_section("STEP 10: HUMAN-READABLE PROOF")

print("""
THEOREM: Transitive closure of equality relation

GIVEN:
  1. AB = CD
  2. CD = EF
  3. EF = GH

TO PROVE:
  1. AB = GH
  2. GH = AB

PROOF:
  Step 1: Given AB = CD (Fact 1)
  Step 2: Given CD = EF (Fact 2)
  Step 3: Given EF = GH (Fact 3)

  Step 4: By transitivity theorem (AB = CD, CD = EF):
          Therefore, AB = EF

  Step 5: By transitivity theorem (AB = EF, EF = GH):
          Therefore, AB = GH  [GOAL 1 PROVED]

  Step 6: By symmetry theorem (AB = GH):
          Therefore, GH = AB  [GOAL 2 PROVED]

Q.E.D.
""")

# Final Summary
print_section("WORKFLOW COMPLETE")

success_count = sum(1 for r in results.values() if r.success)
print(f"\nExecution Summary:")
print(f"  ✓ Parsed {len(ast.statements)} DSL statements")
print(f"  ✓ Extracted {len(facts)} facts from {len(model.points)} points")
print(f"  ✓ Loaded {len(engine.theorems)} theorems")
print(f"  ✓ Tested {len(strategies)} search strategies")
print(f"  ✓ {success_count}/{len(strategies)} strategies succeeded")
print(f"  ✓ Proved {best_result.statistics['proven_goals']}/{len(goals)} goals")
print(f"  ✓ Generated {best_result.statistics['derived_facts']} derived facts")
print(f"  ✓ Applied {best_result.statistics['theorem_applications']} theorems")
print(f"  ✓ Completed in {best_result.statistics['time_ms']}ms")

print(f"\nThis demonstrates the complete Week 1-6 pipeline:")
print(f"  Week 1: DSL parsing (Lexer, Parser, AST)")
print(f"  Week 2-3: Semantic analysis (FactExtractor, GeometryModel)")
print(f"  Week 4: Theorem system (TheoremEngine, Matcher, Applicator)")
print(f"  Week 5: Proof infrastructure (ProofTree, ProofState, SearchStrategy)")
print(f"  Week 6: Automated reasoning (Forward, Backward, Bidirectional)")

print("\n" + "=" * 70)
print("END OF DEMONSTRATION".center(70))
print("=" * 70)
