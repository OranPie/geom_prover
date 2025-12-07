"""
Fact Expansion Walkthrough (Week 8)
===================================

This runnable walkthrough shows how a small DSL description expands into
facts and how the forward reasoner derives additional knowledge.
It uses a simple isosceles triangle so the resulting facts are easy to read.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.facts.fact_types import Fact, Triangle
from geometry_prover.proof.forward_reasoner import ForwardReasoner
from geometry_prover.theorems.engine import TheoremEngine


def flatten_facts(fact_nodes: Iterable[Fact]) -> list[Fact]:
    """Return a list of fact instances from the proof tree nodes."""

    return list(fact_nodes)


def summarize_facts(facts: Iterable[Fact]) -> dict[str, list[Fact]]:
    """Group facts by their fact_type for quick inspection."""

    grouped: dict[str, list[Fact]] = defaultdict(list)
    for fact in facts:
        grouped[fact.fact_type].append(fact)
    return grouped


if __name__ == "__main__":
    print("=" * 70)
    print("FACT EXPANSION WALKTHROUGH")
    print("=" * 70)

    # 1) Describe the problem in DSL
    dsl = """
    Point A, B, C
    Triangle ABC
    AB = AC
    """
    print("\nDSL Problem:")
    print(dsl.strip())

    # 2) Parse and extract initial facts
    tokens = Lexer(dsl).tokenize()
    ast = Parser(tokens).parse()
    model = FactExtractor().extract_from_program(ast)

    initial_facts: list[Fact] = list(model.constraints)

    # Explicit triangle fact helps theorems that require Triangle facts
    tri_abc = Triangle(model.points["A"], model.points["B"], model.points["C"])
    initial_facts.append(tri_abc)

    print("Initial facts:")
    for fact in initial_facts:
        print(f"  - {fact}")

    # 3) Load theorem library and run the forward reasoner
    theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"
    engine = TheoremEngine()
    engine.load_library(str(theorem_dir))

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts, max_depth=5, max_facts=120)

    # 4) Gather derived facts from the proof tree
    all_nodes = result.proof_tree.get_all_nodes() if result.proof_tree else []
    derived_facts = flatten_facts([fact for node in all_nodes for fact in node.facts])

    summary = summarize_facts(derived_facts)

    print("\nDerived facts by type:")
    for fact_type, facts in summary.items():
        print(f"  {fact_type} ({len(facts)}):")
        for fact in facts:
            print(f"    • {fact}")

    print("\nHighlights:")
    print("  • IsoscelesTriangle fact should appear because AB = AC")
    print("  • EqualAngle facts show the base angles are equal")
    print(f"  • Total derived facts: {len(derived_facts)}")

    print("\nStatistics:")
    print(result.statistics)

    print("\nExample 15 Complete")
