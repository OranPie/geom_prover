"""
Test parsing actual DSL example files.

Validates that all example .dsl files can be successfully parsed.
"""

import pytest
from pathlib import Path
from geometry_prover.dsl.parser import parse_program
from geometry_prover.dsl.ast_nodes import Program


def test_parse_all_examples():
    """Test parsing all example DSL files."""
    examples_dir = Path("examples/dsl")

    if not examples_dir.exists():
        pytest.skip("Examples directory not found")

    dsl_files = list(examples_dir.glob("*.dsl"))
    assert len(dsl_files) > 0, "No DSL example files found"

    for dsl_file in dsl_files:
        print(f"\nParsing {dsl_file.name}...")
        text = dsl_file.read_text()

        # Should parse without errors
        program = parse_program(text)
        assert isinstance(program, Program)
        assert len(program.statements) > 0

        print(f"  ✓ {len(program.statements)} statements parsed successfully")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
