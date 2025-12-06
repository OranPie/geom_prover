"""
YAML theorem loader for loading theorems from YAML files.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 4, Day 19 - YAML schema and loader

This module loads theorem definitions from YAML files and converts them
to Theorem objects. This enables data-driven theorem definitions without
hardcoding theorems in Python.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml

from geometry_prover.theorems.theorem import Theorem, TheoremMetadata, TheoremBuilder, Constraint
from geometry_prover.theorems.pattern import Variable, Pattern


class TheoremLoadError(Exception):
    """Exception raised when theorem loading fails."""
    pass


class TheoremLoader:
    """
    Loads theorems from YAML files.

    YAML Format:
        theorems:
          - name: "theorem_name"
            category: "category_name"
            description: "Description"
            references: ["ref1", "ref2"]  # Optional

            conditions:
              - type: "FactType"
                param1: "?Variable1"
                param2: "?Variable2"

            conclusions:
              - type: "FactType"
                param1: "?Variable1"

            variables:
              - name: "?Variable1"
                type: "point|segment|angle|line|circle|triangle"
                description: "Optional description"
    """

    def __init__(self):
        """Initialize theorem loader."""
        pass

    def load_from_file(self, file_path: str) -> List[Theorem]:
        """
        Load theorems from a YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            List of Theorem objects

        Raises:
            TheoremLoadError: If loading fails
        """
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise TheoremLoadError(f"File not found: {file_path}")
        except yaml.YAMLError as e:
            raise TheoremLoadError(f"YAML parse error: {e}")

        if not data or 'theorems' not in data:
            raise TheoremLoadError("YAML file must contain 'theorems' key")

        theorems = []
        for theorem_data in data['theorems']:
            try:
                theorem = self._load_theorem(theorem_data)
                theorems.append(theorem)
            except Exception as e:
                theorem_name = theorem_data.get('name', 'unknown')
                raise TheoremLoadError(f"Error loading theorem '{theorem_name}': {e}")

        return theorems

    def load_from_directory(self, directory: str) -> List[Theorem]:
        """
        Load all theorems from YAML files in a directory.

        Args:
            directory: Path to directory containing YAML files

        Returns:
            List of all loaded theorems

        Raises:
            TheoremLoadError: If loading fails
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            raise TheoremLoadError(f"Directory not found: {directory}")

        theorems = []
        # Search for YAML files in directory and all subdirectories
        # Use rglob to search recursively (includes current directory)
        yaml_files = list(dir_path.rglob("*.yaml")) + list(dir_path.rglob("*.yml"))

        if not yaml_files:
            raise TheoremLoadError(f"No YAML files found in {directory}")

        for yaml_file in yaml_files:
            try:
                file_theorems = self.load_from_file(str(yaml_file))
                theorems.extend(file_theorems)
            except TheoremLoadError as e:
                raise TheoremLoadError(f"Error loading {yaml_file.name}: {e}")

        return theorems

    def _load_theorem(self, data: Dict[str, Any]) -> Theorem:
        """
        Load a single theorem from dictionary data.

        Args:
            data: Dictionary containing theorem data

        Returns:
            Theorem object

        Raises:
            ValueError: If theorem data is invalid
        """
        # Validate required fields
        required_fields = ['name', 'conditions', 'conclusions', 'variables']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Build theorem using TheoremBuilder
        builder = TheoremBuilder(data['name'])

        # Set optional metadata fields
        if 'category' in data:
            builder.category(data['category'])
        if 'description' in data:
            builder.description(data['description'])
        if 'references' in data:
            for ref in data['references']:
                builder.add_reference(ref)

        # Load variables
        for var_data in data['variables']:
            variable = self._load_variable(var_data)
            builder.add_variable(variable)

        # Load conditions
        for cond_data in data['conditions']:
            pattern = self._load_pattern(cond_data)
            builder.add_condition(pattern)

        # Load conclusions
        for concl_data in data['conclusions']:
            pattern = self._load_pattern(concl_data)
            builder.add_conclusion(pattern)

        # Load constraints (optional)
        if 'constraints' in data:
            for constr_data in data['constraints']:
                constraint = self._load_constraint(constr_data)
                builder.add_constraint(constraint)

        return builder.build()

    def _load_variable(self, data: Dict[str, Any]) -> Variable:
        """
        Load a variable from dictionary data.

        Args:
            data: Dictionary containing variable data

        Returns:
            Variable object

        Raises:
            ValueError: If variable data is invalid
        """
        if 'name' not in data:
            raise ValueError("Variable must have 'name' field")
        if 'type' not in data:
            raise ValueError(f"Variable {data['name']} must have 'type' field")

        name = data['name']
        var_type = data['type']
        description = data.get('description', '')
        derived_from = data.get('derived_from', None)

        return Variable(name, var_type, description, derived_from)

    def _load_pattern(self, data: Dict[str, Any]) -> Pattern:
        """
        Load a pattern from dictionary data.

        Args:
            data: Dictionary containing pattern data

        Returns:
            Pattern object

        Raises:
            ValueError: If pattern data is invalid
        """
        if 'type' not in data:
            raise ValueError("Pattern must have 'type' field")

        fact_type = data['type']

        # Extract parameters (all fields except 'type')
        parameters = {k: v for k, v in data.items() if k != 'type'}

        return Pattern(fact_type, parameters)

    def _load_constraint(self, data: Dict[str, Any]) -> Constraint:
        """
        Load a constraint from dictionary data.

        Args:
            data: Dictionary containing constraint data

        Returns:
            Constraint object

        Raises:
            ValueError: If constraint data is invalid
        """
        if 'type' not in data:
            raise ValueError("Constraint must have 'type' field")

        constraint_type = data['type']

        # Extract parameters (all fields except 'type')
        parameters = {k: v for k, v in data.items() if k != 'type'}

        return Constraint(constraint_type=constraint_type, parameters=parameters)


def load_theorems(file_path: str) -> List[Theorem]:
    """
    Convenience function to load theorems from a file.

    Args:
        file_path: Path to YAML file

    Returns:
        List of Theorem objects
    """
    loader = TheoremLoader()
    return loader.load_from_file(file_path)


def load_theorem_library(directory: str) -> List[Theorem]:
    """
    Convenience function to load all theorems from a directory.

    Args:
        directory: Path to directory containing YAML files

    Returns:
        List of all Theorem objects
    """
    loader = TheoremLoader()
    return loader.load_from_directory(directory)
