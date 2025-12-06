"""
Test loading core theorems library.
"""

import pytest
from pathlib import Path
from geometry_prover.theorems.loader import load_theorems, load_theorem_library


class TestCoreTheorems:
    """Test loading core theorems."""

    def test_load_core_theorems_file(self):
        """Test loading core_theorems.yaml file."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "core_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Core theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))

        # Should load 10 core theorems
        assert len(theorems) == 10

    def test_core_theorems_names(self):
        """Test that all expected core theorems are present."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "core_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Core theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        names = {t.metadata.name for t in theorems}

        expected_names = {
            "equality_symmetry",
            "equality_transitivity",
            "angle_equality_symmetry",
            "angle_equality_transitivity",
            "parallel_symmetry",
            "parallel_transitivity",
            "perpendicular_symmetry",
            "right_angle_reflexive",
            "segment_equality_reflexive",
            "collinearity_symmetry"
        }

        assert names == expected_names

    def test_load_entire_theorem_directory(self):
        """Test loading all theorems from directory."""
        theorem_dir = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems"

        if not theorem_dir.exists():
            pytest.skip(f"Theorem directory not found: {theorem_dir}")

        theorems = load_theorem_library(str(theorem_dir))

        # Should load theorems from both example_theorems.yaml and core_theorems.yaml
        assert len(theorems) >= 13  # 3 from example + 10 from core

    def test_equality_symmetry_structure(self):
        """Test structure of equality symmetry theorem."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "core_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Core theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        symm = next((t for t in theorems if t.metadata.name == "equality_symmetry"), None)

        assert symm is not None
        assert symm.metadata.category == "equality_properties"
        assert len(symm.conditions) == 1
        assert len(symm.conclusions) == 1
        assert len(symm.variables) == 2

    def test_equality_transitivity_structure(self):
        """Test structure of equality transitivity theorem."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "core_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Core theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        trans = next((t for t in theorems if t.metadata.name == "equality_transitivity"), None)

        assert trans is not None
        assert trans.metadata.category == "equality_properties"
        assert len(trans.conditions) == 2
        assert len(trans.conclusions) == 1
        assert len(trans.variables) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
