"""
AST (Abstract Syntax Tree) Node Definitions for Geometry DSL.

Defines the node types that represent the parsed structure of DSL programs.
Uses the visitor pattern for traversal and processing.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass


class ASTNode(ABC):
    """
    Base class for all AST nodes.

    Supports the visitor pattern for tree traversal and processing.
    """

    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """
        Accept a visitor for processing this node.

        Args:
            visitor: The visitor to accept

        Returns:
            Result from visitor processing
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """String representation for debugging."""
        pass


class Program(ASTNode):
    """
    Root node representing a complete DSL program.

    Attributes:
        statements: List of top-level statements
    """

    def __init__(self, statements: List['Statement']):
        self.statements = statements

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)

    def __repr__(self) -> str:
        stmts = '\n  '.join(repr(s) for s in self.statements)
        return f"Program(\n  {stmts}\n)"


# Statement nodes

class Statement(ASTNode):
    """Base class for all statements."""
    pass


class PointDecl(Statement):
    """
    Point declaration statement.

    Example: point A, B, C

    Attributes:
        points: List of point identifiers
    """

    def __init__(self, points: List['Identifier']):
        self.points = points

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_point_decl(self)

    def __repr__(self) -> str:
        points_str = ', '.join(repr(p) for p in self.points)
        return f"PointDecl([{points_str}])"


class LineDecl(Statement):
    """
    Line declaration statement.

    Example: line AB

    Attributes:
        name: Identifier for the line (e.g., "AB")
    """

    def __init__(self, name: 'Identifier'):
        self.name = name

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_line_decl(self)

    def __repr__(self) -> str:
        return f"LineDecl({repr(self.name)})"


class CircleDecl(Statement):
    """
    Circle declaration statement.

    Examples:
        circle O with radius 5
        circle O through A

    Attributes:
        center: Center point identifier
        radius: Optional radius value (Number)
        through_point: Optional point the circle passes through
    """

    def __init__(
        self,
        center: 'Identifier',
        radius: Optional['Number'] = None,
        through_point: Optional['Identifier'] = None
    ):
        self.center = center
        self.radius = radius
        self.through_point = through_point

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_circle_decl(self)

    def __repr__(self) -> str:
        if self.radius:
            return f"CircleDecl({repr(self.center)}, radius={repr(self.radius)})"
        elif self.through_point:
            return f"CircleDecl({repr(self.center)}, through={repr(self.through_point)})"
        return f"CircleDecl({repr(self.center)})"


class TriangleDecl(Statement):
    """
    Triangle declaration statement.

    Example: triangle ABC

    Attributes:
        name: Identifier for the triangle (e.g., "ABC")
    """

    def __init__(self, name: 'Identifier'):
        self.name = name

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_triangle_decl(self)

    def __repr__(self) -> str:
        return f"TriangleDecl({repr(self.name)})"


# Constraint nodes

class Constraint(Statement):
    """Base class for all constraint statements."""
    pass


class EqualConstraint(Constraint):
    """
    Equality constraint between two expressions.

    Examples:
        AB = CD
        angle(ABC) = 90
        angle(ABC) = angle(DEF)

    Attributes:
        left: Left expression
        right: Right expression
    """

    def __init__(self, left: 'Expression', right: 'Expression'):
        self.left = left
        self.right = right

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_equal_constraint(self)

    def __repr__(self) -> str:
        return f"EqualConstraint({repr(self.left)} = {repr(self.right)})"


class ParallelConstraint(Constraint):
    """
    Parallel constraint between two line segments.

    Example: AB || CD

    Attributes:
        segment1: First segment
        segment2: Second segment
    """

    def __init__(self, segment1: 'SegmentExpr', segment2: 'SegmentExpr'):
        self.segment1 = segment1
        self.segment2 = segment2

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_parallel_constraint(self)

    def __repr__(self) -> str:
        return f"ParallelConstraint({repr(self.segment1)} || {repr(self.segment2)})"


class PerpendicularConstraint(Constraint):
    """
    Perpendicular constraint between two line segments.

    Example: AB ⊥ CD

    Attributes:
        segment1: First segment
        segment2: Second segment
    """

    def __init__(self, segment1: 'SegmentExpr', segment2: 'SegmentExpr'):
        self.segment1 = segment1
        self.segment2 = segment2

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_perpendicular_constraint(self)

    def __repr__(self) -> str:
        return f"PerpendicularConstraint({repr(self.segment1)} ⊥ {repr(self.segment2)})"


class OnConstraint(Constraint):
    """
    Point-on-object constraint.

    Examples:
        P on AB
        P on circle O

    Attributes:
        point: Point identifier
        object: Object identifier (line, circle, etc.)
    """

    def __init__(self, point: 'Identifier', object: 'Identifier'):
        self.point = point
        self.object = object

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_on_constraint(self)

    def __repr__(self) -> str:
        return f"OnConstraint({repr(self.point)} on {repr(self.object)})"


class ProveStatement(Statement):
    """
    Prove goal statement.

    Example: prove angle(ABC) = angle(ACB)

    Attributes:
        goal: The constraint to prove
    """

    def __init__(self, goal: Constraint):
        self.goal = goal

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_prove_statement(self)

    def __repr__(self) -> str:
        return f"ProveStatement({repr(self.goal)})"


# Expression nodes

class Expression(ASTNode):
    """Base class for all expressions."""
    pass


class Identifier(Expression):
    """
    Identifier expression.

    Represents point names, line names, etc.

    Attributes:
        name: The identifier string
    """

    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)

    def __repr__(self) -> str:
        return f"Identifier('{self.name}')"

    def __eq__(self, other) -> bool:
        return isinstance(other, Identifier) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Number(Expression):
    """
    Numeric literal expression.

    Attributes:
        value: The numeric value as float
    """

    def __init__(self, value: float):
        self.value = value

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_number(self)

    def __repr__(self) -> str:
        return f"Number({self.value})"


class SegmentExpr(Expression):
    """
    Line segment expression.

    Example: AB (segment from point A to point B)

    Attributes:
        identifier: The segment identifier (e.g., "AB")
    """

    def __init__(self, identifier: Identifier):
        self.identifier = identifier

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_segment_expr(self)

    def __repr__(self) -> str:
        return f"SegmentExpr({repr(self.identifier)})"


class AngleExpr(Expression):
    """
    Angle expression.

    Examples:
        angle(ABC)  - angle at vertex B
        ∠ABC       - using Unicode symbol

    Attributes:
        identifier: The angle identifier (e.g., "ABC")
    """

    def __init__(self, identifier: Identifier):
        self.identifier = identifier

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_angle_expr(self)

    def __repr__(self) -> str:
        return f"AngleExpr({repr(self.identifier)})"


# Visitor interface

class ASTVisitor(ABC):
    """
    Abstract visitor interface for traversing AST.

    Subclass this to implement specific processing of the AST.
    """

    @abstractmethod
    def visit_program(self, node: Program) -> Any:
        pass

    @abstractmethod
    def visit_point_decl(self, node: PointDecl) -> Any:
        pass

    @abstractmethod
    def visit_line_decl(self, node: LineDecl) -> Any:
        pass

    @abstractmethod
    def visit_circle_decl(self, node: CircleDecl) -> Any:
        pass

    @abstractmethod
    def visit_triangle_decl(self, node: TriangleDecl) -> Any:
        pass

    @abstractmethod
    def visit_equal_constraint(self, node: EqualConstraint) -> Any:
        pass

    @abstractmethod
    def visit_parallel_constraint(self, node: ParallelConstraint) -> Any:
        pass

    @abstractmethod
    def visit_perpendicular_constraint(self, node: PerpendicularConstraint) -> Any:
        pass

    @abstractmethod
    def visit_on_constraint(self, node: OnConstraint) -> Any:
        pass

    @abstractmethod
    def visit_prove_statement(self, node: ProveStatement) -> Any:
        pass

    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass

    @abstractmethod
    def visit_number(self, node: Number) -> Any:
        pass

    @abstractmethod
    def visit_segment_expr(self, node: SegmentExpr) -> Any:
        pass

    @abstractmethod
    def visit_angle_expr(self, node: AngleExpr) -> Any:
        pass


# Utility: Simple string visitor for debugging

class ASTStringVisitor(ASTVisitor):
    """
    Visitor that generates a readable string representation of the AST.
    Useful for debugging and testing.
    """

    def __init__(self):
        self.indent = 0

    def _indent_str(self) -> str:
        return "  " * self.indent

    def visit_program(self, node: Program) -> str:
        lines = ["Program:"]
        self.indent += 1
        for stmt in node.statements:
            lines.append(self._indent_str() + stmt.accept(self))
        self.indent -= 1
        return "\n".join(lines)

    def visit_point_decl(self, node: PointDecl) -> str:
        points = ", ".join(p.accept(self) for p in node.points)
        return f"PointDecl: {points}"

    def visit_line_decl(self, node: LineDecl) -> str:
        return f"LineDecl: {node.name.accept(self)}"

    def visit_circle_decl(self, node: CircleDecl) -> str:
        center = node.center.accept(self)
        if node.radius:
            return f"CircleDecl: center={center}, radius={node.radius.accept(self)}"
        elif node.through_point:
            return f"CircleDecl: center={center}, through={node.through_point.accept(self)}"
        return f"CircleDecl: center={center}"

    def visit_triangle_decl(self, node: TriangleDecl) -> str:
        return f"TriangleDecl: {node.name.accept(self)}"

    def visit_equal_constraint(self, node: EqualConstraint) -> str:
        left = node.left.accept(self)
        right = node.right.accept(self)
        return f"Equal: {left} = {right}"

    def visit_parallel_constraint(self, node: ParallelConstraint) -> str:
        seg1 = node.segment1.accept(self)
        seg2 = node.segment2.accept(self)
        return f"Parallel: {seg1} || {seg2}"

    def visit_perpendicular_constraint(self, node: PerpendicularConstraint) -> str:
        seg1 = node.segment1.accept(self)
        seg2 = node.segment2.accept(self)
        return f"Perpendicular: {seg1} ⊥ {seg2}"

    def visit_on_constraint(self, node: OnConstraint) -> str:
        point = node.point.accept(self)
        obj = node.object.accept(self)
        return f"On: {point} on {obj}"

    def visit_prove_statement(self, node: ProveStatement) -> str:
        goal = node.goal.accept(self)
        return f"Prove: {goal}"

    def visit_identifier(self, node: Identifier) -> str:
        return node.name

    def visit_number(self, node: Number) -> str:
        return str(node.value)

    def visit_segment_expr(self, node: SegmentExpr) -> str:
        return f"Segment({node.identifier.accept(self)})"

    def visit_angle_expr(self, node: AngleExpr) -> str:
        return f"Angle({node.identifier.accept(self)})"
