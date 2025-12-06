"""
Test Suite for Week 7 Examples
================================

Automated tests to validate all Week 7 examples run successfully.
"""

import subprocess
import sys
from pathlib import Path
import pytest


# Get the project root and examples directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
EXAMPLES_DIR = Path(__file__).parent


def run_example(example_path: Path) -> tuple[bool, str, str]:
    """
    Run an example and return success status, stdout, stderr.

    Returns:
        (success, stdout, stderr)
    """
    env = {
        'PYTHONPATH': f"{PROJECT_ROOT}:{PROJECT_ROOT.parent}"
    }

    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            timeout=30,
            env={**subprocess.os.environ, **env}
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout after 30 seconds"
    except Exception as e:
        return False, "", str(e)


class TestEqualityExamples:
    """Test equality reasoning examples."""

    def test_example_06_multi_step_segment_equality(self):
        """Test Example 6: Multi-step segment equality."""
        example = EXAMPLES_DIR / "equality" / "multi_step_segment_equality.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 6 failed:\n{stderr}"
        assert "Example 6 Complete" in stdout
        assert "Successfully proved AB = GH" in stdout

    def test_example_07_multi_step_angle_equality(self):
        """Test Example 7: Multi-step angle equality."""
        example = EXAMPLES_DIR / "equality" / "multi_step_angle_equality.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 7 failed:\n{stderr}"
        assert "Example 7 Complete" in stdout
        assert "Successfully proved" in stdout

    def test_example_08_mixed_equality_reasoning(self):
        """Test Example 8: Mixed equality reasoning."""
        example = EXAMPLES_DIR / "equality" / "mixed_equality_reasoning.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 8 failed:\n{stderr}"
        assert "Example 8 Complete" in stdout
        assert "Successfully demonstrated mixed equality reasoning" in stdout


class TestParallelExamples:
    """Test parallel line examples."""

    def test_example_09_parallel_transitivity_chain(self):
        """Test Example 9: Parallel transitivity chain."""
        example = EXAMPLES_DIR / "parallel" / "parallel_transitivity_chain.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 9 failed:\n{stderr}"
        assert "Example 9 Complete" in stdout
        assert "Successfully proved AB || GH" in stdout


class TestAngleExamples:
    """Test angle reasoning examples."""

    def test_example_10_vertical_angles_proof(self):
        """Test Example 10: Vertical angles proof."""
        example = EXAMPLES_DIR / "angles" / "vertical_angles_proof.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 10 failed:\n{stderr}"
        assert "Example 10 Complete" in stdout
        assert "Demonstrated vertical angles theorem" in stdout

    def test_example_11_isosceles_base_angles(self):
        """Test Example 11: Isosceles triangle base angles."""
        example = EXAMPLES_DIR / "angles" / "isosceles_base_angles.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 11 failed:\n{stderr}"
        assert "Example 11 Complete" in stdout
        assert "Demonstrated isosceles triangle property" in stdout


class TestAdvancedExamples:
    """Test advanced reasoning examples."""

    def test_example_12_combined_geometric_reasoning(self):
        """Test Example 12: Combined geometric reasoning."""
        example = EXAMPLES_DIR / "advanced" / "combined_geometric_reasoning.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 12 failed:\n{stderr}"
        assert "Example 12 Complete" in stdout
        assert "Successfully processed" in stdout

    def test_example_13_deep_proof_chain(self):
        """Test Example 13: Deep proof chain."""
        example = EXAMPLES_DIR / "advanced" / "deep_proof_chain.py"
        success, stdout, stderr = run_example(example)

        assert success, f"Example 13 failed:\n{stderr}"
        assert "Example 13 Complete" in stdout
        assert "Successfully proved AB = MN through deep chain" in stdout


class TestExampleMetrics:
    """Test that examples produce expected metrics."""

    def test_all_examples_complete_quickly(self):
        """Verify all examples complete in reasonable time."""
        examples = [
            EXAMPLES_DIR / "equality" / "multi_step_segment_equality.py",
            EXAMPLES_DIR / "equality" / "multi_step_angle_equality.py",
            EXAMPLES_DIR / "equality" / "mixed_equality_reasoning.py",
            EXAMPLES_DIR / "parallel" / "parallel_transitivity_chain.py",
            EXAMPLES_DIR / "angles" / "vertical_angles_proof.py",
            EXAMPLES_DIR / "angles" / "isosceles_base_angles.py",
            EXAMPLES_DIR / "advanced" / "combined_geometric_reasoning.py",
            EXAMPLES_DIR / "advanced" / "deep_proof_chain.py",
        ]

        for example in examples:
            success, stdout, stderr = run_example(example)
            assert success, f"{example.name} failed to complete"

    def test_examples_use_theorems(self):
        """Verify examples actually apply theorems."""
        example = EXAMPLES_DIR / "equality" / "multi_step_segment_equality.py"
        success, stdout, stderr = run_example(example)

        assert success
        assert "equality_transitivity" in stdout or "Theorem usage" in stdout

    def test_examples_show_statistics(self):
        """Verify examples output statistics."""
        example = EXAMPLES_DIR / "equality" / "multi_step_segment_equality.py"
        success, stdout, stderr = run_example(example)

        assert success
        assert "Iterations:" in stdout or "iterations" in stdout.lower()
        assert "Time:" in stdout or "ms" in stdout


def test_all_examples_exist():
    """Verify all expected example files exist."""
    expected_examples = [
        "equality/multi_step_segment_equality.py",
        "equality/multi_step_angle_equality.py",
        "equality/mixed_equality_reasoning.py",
        "parallel/parallel_transitivity_chain.py",
        "angles/vertical_angles_proof.py",
        "angles/isosceles_base_angles.py",
        "advanced/combined_geometric_reasoning.py",
        "advanced/deep_proof_chain.py",
    ]

    for example_path in expected_examples:
        full_path = EXAMPLES_DIR / example_path
        assert full_path.exists(), f"Example not found: {example_path}"


def test_readme_exists():
    """Verify Week 7 README exists."""
    readme = EXAMPLES_DIR / "README.md"
    assert readme.exists(), "Week 7 README.md not found"

    content = readme.read_text()
    assert "Week 7" in content
    assert "Example 6" in content or "Example 13" in content


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
