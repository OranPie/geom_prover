"""
Proof display utilities.

Provides clean, concise output for proof trees showing:
- Facts derived
- Premises used (前置条件)
- Theorems applied
- Reasoning chain
"""

from typing import List, Set
from geometry_prover.proof.proof_tree import ProofTree, ProofNode, ProofNodeType
from geometry_prover.facts.fact_types import Fact


class ProofDisplay:
    """
    Display proof trees in a clean, readable format.

    Shows only relevant derivation steps with premises and theorems.
    """

    def __init__(self):
        """Initialize proof display."""
        self.displayed_facts: Set[str] = set()

    def display_proof(self, tree: ProofTree, goal_facts: List[Fact] = None):
        """
        Display proof tree in a clean format.

        Args:
            tree: Proof tree to display
            goal_facts: Optional goal facts to highlight
        """
        if tree.root is None:
            print("Empty proof tree")
            return

        print("\n" + "=" * 80)
        print("PROOF STEPS (证明步骤)")
        print("=" * 80)

        # Display initial facts
        if tree.root.facts:
            print("\n【Given / 已知】")
            for i, fact in enumerate(tree.root.facts, 1):
                print(f"  {i}. {fact.to_string()}")

        # Collect all theorem application nodes
        step_number = 1

        for node in tree.get_all_nodes():
            if node.node_type == ProofNodeType.THEOREM_APPLICATION:
                # Display this derivation step
                self._display_step(step_number, node)
                step_number += 1

        print("\n" + "=" * 80)

    def _display_step(self, step_num: int, node: ProofNode):
        """
        Display a single proof step.

        Args:
            step_num: Step number
            node: Proof node to display
        """
        theorem_name = node.theorem.metadata.name if node.theorem else "unknown"

        print(f"\n【Step {step_num} / 步骤 {step_num}】")

        # Show theorem
        print(f"  Theorem (定理): {theorem_name}")

        # Show premises (what facts were used)
        if node.premises:
            print("  Premises (前置条件):")
            for premise in node.premises:
                print(f"    • {premise.to_string()}")

        # Show derived facts
        print("  Derived (推导出):")
        for fact in node.facts:
            print(f"    ✓ {fact.to_string()}")

    def display_goal_proof(self, tree: ProofTree, goal_fact: Fact):
        """
        Display proof chain for a specific goal.

        Traces back from goal to show minimal proof path.

        Args:
            tree: Proof tree
            goal_fact: Goal to prove
        """
        # Find the node that derived this goal
        goal_node = None

        for node in tree.get_all_nodes():
            if node.node_type == ProofNodeType.THEOREM_APPLICATION:
                for fact in node.facts:
                    if self._facts_match(fact, goal_fact):
                        goal_node = node
                        break

        if goal_node is None:
            print(f"\n❌ Goal not found in proof tree: {goal_fact.to_string()}")
            return

        print("\n" + "=" * 80)
        print(f"PROOF OF: {goal_fact.to_string()}")
        print("=" * 80)

        # Collect proof chain
        proof_chain = []
        self._collect_proof_chain(goal_node, proof_chain)

        # Display chain
        for i, node in enumerate(proof_chain, 1):
            self._display_step(i, node)

        print(f"\n✅ Proved: {goal_fact.to_string()}")
        print("=" * 80)

    def _collect_proof_chain(self, node: ProofNode, chain: List[ProofNode]):
        """
        Collect all nodes in the proof chain.

        Args:
            node: Target node
            chain: List to collect nodes into
        """
        # Add this node
        if node.node_type == ProofNodeType.THEOREM_APPLICATION:
            chain.insert(0, node)

        # Recursively add dependencies
        # (In the current implementation, we don't track which nodes
        # derived the premises, so we just show the direct chain)

    def _facts_match(self, fact1: Fact, fact2: Fact) -> bool:
        """
        Check if two facts are equivalent.

        Args:
            fact1: First fact
            fact2: Second fact

        Returns:
            True if facts match
        """
        return fact1.to_string() == fact2.to_string()

    def display_statistics(self, stats: dict):
        """
        Display proof statistics.

        Args:
            stats: Statistics dictionary from ProofResult
        """
        print("\n" + "=" * 80)
        print("PROOF STATISTICS (统计)")
        print("=" * 80)

        print(f"  Total facts: {stats.get('total_facts', 0)}")
        print(f"  Derived facts: {stats.get('derived_facts', 0)}")
        print(f"  Iterations: {stats.get('iterations', 0)}")
        print(f"  Theorem applications: {stats.get('theorem_applications', 0)}")
        print(f"  Time: {stats.get('time_ms', 0)} ms")

        if stats.get('converged'):
            print("  Status: ✓ Converged (no more facts can be derived)")
        else:
            print("  Status: ⊗ Did not converge (limit reached)")

        # Show theorem usage
        theorem_usage = stats.get('theorem_usage', {})
        if theorem_usage:
            print("\n  Theorems used:")
            for name, count in sorted(theorem_usage.items()):
                print(f"    • {name}: {count}×")

        print("=" * 80)


def display_concise_proof(tree: ProofTree, initial_count: int = 0):
    """
    Display a very concise proof (just key steps).

    Args:
        tree: Proof tree
        initial_count: Number of initial facts (to skip)
    """
    display = ProofDisplay()

    # Show only theorem applications
    nodes = [n for n in tree.get_all_nodes()
             if n.node_type == ProofNodeType.THEOREM_APPLICATION]

    if not nodes:
        print("\nNo derivations performed.")
        return

    print(f"\n📋 Derived {len(nodes)} new fact(s) using theorems:")

    for i, node in enumerate(nodes, 1):
        theorem_name = node.theorem.metadata.name if node.theorem else "?"
        fact_summary = ", ".join(f.to_string() for f in node.facts[:2])
        if len(node.facts) > 2:
            fact_summary += f" (+{len(node.facts)-2} more)"

        print(f"  {i}. {theorem_name} → {fact_summary}")
