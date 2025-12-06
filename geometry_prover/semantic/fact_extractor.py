"""
FactExtractor - Converts complete AST Program into GeometryModel with Facts.

The FactExtractor processes an entire AST Program, handling all statement types
and populating a GeometryModel with geometric objects, constraints, and proof goals.

From DETAILED_DEVELOPMENT_PLAN.md:
Week 3, Task 3.4 - FactExtractor Implementation
- Process all declaration statement types
- Integrate with ConstraintBuilder and ProveGoalExtractor
- Provide complete AST → GeometryModel pipeline
"""

from typing import Optional
from geometry_prover.dsl.ast_nodes import (
    Program, Statement,
    PointDecl, LineDecl, CircleDecl, TriangleDecl,
    Constraint, ProveStatement
)
from geometry_prover.semantic.geometry_model import GeometryModel
from geometry_prover.semantic.constraint_builder import ConstraintBuilder
from geometry_prover.semantic.prove_goal_extractor import ProveGoalExtractor
from geometry_prover.utils.geometry_objects import LineType


class FactExtractor:
    """
    Extracts facts from AST and populates GeometryModel.

    Processes all statement types:
    - Declarations: PointDecl, LineDecl, CircleDecl, TriangleDecl
    - Constraints: EqualConstraint, ParallelConstraint, etc.
    - Goals: ProveStatement
    """

    def __init__(self, model: Optional[GeometryModel] = None):
        """
        Initialize fact extractor.

        Args:
            model: Optional GeometryModel to use. If None, creates new model.
        """
        self.model = model if model is not None else GeometryModel()
        self.constraint_builder = ConstraintBuilder(self.model)
        self.goal_extractor = ProveGoalExtractor(self.model)

    def extract_from_program(self, program: Program) -> GeometryModel:
        """
        Extract all facts from AST Program.

        Args:
            program: Program AST node

        Returns:
            Populated GeometryModel
        """
        for statement in program.statements:
            self.process_statement(statement)

        return self.model

    def process_statement(self, statement: Statement) -> None:
        """
        Process a single statement.

        Args:
            statement: AST statement node
        """
        # Declaration statements
        if isinstance(statement, PointDecl):
            self.process_point_decl(statement)
        elif isinstance(statement, LineDecl):
            self.process_line_decl(statement)
        elif isinstance(statement, CircleDecl):
            self.process_circle_decl(statement)
        elif isinstance(statement, TriangleDecl):
            self.process_triangle_decl(statement)

        # Constraint statements
        elif isinstance(statement, Constraint):
            self.process_constraint(statement)

        # Prove statement
        elif isinstance(statement, ProveStatement):
            self.process_prove_statement(statement)

        else:
            # Unknown statement type - ignore or log warning
            pass

    def process_point_decl(self, decl: PointDecl) -> None:
        """
        Process point declaration.

        Example: point A, B, C

        Args:
            decl: PointDecl node
        """
        for point_id in decl.points:
            self.model.add_point(point_id.name, declared=True)

    def process_line_decl(self, decl: LineDecl) -> None:
        """
        Process line declaration.

        Example: line AB

        Args:
            decl: LineDecl node
        """
        line_name = decl.name.name

        # Extract points from line name (e.g., "AB" -> "A", "B")
        if len(line_name) >= 2:
            p1_name = line_name[0]
            p2_name = line_name[1]

            # Get or create points
            p1 = self.model.get_or_create_point(p1_name)
            p2 = self.model.get_or_create_point(p2_name)

            # Add line
            self.model.add_line(p1, p2, LineType.LINE, line_name, declared=True)

    def process_circle_decl(self, decl: CircleDecl) -> None:
        """
        Process circle declaration.

        Examples:
            circle O with radius 5
            circle O through A

        Args:
            decl: CircleDecl node
        """
        center_name = decl.center.name
        center = self.model.get_or_create_point(center_name)

        # Determine radius
        if decl.radius is not None:
            # Explicit radius: circle O with radius 5
            radius = decl.radius.value
        elif decl.through_point is not None:
            # Implicit radius from point: circle O through A
            # We'll use a default radius for now, or compute from through_point
            # For simplicity, use a placeholder radius
            # In production, we'd compute the distance from center to through_point
            radius = 1.0  # Placeholder
        else:
            # No radius specified - use default
            radius = 1.0

        self.model.add_circle(center, radius, declared=True)

    def process_triangle_decl(self, decl: TriangleDecl) -> None:
        """
        Process triangle declaration.

        Example: triangle ABC

        Args:
            decl: TriangleDecl node
        """
        triangle_name = decl.name.name

        # Extract vertices from triangle name (e.g., "ABC" -> "A", "B", "C")
        if len(triangle_name) >= 3:
            p1_name = triangle_name[0]
            p2_name = triangle_name[1]
            p3_name = triangle_name[2]

            # Get or create points
            p1 = self.model.get_or_create_point(p1_name)
            p2 = self.model.get_or_create_point(p2_name)
            p3 = self.model.get_or_create_point(p3_name)

            # Add triangle
            self.model.add_triangle(p1, p2, p3)

    def process_constraint(self, constraint: Constraint) -> None:
        """
        Process constraint statement.

        Examples:
            AB = CD
            AB || CD
            angle(ABC) = 90

        Args:
            constraint: Constraint AST node
        """
        # Use ConstraintBuilder to convert constraint to fact
        fact = self.constraint_builder.build_constraint(constraint)

        if fact is not None:
            self.model.add_constraint(fact)

    def process_prove_statement(self, prove_stmt: ProveStatement) -> None:
        """
        Process prove statement.

        Example: prove angle(ABC) = angle(ACB)

        Args:
            prove_stmt: ProveStatement AST node
        """
        # Use ProveGoalExtractor to convert goal to fact
        goal = self.goal_extractor.extract_goal(prove_stmt)
        self.model.add_prove_goal(goal)


def extract_facts(program: Program) -> GeometryModel:
    """
    Convenience function to extract facts from AST program.

    Args:
        program: Program AST node

    Returns:
        Populated GeometryModel
    """
    extractor = FactExtractor()
    return extractor.extract_from_program(program)
