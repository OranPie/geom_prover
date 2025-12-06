"""
Test loading actual theorem files from the data directory.
"""

import pytest
from pathlib import Path
from geometry_prover.theorems.loader import load_theorems, TheoremLoadError


class TestLoadActualTheoremFiles:
    """Test loading actual theorem YAML files."""

    def test_load_example_theorems(self):
        """Test loading example_theorems.yaml file."""
        # Path to example theorems file
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "example_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Example theorems file not found: {theorem_file}")

        # Load theorems
        theorems = load_theorems(str(theorem_file))

        # Should load 3 example theorems
        assert len(theorems) >= 3

        # Check theorem names
        theorem_names = {t.metadata.name for t in theorems}
        assert "isosceles_base_angles" in theorem_names
        assert "vertical_angles" in theorem_names
        assert "pythagorean_theorem" in theorem_names

    def test_isosceles_theorem_structure(self):
        """Test structure of isosceles base angles theorem."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "example_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Example theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        isosceles = next((t for t in theorems if t.metadata.name == "isosceles_base_angles"), None)

        assert isosceles is not None
        assert isosceles.metadata.category == "triangle_properties"
        assert len(isosceles.conditions) == 1
        assert len(isosceles.conclusions) == 1
        assert len(isosceles.variables) >= 4  # At least points and segments

    def test_vertical_angles_theorem_structure(self):
        """Test structure of vertical angles theorem."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "example_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Example theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        vertical = next((t for t in theorems if t.metadata.name == "vertical_angles"), None)

        assert vertical is not None
        assert vertical.metadata.category == "angle_properties"
        assert len(vertical.conditions) == 2  # Two On conditions
        assert len(vertical.conclusions) == 2  # Two angle equalities

    def test_pythagorean_theorem_structure(self):
        """Test structure of Pythagorean theorem."""
        theorem_file = Path(__file__).parent.parent.parent / "geometry_prover" / "data" / "theorems" / "example_theorems.yaml"

        if not theorem_file.exists():
            pytest.skip(f"Example theorems file not found: {theorem_file}")

        theorems = load_theorems(str(theorem_file))
        pythag = next((t for t in theorems if t.metadata.name == "pythagorean_theorem"), None)

        assert pythag is not None
        assert pythag.metadata.category == "triangle_properties"
        assert len(pythag.conditions) == 1  # RightAngle condition
        assert len(pythag.conclusions) == 1  # PythagoreanRelation conclusion


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
