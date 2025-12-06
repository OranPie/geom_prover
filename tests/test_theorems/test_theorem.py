"""
Tests for Theorem class.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 17 - Test theorem representation
"""

import pytest
from geometry_prover.theorems.theorem import (
    Theorem, TheoremMetadata, TheoremBuilder
)
from geometry_prover.theorems.pattern import Variable, Pattern, PatternTemplate


class TestTheoremMetadata:
    """Test TheoremMetadata class."""

    def test_create_metadata(self):
        """Test creating theorem metadata."""
        metadata = TheoremMetadata(
            name="test_theorem",
            category="test_category",
            description="A test theorem"
        )

        assert metadata.name == "test_theorem"
        assert metadata.category == "test_category"
        assert metadata.description == "A test theorem"
        assert metadata.references == []

    def test_metadata_with_references(self):
        """Test metadata with references."""
        metadata = TheoremMetadata(
            name="pythagorean",
            category="triangle_properties",
            description="Pythagorean theorem",
            references=["Euclid's Elements", "Modern Geometry Textbook"]
        )

        assert len(metadata.references) == 2
        assert "Euclid's Elements" in metadata.references


class TestTheorem:
    """Test Theorem class."""

    def test_create_simple_theorem(self):
        """Test creating a simple theorem."""
        # Isosceles base angles theorem
        metadata = TheoremMetadata(
            name="isosceles_base_angles",
            category="triangle_properties",
            description="Base angles of isosceles triangle are equal"
        )

        variables = [
            Variable("?A", "point"),
            Variable("?B", "point"),
            Variable("?C", "point"),
            Variable("?AB", "segment"),
            Variable("?AC", "segment"),
            Variable("?ABC", "angle"),
            Variable("?ACB", "angle"),
        ]

        conditions = [
            PatternTemplate.equal_segment("?AB", "?AC")
        ]

        conclusions = [
            PatternTemplate.equal_angle("?ABC", "?ACB")
        ]

        theorem = Theorem(metadata, conditions, conclusions, variables)

        assert theorem.metadata.name == "isosceles_base_angles"
        assert len(theorem.conditions) == 1
        assert len(theorem.conclusions) == 1
        assert len(theorem.variables) == 7  # A, B, C, AB, AC, ABC, ACB

    def test_theorem_validation_requires_conditions(self):
        """Test that theorem requires at least one condition."""
        metadata = TheoremMetadata("test", "test", "test")
        variables = [Variable("?A", "point")]
        conditions = []  # No conditions
        conclusions = [PatternTemplate.equal_segment("?AB", "?CD")]

        with pytest.raises(ValueError, match="has no conditions"):
            Theorem(metadata, conditions, conclusions, variables)

    def test_theorem_validation_requires_conclusions(self):
        """Test that theorem requires at least one conclusion."""
        metadata = TheoremMetadata("test", "test", "test")
        variables = [Variable("?A", "point")]
        conditions = [PatternTemplate.equal_segment("?AB", "?CD")]
        conclusions = []  # No conclusions

        with pytest.raises(ValueError, match="has no conclusions"):
            Theorem(metadata, conditions, conclusions, variables)

    def test_theorem_validation_undeclared_variables(self):
        """Test that theorem rejects undeclared variables."""
        metadata = TheoremMetadata("test", "test", "test")
        variables = [Variable("?A", "point")]  # Only ?A declared
        conditions = [PatternTemplate.equal_segment("?AB", "?CD")]  # Uses ?AB, ?CD
        conclusions = [PatternTemplate.equal_angle("?ABC", "?DEF")]

        with pytest.raises(ValueError, match="undeclared variables"):
            Theorem(metadata, conditions, conclusions, variables)

    def test_get_variable(self):
        """Test getting variable by name."""
        var_a = Variable("?A", "point")
        var_b = Variable("?B", "point")

        metadata = TheoremMetadata("test", "test", "test")
        variables = [var_a, var_b]
        conditions = [Pattern("On", {"point": "?A", "line": "?B"})]
        conclusions = [Pattern("Test", {})]

        theorem = Theorem(metadata, conditions, conclusions, variables)

        assert theorem.get_variable("?A") == var_a
        assert theorem.get_variable("?B") == var_b
        assert theorem.get_variable("?C") is None

    def test_theorem_repr(self):
        """Test theorem repr."""
        metadata = TheoremMetadata("test", "test", "A test")
        variables = [Variable("?A", "point")]
        conditions = [Pattern("Test", {"param": "?A"})]
        conclusions = [Pattern("Result", {"value": "?A"})]

        theorem = Theorem(metadata, conditions, conclusions, variables)
        repr_str = repr(theorem)

        assert "Theorem" in repr_str
        assert "test" in repr_str

    def test_theorem_str(self):
        """Test theorem string representation."""
        metadata = TheoremMetadata(
            "isosceles_base_angles",
            "triangle_properties",
            "Base angles equal in isosceles triangle"
        )
        variables = [
            Variable("?A", "point", "Apex"),
            Variable("?B", "point", "Base vertex 1"),
            Variable("?AB", "segment"),
            Variable("?AC", "segment"),
            Variable("?ABC", "angle"),
            Variable("?ACB", "angle"),
        ]
        conditions = [PatternTemplate.equal_segment("?AB", "?AC")]
        conclusions = [PatternTemplate.equal_angle("?ABC", "?ACB")]

        theorem = Theorem(metadata, conditions, conclusions, variables)
        str_repr = str(theorem)

        assert "isosceles_base_angles" in str_repr
        assert "triangle_properties" in str_repr
        assert "Conditions:" in str_repr
        assert "Conclusions:" in str_repr
        assert "Variables:" in str_repr


class TestTheoremBuilder:
    """Test TheoremBuilder class."""

    def test_builder_basic_usage(self):
        """Test basic builder usage."""
        theorem = (TheoremBuilder("test_theorem")
                   .category("test_category")
                   .description("A test theorem")
                   .add_variable(Variable("?A", "point"))
                   .add_variable(Variable("?B", "point"))
                   .add_condition(Pattern("On", {"point": "?A", "line": "?B"}))
                   .add_conclusion(Pattern("Result", {"value": "?A"}))
                   .build())

        assert theorem.metadata.name == "test_theorem"
        assert theorem.metadata.category == "test_category"
        assert theorem.metadata.description == "A test theorem"
        assert len(theorem.variables) == 2
        assert len(theorem.conditions) == 1
        assert len(theorem.conclusions) == 1

    def test_builder_with_references(self):
        """Test builder with references."""
        theorem = (TheoremBuilder("pythagorean")
                   .category("triangle_properties")
                   .description("Pythagorean theorem")
                   .add_reference("Euclid")
                   .add_reference("Modern Geometry")
                   .add_variable(Variable("?A", "point"))
                   .add_variable(Variable("?B", "point"))
                   .add_variable(Variable("?C", "point"))
                   .add_variable(Variable("?ABC", "angle"))
                   .add_condition(PatternTemplate.right_angle("?ABC"))
                   .add_conclusion(Pattern("PythagoreanRelation", {}))
                   .build())

        assert len(theorem.metadata.references) == 2
        assert "Euclid" in theorem.metadata.references

    def test_builder_isosceles_theorem(self):
        """Test building isosceles base angles theorem."""
        theorem = (TheoremBuilder("isosceles_base_angles")
                   .category("triangle_properties")
                   .description("Base angles of isosceles triangle are equal")
                   .add_variable(Variable("?A", "point", "Apex"))
                   .add_variable(Variable("?B", "point", "Base vertex 1"))
                   .add_variable(Variable("?C", "point", "Base vertex 2"))
                   .add_variable(Variable("?AB", "segment"))
                   .add_variable(Variable("?AC", "segment"))
                   .add_variable(Variable("?ABC", "angle"))
                   .add_variable(Variable("?ACB", "angle"))
                   .add_condition(PatternTemplate.equal_segment("?AB", "?AC"))
                   .add_conclusion(PatternTemplate.equal_angle("?ABC", "?ACB"))
                   .build())

        assert theorem.metadata.name == "isosceles_base_angles"
        assert len(theorem.variables) == 7
        assert len(theorem.conditions) == 1
        assert len(theorem.conclusions) == 1

    def test_builder_defaults(self):
        """Test builder default values."""
        theorem = (TheoremBuilder("test")
                   .add_variable(Variable("?A", "point"))
                   .add_condition(Pattern("Test", {"point": "?A"}))
                   .add_conclusion(Pattern("Result", {"value": "?A"}))
                   .build())

        assert theorem.metadata.category == "uncategorized"
        assert theorem.metadata.description == "No description"
        assert theorem.metadata.references == []


class TestCompleteTheoremExamples:
    """Test complete theorem examples."""

    def test_vertical_angles_theorem(self):
        """Test vertical angles theorem."""
        theorem = (TheoremBuilder("vertical_angles")
                   .category("angle_properties")
                   .description("Vertical angles formed by intersecting lines are equal")
                   .add_variable(Variable("?P", "point", "Intersection point"))
                   .add_variable(Variable("?A", "point"))
                   .add_variable(Variable("?B", "point"))
                   .add_variable(Variable("?C", "point"))
                   .add_variable(Variable("?D", "point"))
                   .add_variable(Variable("?AB", "line"))
                   .add_variable(Variable("?CD", "line"))
                   .add_variable(Variable("?APC", "angle"))
                   .add_variable(Variable("?BPD", "angle"))
                   .add_variable(Variable("?APD", "angle"))
                   .add_variable(Variable("?BPC", "angle"))
                   .add_condition(PatternTemplate.on_point("?P", "?AB"))
                   .add_condition(PatternTemplate.on_point("?P", "?CD"))
                   .add_conclusion(PatternTemplate.equal_angle("?APC", "?BPD"))
                   .add_conclusion(PatternTemplate.equal_angle("?APD", "?BPC"))
                   .build())

        assert len(theorem.conditions) == 2
        assert len(theorem.conclusions) == 2
        assert theorem.metadata.name == "vertical_angles"

    def test_parallel_transversal_theorem(self):
        """Test parallel lines transversal theorem (alternate interior angles)."""
        theorem = (TheoremBuilder("parallel_transversal_alternate_interior")
                   .category("parallel_lines")
                   .description("Alternate interior angles are equal when transversal crosses parallel lines")
                   .add_variable(Variable("?AB", "line", "First parallel line"))
                   .add_variable(Variable("?CD", "line", "Second parallel line"))
                   .add_variable(Variable("?EF", "line", "Transversal"))
                   .add_variable(Variable("?P", "point", "Intersection with AB"))
                   .add_variable(Variable("?Q", "point", "Intersection with CD"))
                   .add_variable(Variable("?APQ", "angle"))
                   .add_variable(Variable("?CQP", "angle"))
                   .add_condition(PatternTemplate.parallel("?AB", "?CD"))
                   .add_condition(PatternTemplate.on_point("?P", "?AB"))
                   .add_condition(PatternTemplate.on_point("?P", "?EF"))
                   .add_condition(PatternTemplate.on_point("?Q", "?CD"))
                   .add_condition(PatternTemplate.on_point("?Q", "?EF"))
                   .add_conclusion(PatternTemplate.equal_angle("?APQ", "?CQP"))
                   .build())

        assert len(theorem.conditions) == 5
        assert len(theorem.conclusions) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
