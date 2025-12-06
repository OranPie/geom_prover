"""
Tests for YAML theorem loader.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 19 - Test YAML loader
"""

import pytest
import tempfile
import os
from pathlib import Path

from geometry_prover.theorems.loader import (
    TheoremLoader, TheoremLoadError, load_theorems, load_theorem_library
)
from geometry_prover.theorems.theorem import Theorem
from geometry_prover.theorems.pattern import Variable, Pattern


class TestTheoremLoader:
    """Test TheoremLoader class."""

    def test_load_simple_theorem(self, tmp_path):
        """Test loading a simple theorem from YAML."""
        yaml_content = """
theorems:
  - name: "test_theorem"
    category: "test"
    description: "A test theorem"

    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"

    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"

    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        # Write to temp file
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        # Load theorems
        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        # Verify
        assert len(theorems) == 1
        theorem = theorems[0]
        assert theorem.metadata.name == "test_theorem"
        assert theorem.metadata.category == "test"
        assert theorem.metadata.description == "A test theorem"
        assert len(theorem.conditions) == 1
        assert len(theorem.conclusions) == 1
        assert len(theorem.variables) == 2

    def test_load_theorem_with_references(self, tmp_path):
        """Test loading theorem with references."""
        yaml_content = """
theorems:
  - name: "pythagorean"
    category: "triangle"
    description: "Pythagorean theorem"
    references:
      - "Euclid's Elements"
      - "Modern Geometry"

    conditions:
      - type: "RightAngle"
        angle: "?ABC"

    conclusions:
      - type: "PythagoreanRelation"
        hypotenuse: "?AC"

    variables:
      - name: "?ABC"
        type: "angle"
      - name: "?AC"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        assert len(theorems) == 1
        theorem = theorems[0]
        assert len(theorem.metadata.references) == 2
        assert "Euclid's Elements" in theorem.metadata.references

    def test_load_theorem_with_variable_descriptions(self, tmp_path):
        """Test loading theorem with variable descriptions."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"

    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"

    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"

    variables:
      - name: "?AB"
        type: "segment"
        description: "First segment"
      - name: "?CD"
        type: "segment"
        description: "Second segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        theorem = theorems[0]
        var_ab = theorem.get_variable("?AB")
        assert var_ab.description == "First segment"

    def test_load_multiple_theorems(self, tmp_path):
        """Test loading multiple theorems from one file."""
        yaml_content = """
theorems:
  - name: "theorem1"
    category: "test"
    description: "First"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"

  - name: "theorem2"
    category: "test"
    description: "Second"
    conditions:
      - type: "RightAngle"
        angle: "?ABC"
    conclusions:
      - type: "RightAngle"
        angle: "?ABC"
    variables:
      - name: "?ABC"
        type: "angle"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        assert len(theorems) == 2
        assert theorems[0].metadata.name == "theorem1"
        assert theorems[1].metadata.name == "theorem2"

    def test_load_theorem_multiple_conditions(self, tmp_path):
        """Test loading theorem with multiple conditions."""
        yaml_content = """
theorems:
  - name: "transitivity"
    category: "equality"
    description: "Transitive property"

    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?EF"

    conclusions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?EF"

    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
      - name: "?EF"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        theorem = theorems[0]
        assert len(theorem.conditions) == 2
        assert len(theorem.conclusions) == 1

    def test_load_theorem_multiple_conclusions(self, tmp_path):
        """Test loading theorem with multiple conclusions."""
        yaml_content = """
theorems:
  - name: "multi_conclusion"
    category: "test"
    description: "Multiple conclusions"

    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"

    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?AB"

    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        theorems = loader.load_from_file(str(yaml_file))

        theorem = theorems[0]
        assert len(theorem.conclusions) == 2

    def test_load_file_not_found(self):
        """Test loading non-existent file raises error."""
        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="File not found"):
            loader.load_from_file("/nonexistent/file.yaml")

    def test_load_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML raises error."""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("invalid: yaml: content: [[[")

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="YAML parse error"):
            loader.load_from_file(str(yaml_file))

    def test_load_missing_theorems_key(self, tmp_path):
        """Test loading YAML without 'theorems' key raises error."""
        yaml_content = """
some_other_key:
  - value: "test"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="must contain 'theorems' key"):
            loader.load_from_file(str(yaml_file))

    def test_load_missing_required_field(self, tmp_path):
        """Test loading theorem missing required field raises error."""
        yaml_content = """
theorems:
  - name: "incomplete"
    category: "test"
    # Missing conditions, conclusions, variables
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="Missing required field"):
            loader.load_from_file(str(yaml_file))

    def test_load_variable_missing_name(self, tmp_path):
        """Test loading variable without name raises error."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - type: "segment"  # Missing name
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="must have 'name' field"):
            loader.load_from_file(str(yaml_file))

    def test_load_variable_missing_type(self, tmp_path):
        """Test loading variable without type raises error."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"  # Missing type
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="must have 'type' field"):
            loader.load_from_file(str(yaml_file))

    def test_load_pattern_missing_type(self, tmp_path):
        """Test loading pattern without type raises error."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"
    conditions:
      - segment1: "?AB"  # Missing type
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="must have 'type' field"):
            loader.load_from_file(str(yaml_file))

    def test_load_from_directory(self, tmp_path):
        """Test loading theorems from directory."""
        # Create multiple YAML files
        yaml1 = """
theorems:
  - name: "theorem1"
    category: "test"
    description: "First"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        yaml2 = """
theorems:
  - name: "theorem2"
    category: "test"
    description: "Second"
    conditions:
      - type: "RightAngle"
        angle: "?ABC"
    conclusions:
      - type: "RightAngle"
        angle: "?ABC"
    variables:
      - name: "?ABC"
        type: "angle"
"""
        (tmp_path / "file1.yaml").write_text(yaml1)
        (tmp_path / "file2.yaml").write_text(yaml2)

        loader = TheoremLoader()
        theorems = loader.load_from_directory(str(tmp_path))

        assert len(theorems) == 2
        names = {t.metadata.name for t in theorems}
        assert "theorem1" in names
        assert "theorem2" in names

    def test_load_from_nonexistent_directory(self):
        """Test loading from non-existent directory raises error."""
        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="Directory not found"):
            loader.load_from_directory("/nonexistent/directory")

    def test_load_from_empty_directory(self, tmp_path):
        """Test loading from directory with no YAML files raises error."""
        loader = TheoremLoader()
        with pytest.raises(TheoremLoadError, match="No YAML files found"):
            loader.load_from_directory(str(tmp_path))

    def test_convenience_function_load_theorems(self, tmp_path):
        """Test convenience function load_theorems."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        theorems = load_theorems(str(yaml_file))
        assert len(theorems) == 1
        assert theorems[0].metadata.name == "test"

    def test_convenience_function_load_library(self, tmp_path):
        """Test convenience function load_theorem_library."""
        yaml_content = """
theorems:
  - name: "test"
    category: "test"
    description: "Test"
    conditions:
      - type: "EqualSegment"
        segment1: "?AB"
        segment2: "?CD"
    conclusions:
      - type: "EqualSegment"
        segment1: "?CD"
        segment2: "?AB"
    variables:
      - name: "?AB"
        type: "segment"
      - name: "?CD"
        type: "segment"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        theorems = load_theorem_library(str(tmp_path))
        assert len(theorems) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
