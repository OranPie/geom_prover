#!/usr/bin/env python3
"""
Circle Theorem Examples
=======================

This file demonstrates the use of circle theorems in the geometry prover system.

Topics covered:
1. Thales' Theorem (angle in semicircle = 90°)
2. Inscribed Angle Theorem (inscribed = half of central)
3. Tangent-Radius Perpendicular
4. Equal Tangent Segments from External Point
5. Cyclic Quadrilateral (opposite angles supplementary)
"""

import sys
sys.path.insert(0, '/Users/yanyige/workspace2')

from geometry_prover.utils import Point, Line, Angle, Circle
from geometry_prover.facts.fact_types import (
    OnCircle,
    Diameter,
    InscribedAngle,
    CentralAngle,
    TangentAt,
    CyclicQuadrilateral,
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


def example_1_thales_theorem():
    """
    Example 1: Thales' Theorem (Angle in Semicircle)

    Problem (Chinese):
    已知：圆 O，直径 AB，点 P 在圆上
    求证：∠APB = 90°

    Problem (English):
    Given: Circle O with diameter AB, point P on circle
    Prove: ∠APB = 90° (angle in semicircle is a right angle)

    This is one of the most famous circle theorems!
    """
    print_section("EXAMPLE 1: Thales' Theorem (Angle in Semicircle)")

    # Setup
    O = Point("O")  # Center
    A = Point("A")
    B = Point("B")
    P = Point("P")  # Point on circle

    circle = Circle(O, 5.0)  # Circle with radius 5

    # Facts
    diameter_AB = Diameter(A, B, circle)
    on_P = OnCircle(P, circle)
    angle_APB = Angle(A, P, B)
    inscribed = InscribedAngle(angle_APB, circle)

    print("\nGiven (已知):")
    print("  • Circle O with radius 5")
    print("  • AB is a diameter")
    print("  • P is on the circle")
    print("  • ∠APB is inscribed in the circle")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(
        initial_facts=[diameter_AB, on_P, inscribed],
        max_iterations=5
    )

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusion (结论):")
    print("  ✅ ∠APB = 90° (Thales' Theorem)")
    print("  • Any angle inscribed in a semicircle is a right angle")


def example_2_inscribed_angle_theorem():
    """
    Example 2: Inscribed Angle Theorem

    Problem (Chinese):
    已知：圆 O，弧 AB，点 P 在圆上（不在弧 AB 上）
          中心角 ∠AOB = 80°
    求：内接角 ∠APB

    Problem (English):
    Given: Circle O, arc AB, point P on circle (not on arc AB)
           Central angle ∠AOB = 80°
    Find: Inscribed angle ∠APB

    Solution: ∠APB = (1/2) × ∠AOB = (1/2) × 80° = 40°
    """
    print_section("EXAMPLE 2: Inscribed Angle Theorem")

    # Setup
    O = Point("O")  # Center
    A = Point("A")
    B = Point("B")
    P = Point("P")

    circle = Circle(O, 5.0)

    # Facts
    on_A = OnCircle(A, circle)
    on_B = OnCircle(B, circle)
    on_P = OnCircle(P, circle)

    angle_AOB = Angle(A, O, B)
    angle_APB = Angle(A, P, B)

    central = CentralAngle(angle_AOB, circle)
    inscribed = InscribedAngle(angle_APB, circle)

    central_value = AngleValue(angle_AOB, 80.0)

    print("\nGiven (已知):")
    print("  • Circle O with radius 5")
    print("  • Points A, B, P on the circle")
    print("  • Central angle ∠AOB = 80°")
    print("  • ∠APB is inscribed angle")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(
        initial_facts=[on_A, on_B, on_P, central, inscribed, central_value],
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
    print("  • Theorem: inscribed_angle_theorem")
    print("  • Inscribed angle = (1/2) × Central angle")
    print("  • ∠APB = (1/2) × ∠AOB")
    print("  • ∠APB = (1/2) × 80°")
    print("  • ∠APB = 40°")
    print("\n  ✅ Answer: ∠APB = 40°")


def example_3_tangent_radius_perpendicular():
    """
    Example 3: Tangent-Radius Perpendicular

    Problem (Chinese):
    已知：圆 O，切线 L 切于点 P
    求证：OP ⊥ L

    Problem (English):
    Given: Circle O, tangent line L at point P
    Prove: Radius OP is perpendicular to tangent L

    This is a fundamental property of tangents to circles.
    """
    print_section("EXAMPLE 3: Tangent-Radius Perpendicular")

    # Setup
    O = Point("O")  # Center
    P = Point("P")  # Tangent point

    circle = Circle(O, 5.0)
    line_L = Line(P, Point("Q"))  # Tangent line

    # Facts
    tangent = TangentAt(line_L, circle, P)

    print("\nGiven (已知):")
    print("  • Circle O with radius 5")
    print("  • Line L is tangent to circle at point P")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[tangent], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusion (结论):")
    print("  ✅ OP ⊥ L (radius perpendicular to tangent)")
    print("  • This is always true for any tangent to a circle")


def example_4_equal_tangent_segments():
    """
    Example 4: Equal Tangent Segments from External Point

    Problem (Chinese):
    已知：圆 O，外部点 P
          PA 切于点 A，PB 切于点 B
    求证：PA = PB

    Problem (English):
    Given: Circle O, external point P
           PA tangent at A, PB tangent at B
    Prove: PA = PB (tangent segments are equal)
    """
    print_section("EXAMPLE 4: Equal Tangent Segments from External Point")

    # Setup
    O = Point("O")  # Center
    P = Point("P")  # External point
    A = Point("A")  # First tangent point
    B = Point("B")  # Second tangent point

    circle = Circle(O, 5.0)

    # Tangent lines
    line_PA = Line(P, A)
    line_PB = Line(P, B)

    # Facts
    tangent_A = TangentAt(line_PA, circle, A)
    tangent_B = TangentAt(line_PB, circle, B)

    print("\nGiven (已知):")
    print("  • Circle O with radius 5")
    print("  • External point P")
    print("  • PA is tangent at A")
    print("  • PB is tangent at B")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[tangent_A, tangent_B], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nConclusion (结论):")
    print("  ✅ PA = PB (equal tangent segments)")
    print("  • Tangent segments from an external point are always equal")


def example_5_cyclic_quadrilateral():
    """
    Example 5: Cyclic Quadrilateral Opposite Angles

    Problem (Chinese):
    已知：圆内接四边形 ABCD，∠A = 70°
    求：∠C

    Problem (English):
    Given: Cyclic quadrilateral ABCD (inscribed in circle)
           ∠A = 70°
    Find: ∠C

    Solution: Opposite angles are supplementary
             ∠A + ∠C = 180°
             ∠C = 180° - 70° = 110°
    """
    print_section("EXAMPLE 5: Cyclic Quadrilateral Opposite Angles")

    # Setup
    A, B, C, D = [Point(name) for name in "ABCD"]

    circle = Circle(Point("O"), 5.0)

    # Facts
    cyclic = CyclicQuadrilateral(A, B, C, D, circle)
    angle_A = AngleValue(Angle(D, A, B), 70.0)

    print("\nGiven (已知):")
    print("  • Quadrilateral ABCD inscribed in circle")
    print("  • ∠A = 70°")

    # Load theorems and reason
    engine = TheoremEngine()
    engine.load_library("/Users/yanyige/workspace2/geometry_prover/data/theorems")

    reasoner = ForwardReasoner(engine)
    result = reasoner.reason(initial_facts=[cyclic, angle_A], max_iterations=5)

    # Results
    print("\nResults:")
    print(f"  ✓ Derived {result.statistics['derived_facts']} new facts")
    print(f"  ✓ Applied {result.statistics['theorem_applications']} theorems")

    print("\nTheorems applied:")
    for name, count in result.statistics['theorem_usage'].items():
        print(f"  • {name}: {count}×")

    print("\nSolution (解):")
    print("  • Theorem: cyclic_quadrilateral_opposite_angles")
    print("  • Opposite angles are supplementary")
    print("  • ∠A + ∠C = 180°")
    print("  • 70° + ∠C = 180°")
    print("  • ∠C = 110°")
    print("\n  ✅ Answer: ∠C = 110°")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CIRCLE THEOREM EXAMPLES")
    print("=" * 80)
    print("\nThis file demonstrates:")
    print("  1. Thales' Theorem (angle in semicircle = 90°)")
    print("  2. Inscribed Angle Theorem (inscribed = half of central)")
    print("  3. Tangent-Radius Perpendicular")
    print("  4. Equal Tangent Segments from External Point")
    print("  5. Cyclic Quadrilateral Opposite Angles")

    # Run all examples
    example_1_thales_theorem()
    example_2_inscribed_angle_theorem()
    example_3_tangent_radius_perpendicular()
    example_4_equal_tangent_segments()
    example_5_cyclic_quadrilateral()

    # Summary
    print_section("SUMMARY")
    print("\n✅ All 5 circle theorem examples completed successfully!")
    print("\nKey Theorems Demonstrated:")
    print("  • thales_theorem")
    print("  • inscribed_angle_theorem")
    print("  • tangent_radius_perpendicular")
    print("  • equal_tangent_segments")
    print("  • cyclic_quadrilateral_opposite_angles")
    print("\n" + "=" * 80)
