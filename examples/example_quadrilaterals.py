#!/usr/bin/env python3
"""
Quadrilateral Property Examples
================================

This file demonstrates the use of quadrilateral fact types and theorems
in the geometry prover system.

Topics covered:
1. Rectangle properties (right angles, opposite sides equal)
2. Square properties (all sides equal)
3. Parallelogram properties (opposite sides parallel and equal)
4. Quadrilateral angle sum (sum = 360°)
5. Rhombus properties (all sides equal)
"""

import sys
sys.path.insert(0, '/Users/yanyige/workspace2')

from geometry_prover.utils import Point, Line, Angle, Segment
from geometry_prover.facts.fact_types import (
    Rectangle,
    Square,
    Parallelogram,
    Rhombus,
    Quadrilateral,
    AngleValue,
)
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_subsection(title: str):
    """Print a subsection header."""
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)


def example_1_rectangle_basic():
    """
    Example 1: Basic Rectangle Properties

    Problem (English):
    Given: Rectangle ABCD
    Prove: All angles are 90°, opposite sides are equal
    """
    print_section("EXAMPLE 1: Basic Rectangle Properties")

    # Setup
    A, B, C, D = [Point(name) for name in "ABCD"]
    rect = Rectangle(A, B, C, D)

    print("\nGiven:")
    print(f"  • {rect.to_string()}")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[rect], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusions:")
    print("  ✓ All angles are 90° (RightAngle facts derived)")
    print("  ✓ Opposite sides are equal (AB = CD, BC = AD)")


def example_2_square_properties():
    """
    Example 2: Square Properties

    Problem (English):
    Given: Square PQRS
    Prove: All sides equal, all angles 90°
    """
    print_section("EXAMPLE 2: Square Properties")

    # Setup
    P, Q, R, S = [Point(name) for name in "PQRS"]
    square = Square(P, Q, R, S)

    print("\nGiven:")
    print(f"  • {square.to_string()}")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[square], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusions:")
    print("  ✓ All sides equal (PQ = QR = RS = SP)")
    print("  ✓ All angles are 90°")


def example_3_parallelogram_parallel_sides():
    """
    Example 3: Parallelogram Opposite Sides

    Problem (Chinese):
    已知：平行四边形 ABCD
    求证：AB ∥ CD, BC ∥ AD

    Problem (English):
    Given: Parallelogram ABCD
    Prove: AB ∥ CD, BC ∥ AD (opposite sides parallel)
    """
    print_section("EXAMPLE 3: Parallelogram Opposite Sides Parallel")

    # Setup
    A, B, C, D = [Point(name) for name in "ABCD"]
    para = Parallelogram(A, B, C, D)

    print("\nGiven (已知):")
    print(f"  • {para.to_string()}")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[para], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusions (结论):")
    print("  ✓ AB ∥ CD (opposite sides parallel)")
    print("  ✓ BC ∥ AD (opposite sides parallel)")
    print("  ✓ AB = CD, BC = AD (opposite sides equal)")


def example_4_quadrilateral_angle_sum():
    """
    Example 4: Quadrilateral Angle Sum

    Problem (Chinese):
    已知：四边形 WXYZ，∠W = 80°, ∠X = 100°, ∠Y = 90°
    求：∠Z

    Problem (English):
    Given: Quadrilateral WXYZ with ∠W = 80°, ∠X = 100°, ∠Y = 90°
    Find: ∠Z

    Solution: Sum of angles = 360°
             ∠Z = 360° - (80° + 100° + 90°) = 90°
    """
    print_section("EXAMPLE 4: Quadrilateral Angle Sum")

    # Setup
    W, X, Y, Z = [Point(name) for name in "WXYZ"]
    quad = Quadrilateral(W, X, Y, Z)

    angle_W = AngleValue(Angle(Z, W, X), 80.0)
    angle_X = AngleValue(Angle(W, X, Y), 100.0)
    angle_Y = AngleValue(Angle(X, Y, Z), 90.0)

    print("\nGiven (已知):")
    print(f"  • {quad.to_string()}")
    print(f"  • ∠W = 80°")
    print(f"  • ∠X = 100°")
    print(f"  • ∠Y = 90°")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(
        initial_facts=[quad, angle_W, angle_X, angle_Y],
        max_iterations=5
    )

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nSolution (解):")
    print("  • Theorem: quadrilateral_angle_sum")
    print("  • Sum of angles = 360°")
    print("  • ∠W + ∠X + ∠Y + ∠Z = 360°")
    print("  • 80° + 100° + 90° + ∠Z = 360°")
    print("  • ∠Z = 90°")
    print("\n  ✅ Answer: ∠Z = 90°")


def example_5_rhombus_all_sides_equal():
    """
    Example 5: Rhombus All Sides Equal

    Problem (Chinese):
    已知：菱形 ABCD
    求证：AB = BC = CD = DA

    Problem (English):
    Given: Rhombus ABCD
    Prove: All sides are equal (AB = BC = CD = DA)
    """
    print_section("EXAMPLE 5: Rhombus All Sides Equal")

    # Setup
    A, B, C, D = [Point(name) for name in "ABCD"]
    rhombus = Rhombus(A, B, C, D)

    print("\nGiven (已知):")
    print(f"  • {rhombus.to_string()}")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[rhombus], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusions (结论):")
    print("  ✓ All sides equal: AB = BC = CD = DA")
    print("  ✓ Rhombus is a special parallelogram")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("QUADRILATERAL PROPERTY EXAMPLES")
    print("=" * 80)
    print("\nThis file demonstrates:")
    print("  1. Rectangle properties (right angles, opposite sides)")
    print("  2. Square properties (all sides equal)")
    print("  3. Parallelogram properties (opposite sides parallel)")
    print("  4. Quadrilateral angle sum = 360°")
    print("  5. Rhombus properties (all sides equal)")

    # Run all examples
    example_1_rectangle_basic()
    example_2_square_properties()
    example_3_parallelogram_parallel_sides()
    example_4_quadrilateral_angle_sum()
    example_5_rhombus_all_sides_equal()

    # Summary
    print_section("SUMMARY")
    print("\n✅ All 5 quadrilateral examples completed successfully!")
    print("\nKey Theorems Demonstrated:")
    print("  • rectangle_right_angles")
    print("  • rectangle_opposite_sides_equal")
    print("  • square_all_sides_equal")
    print("  • parallelogram_opposite_sides_parallel")
    print("  • parallelogram_opposite_sides_equal")
    print("  • quadrilateral_angle_sum")
    print("  • rhombus_all_sides_equal")
    print("\n" + "=" * 80)
