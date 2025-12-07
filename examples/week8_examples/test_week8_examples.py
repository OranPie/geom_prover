"""
Automated tests for Week 8 examples.

These tests ensure the complex triangle congruence example runs
successfully and reports the expected derived facts.
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).parent.parent.parent
EXAMPLES_DIR = Path(__file__).parent


def run_example(example_path: Path) -> tuple[bool, str, str]:
    """Run an example script and capture output."""
    env = {
        "PYTHONPATH": f"{PROJECT_ROOT}:{PROJECT_ROOT.parent}",
        **subprocess.os.environ,
    }

    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            timeout=45,
            env=env,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout after 45 seconds"


def test_complex_triangle_congruence_example():
    """The complex triangle congruence example should reach expected milestones."""

    example = EXAMPLES_DIR / "complex_triangle_congruence.py"
    success, stdout, stderr = run_example(example)

    assert success, f"Example failed: {stderr}"
    assert "Derived congruent triangle" in stdout
    assert "Derived similar triangle" in stdout
    assert "Example 14 Complete" in stdout


def test_fact_expansion_walkthrough():
    """Fact expansion walkthrough should emit grouped derived facts."""

    example = EXAMPLES_DIR / "fact_expansion_walkthrough.py"
    success, stdout, stderr = run_example(example)

    assert success, f"Example failed: {stderr}"
    assert "IsoscelesTriangle" in stdout
    assert "EqualAngle" in stdout
    assert "Example 15 Complete" in stdout
