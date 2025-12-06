"""
ProveGoalExtractor - Extracts proof goals from AST.

The ProveGoalExtractor takes ProveStatement nodes from the AST and
extracts the goal constraints, converting them into Facts.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 3, Task 3.3 - ProveGoalExtractor Implementation
- Extract proof goals from ProveStatement nodes
- Convert goals to Facts using ConstraintBuilder
"""

from typing import List
from geometry_prover.dsl.ast_nodes import ProveStatement
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.semantic.constraint_builder import ConstraintBuilder
from geometry_prover.facts.fact_types import Fact


class ProveGoalExtractor:
    """
    Extracts proof goals from AST ProveStatement nodes.

    Uses ConstraintBuilder to convert goal constraints into Facts.
    """

    def __init__(self, model: GeometryModel):
        """
        Initialize prove goal extractor.

        Args:
            model: GeometryModel to use for object resolution
        """
        self.model = model
        self.constraint_builder = ConstraintBuilder(model)

    def extract_goal(self, prove_stmt: ProveStatement) -> Fact:
        """
        Extract goal fact from ProveStatement.

        Args:
            prove_stmt: ProveStatement AST node

        Returns:
            Fact representing the proof goal

        Raises:
            ValueError: If goal cannot be extracted
        """
        # The goal is stored in the ProveStatement's goal attribute
        # which is a constraint node
        goal_constraint = prove_stmt.goal

        # Use ConstraintBuilder to convert constraint to fact
        goal_fact = self.constraint_builder.build_constraint(goal_constraint)

        if goal_fact is None:
            raise ValueError("Failed to extract goal from prove statement")

        return goal_fact

    def extract_goals(self, prove_stmts: List[ProveStatement]) -> List[Fact]:
        """
        Extract multiple goals from list of ProveStatements.

        Args:
            prove_stmts: List of ProveStatement nodes

        Returns:
            List of goal Facts
        """
        goals = []
        for stmt in prove_stmts:
            goal = self.extract_goal(stmt)
            goals.append(goal)
        return goals
