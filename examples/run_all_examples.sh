#!/bin/bash
# Run all geometry prover examples
# This script demonstrates the complete Week 1-6 pipeline

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

cd "$PROJECT_ROOT"

echo "=================================================================="
echo "GEOMETRY PROVER - EXAMPLE DEMONSTRATIONS"
echo "=================================================================="
echo ""
echo "This script will run all examples demonstrating the complete"
echo "pipeline from DSL parsing through automated proof generation."
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Python path: $PYTHONPATH"
echo ""
echo "Press Enter to begin..."
read

# Example 1
echo ""
echo "=================================================================="
echo "EXAMPLE 1: Simple Symmetry Proof"
echo "=================================================================="
echo "Demonstrates: Basic pipeline, single theorem application"
echo "Complexity: Basic"
echo ""
python3 examples/example_01_simple_symmetry.py
echo ""
echo "Example 1 complete. Press Enter to continue..."
read

# Example 2
echo ""
echo "=================================================================="
echo "EXAMPLE 2: Transitivity Chain"
echo "=================================================================="
echo "Demonstrates: Multi-step proof, strategy comparison"
echo "Complexity: Intermediate"
echo ""
python3 examples/example_02_transitivity.py
echo ""
echo "Example 2 complete. Press Enter to continue..."
read

# Example 3
echo ""
echo "=================================================================="
echo "EXAMPLE 3: Isosceles Triangle"
echo "=================================================================="
echo "Demonstrates: Complex objects, exploratory reasoning"
echo "Complexity: Advanced"
echo ""
python3 examples/example_03_isosceles_triangle.py
echo ""
echo "Example 3 complete. Press Enter to continue..."
read

# Example 4
echo ""
echo "=================================================================="
echo "EXAMPLE 4: Detailed Proof Steps"
echo "=================================================================="
echo "Demonstrates: Step-by-step proof visualization"
echo "Complexity: Educational"
echo ""
python3 examples/example_04_detailed_proof.py
echo ""
echo "Example 4 complete. Press Enter to continue..."
read

# Example 5
echo ""
echo "=================================================================="
echo "EXAMPLE 5: Complete Workflow"
echo "=================================================================="
echo "Demonstrates: Full pipeline with all strategies"
echo "Complexity: Comprehensive"
echo ""
python3 examples/example_05_complete_workflow.py
echo ""
echo "Example 5 complete."
echo ""

# Summary
echo ""
echo "=================================================================="
echo "ALL EXAMPLES COMPLETE"
echo "=================================================================="
echo ""
echo "Summary:"
echo "  ✓ Example 1: Simple Symmetry Proof"
echo "  ✓ Example 2: Transitivity Chain"
echo "  ✓ Example 3: Isosceles Triangle"
echo "  ✓ Example 4: Detailed Proof Steps"
echo "  ✓ Example 5: Complete Workflow"
echo ""
echo "These examples demonstrated:"
echo "  • Complete DSL-to-proof pipeline (Week 1-6)"
echo "  • DSL parsing and semantic extraction"
echo "  • Theorem loading and application"
echo "  • Forward, backward, and bidirectional reasoning"
echo "  • Multiple search strategies (BFS, DFS, Best-First)"
echo "  • Proof tree construction and visualization"
echo "  • Statistics tracking and performance analysis"
echo ""
echo "For more information, see examples/README.md"
echo "=================================================================="
