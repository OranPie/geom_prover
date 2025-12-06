#!/bin/bash
# Run all Week 7 geometry prover examples
# Demonstrates extended validation of reasoning engines

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

cd "$PROJECT_ROOT"

echo "=================================================================="
echo "WEEK 7 EXAMPLES - EXTENDED VALIDATION"
echo "=================================================================="
echo ""
echo "This script runs all 8 Week 7 examples demonstrating:"
echo "  • Equality reasoning (segments and angles)"
echo "  • Parallel line reasoning"
echo "  • Angle properties and theorems"
echo "  • Advanced multi-category reasoning"
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Python path: $PYTHONPATH"
echo ""
echo "Press Enter to begin..."
read

# Example 6
echo ""
echo "=================================================================="
echo "EXAMPLE 6: Multi-Step Segment Equality"
echo "=================================================================="
echo "Problem: AB=CD=EF=GH, prove AB=GH"
echo "Demonstrates: Equality transitivity chaining"
echo ""
python3 examples/week7_examples/equality/multi_step_segment_equality.py
echo ""
echo "Example 6 complete. Press Enter to continue..."
read

# Example 7
echo ""
echo "=================================================================="
echo "EXAMPLE 7: Multi-Step Angle Equality"
echo "=================================================================="
echo "Problem: ∠ABC=∠DEF=∠GHI=∠JKL, prove ∠ABC=∠JKL"
echo "Demonstrates: Angle equality transitivity"
echo ""
python3 examples/week7_examples/equality/multi_step_angle_equality.py
echo ""
echo "Example 7 complete. Press Enter to continue..."
read

# Example 8
echo ""
echo "=================================================================="
echo "EXAMPLE 8: Mixed Equality Reasoning"
echo "=================================================================="
echo "Problem: Combining segment and angle equalities"
echo "Demonstrates: Isosceles triangles, mixed fact types"
echo ""
python3 examples/week7_examples/equality/mixed_equality_reasoning.py
echo ""
echo "Example 8 complete. Press Enter to continue..."
read

# Example 9
echo ""
echo "=================================================================="
echo "EXAMPLE 9: Parallel Transitivity Chain"
echo "=================================================================="
echo "Problem: AB||CD||EF||GH, prove AB||GH"
echo "Demonstrates: Parallel line transitivity"
echo ""
python3 examples/week7_examples/parallel/parallel_transitivity_chain.py
echo ""
echo "Example 9 complete. Press Enter to continue..."
read

# Example 10
echo ""
echo "=================================================================="
echo "EXAMPLE 10: Vertical Angles Proof"
echo "=================================================================="
echo "Problem: Intersecting lines create equal vertical angles"
echo "Demonstrates: Vertical angles theorem"
echo ""
python3 examples/week7_examples/angles/vertical_angles_proof.py
echo ""
echo "Example 10 complete. Press Enter to continue..."
read

# Example 11
echo ""
echo "=================================================================="
echo "EXAMPLE 11: Isosceles Triangle Base Angles"
echo "=================================================================="
echo "Problem: AB=AC → ∠ABC=∠ACB"
echo "Demonstrates: Isosceles triangle property"
echo ""
python3 examples/week7_examples/angles/isosceles_base_angles.py
echo ""
echo "Example 11 complete. Press Enter to continue..."
read

# Example 12
echo ""
echo "=================================================================="
echo "EXAMPLE 12: Combined Geometric Reasoning"
echo "=================================================================="
echo "Problem: Mix of parallel lines and segment equalities"
echo "Demonstrates: Multi-category theorem usage"
echo ""
python3 examples/week7_examples/advanced/combined_geometric_reasoning.py
echo ""
echo "Example 12 complete. Press Enter to continue..."
read

# Example 13
echo ""
echo "=================================================================="
echo "EXAMPLE 13: Deep Proof Chain"
echo "=================================================================="
echo "Problem: 6-segment chain, prove AB=MN"
echo "Demonstrates: Deep search, scalability"
echo ""
python3 examples/week7_examples/advanced/deep_proof_chain.py
echo ""
echo "Example 13 complete."
echo ""

# Summary
echo ""
echo "=================================================================="
echo "ALL WEEK 7 EXAMPLES COMPLETE"
echo "=================================================================="
echo ""
echo "Summary:"
echo "  ✓ Example 6: Multi-Step Segment Equality"
echo "  ✓ Example 7: Multi-Step Angle Equality"
echo "  ✓ Example 8: Mixed Equality Reasoning"
echo "  ✓ Example 9: Parallel Transitivity Chain"
echo "  ✓ Example 10: Vertical Angles Proof"
echo "  ✓ Example 11: Isosceles Triangle Base Angles"
echo "  ✓ Example 12: Combined Geometric Reasoning"
echo "  ✓ Example 13: Deep Proof Chain"
echo ""
echo "These examples demonstrated:"
echo "  • Equality reasoning (segments and angles)"
echo "  • Parallel line transitivity"
echo "  • Angle properties (vertical angles, isosceles)"
echo "  • Multi-category integration"
echo "  • Deep proof chains and scalability"
echo ""
echo "Theorem categories validated:"
echo "  ✓ Equality properties"
echo "  ✓ Parallel lines"
echo "  ✓ Angle properties"
echo "  ✓ Triangle properties"
echo ""
echo "For more information, see examples/week7_examples/README.md"
echo "=================================================================="
