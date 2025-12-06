"""
Theorem engine for automated reasoning.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 20 - Theorem engine integration

This module provides a high-level engine that manages theorem libraries
and automatically applies theorems to derive new facts.
"""

from typing import List, Set, Optional, Tuple
from dataclasses import dataclass

from geometry_prover.theorems.theorem import Theorem
from geometry_prover.theorems.applicator import TheoremApplicator, TheoremApplication
from geometry_prover.theorems.loader import load_theorem_library
from geometry_prover.theorems.auxiliary_constructor import AuxiliaryConstructor
from geometry_prover.facts.fact_types import Fact


@dataclass
class DerivationStep:
    """
    Records a single step in a derivation.

    Tracks which theorem was applied and what facts were derived.
    """
    theorem_name: str
    derived_facts: List[Fact]
    step_number: int

    def __repr__(self) -> str:
        return (
            f"Step {self.step_number}: Applied '{self.theorem_name}' "
            f"→ {len(self.derived_facts)} fact(s)"
        )


class TheoremEngine:
    """
    High-level theorem engine for automated reasoning.

    The engine:
    - Manages a library of theorems
    - Automatically applies applicable theorems
    - Performs forward chaining (iterative derivation)
    - Tracks derivation history
    - Prevents infinite loops via fact deduplication

    Example:
        engine = TheoremEngine()
        engine.load_library("data/theorems/")

        # Add initial facts
        facts = [EqualSegment(seg_ab, seg_cd)]

        # Derive new facts
        results = engine.forward_chain(facts, max_iterations=10)
        print(f"Derived {len(results.all_facts)} total facts")
    """

    def __init__(self, theorems: Optional[List[Theorem]] = None):
        """
        Initialize theorem engine.

        Args:
            theorems: Optional list of theorems to use
        """
        self.theorems = theorems or []

        # Create auxiliary constructor for handling derived_from
        aux_constructor = AuxiliaryConstructor()

        # Create applicator with auxiliary constructor
        self.applicator = TheoremApplicator()
        self.applicator.matcher.auxiliary_constructor = aux_constructor

    def load_library(self, directory: str) -> int:
        """
        Load theorem library from directory.

        Args:
            directory: Path to directory containing YAML files

        Returns:
            Number of theorems loaded
        """
        self.theorems = load_theorem_library(directory)
        return len(self.theorems)

    def add_theorem(self, theorem: Theorem) -> None:
        """Add a single theorem to the engine."""
        self.theorems.append(theorem)

    def forward_chain(
        self,
        initial_facts: List[Fact],
        max_iterations: int = 100,
        max_facts: int = 1000
    ) -> 'ForwardChainResult':
        """
        Perform forward chaining to derive new facts.

        Applies theorems iteratively until no new facts can be derived
        or limits are reached.

        Args:
            initial_facts: Starting facts
            max_iterations: Maximum iterations to prevent infinite loops
            max_facts: Maximum total facts to prevent explosion

        Returns:
            ForwardChainResult with all facts and derivation history
        """
        # Track all facts (using set for deduplication)
        all_facts_set: Set[Fact] = set(initial_facts)
        all_facts: List[Fact] = list(initial_facts)

        # Track derivation history
        derivation_steps: List[DerivationStep] = []
        step_number = 0

        # Forward chaining loop
        for iteration in range(max_iterations):
            new_facts_this_iteration: List[Fact] = []

            # Try applying each theorem
            for theorem in self.theorems:
                result = self.applicator.apply(theorem, all_facts)

                if result:
                    # Check which facts are actually new
                    new_facts = [f for f in result.derived_facts if f not in all_facts_set]

                    if new_facts:
                        step_number += 1
                        derivation_steps.append(
                            DerivationStep(
                                theorem_name=theorem.metadata.name,
                                derived_facts=new_facts,
                                step_number=step_number
                            )
                        )

                        # Add to collections
                        for fact in new_facts:
                            all_facts_set.add(fact)
                            all_facts.append(fact)
                            new_facts_this_iteration.append(fact)

            # Check termination conditions
            if not new_facts_this_iteration:
                # No new facts derived - we're done
                break

            if len(all_facts) >= max_facts:
                # Fact explosion - stop
                break

        return ForwardChainResult(
            initial_facts=initial_facts,
            all_facts=all_facts,
            derived_facts=all_facts[len(initial_facts):],
            derivation_steps=derivation_steps,
            iterations=iteration + 1,
            converged=(len(derivation_steps) == 0 or
                      (iteration < max_iterations - 1 and not new_facts_this_iteration))
        )

    def apply_single_theorem(
        self,
        theorem_name: str,
        facts: List[Fact]
    ) -> Optional[TheoremApplication]:
        """
        Apply a specific theorem by name.

        Args:
            theorem_name: Name of theorem to apply
            facts: Facts to match against

        Returns:
            TheoremApplication if successful, None otherwise
        """
        theorem = self.get_theorem(theorem_name)
        if not theorem:
            return None

        return self.applicator.apply(theorem, facts)

    def get_theorem(self, name: str) -> Optional[Theorem]:
        """
        Get theorem by name.

        Args:
            name: Theorem name

        Returns:
            Theorem if found, None otherwise
        """
        for theorem in self.theorems:
            if theorem.metadata.name == name:
                return theorem
        return None

    def list_theorems(self) -> List[str]:
        """
        Get list of all theorem names.

        Returns:
            List of theorem names
        """
        return [t.metadata.name for t in self.theorems]

    def get_theorems_by_category(self, category: str) -> List[Theorem]:
        """
        Get all theorems in a category.

        Args:
            category: Category name

        Returns:
            List of theorems in category
        """
        return [t for t in self.theorems if t.metadata.category == category]


@dataclass
class ForwardChainResult:
    """
    Result of forward chaining.

    Contains all facts, derivation history, and statistics.
    """
    initial_facts: List[Fact]
    all_facts: List[Fact]
    derived_facts: List[Fact]
    derivation_steps: List[DerivationStep]
    iterations: int
    converged: bool

    def __repr__(self) -> str:
        return (
            f"ForwardChainResult("
            f"initial={len(self.initial_facts)}, "
            f"derived={len(self.derived_facts)}, "
            f"total={len(self.all_facts)}, "
            f"steps={len(self.derivation_steps)}, "
            f"iterations={self.iterations}, "
            f"converged={self.converged})"
        )

    def print_summary(self) -> None:
        """Print human-readable summary."""
        print(f"\n=== Forward Chaining Results ===")
        print(f"Initial facts: {len(self.initial_facts)}")
        print(f"Derived facts: {len(self.derived_facts)}")
        print(f"Total facts: {len(self.all_facts)}")
        print(f"Derivation steps: {len(self.derivation_steps)}")
        print(f"Iterations: {self.iterations}")
        print(f"Converged: {self.converged}")

        if self.derivation_steps:
            print(f"\n=== Derivation Steps ===")
            for step in self.derivation_steps:
                print(f"  {step}")
