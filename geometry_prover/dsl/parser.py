"""
Parser for Geometry DSL.

Implements a recursive descent parser that converts a stream of tokens
from the lexer into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from geometry_prover.dsl.lexer import Token, TokenType, Lexer
from geometry_prover.dsl.ast_nodes import (
    Program, Statement, Expression,
    PointDecl, LineDecl, CircleDecl, TriangleDecl,
    EqualConstraint, ParallelConstraint, PerpendicularConstraint, OnConstraint,
    ProveStatement,
    Identifier, Number, SegmentExpr, AngleExpr
)
from geometry_prover.utils import DSLParseError


class Parser:
    """
    Recursive descent parser for the Geometry DSL.

    Converts a stream of tokens into an Abstract Syntax Tree (AST).
    """

    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with token stream.

        Args:
            tokens: List of tokens from lexer
        """
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def error(self, message: str) -> DSLParseError:
        """
        Create a parser error with current token position.

        Args:
            message: Error message

        Returns:
            DSLParseError with position information
        """
        if self.current_token:
            return DSLParseError(
                message,
                self.current_token.line,
                self.current_token.column
            )
        return DSLParseError(message, 0, 0)

    def peek(self, offset: int = 0) -> Optional[Token]:
        """
        Peek at token without consuming it.

        Args:
            offset: Offset from current position

        Returns:
            Token at position, or None if out of bounds
        """
        pos = self.pos + offset
        if 0 <= pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def advance(self) -> Token:
        """
        Consume and return current token.

        Returns:
            Current token before advancing
        """
        token = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return token

    def expect(self, token_type: TokenType) -> Token:
        """
        Consume token of expected type or raise error.

        Args:
            token_type: Expected token type

        Returns:
            Consumed token

        Raises:
            DSLParseError: If current token is not of expected type
        """
        if self.current_token.type != token_type:
            raise self.error(
                f"Expected {token_type.name}, got {self.current_token.type.name}"
            )
        return self.advance()

    def match(self, *token_types: TokenType) -> bool:
        """
        Check if current token matches any of the given types.

        Args:
            token_types: Token types to check

        Returns:
            True if current token matches any type
        """
        if self.current_token is None:
            return False
        return self.current_token.type in token_types

    # Grammar productions

    def parse(self) -> Program:
        """
        Parse the entire program.

        Grammar:
            <program> ::= <statement_list>

        Returns:
            Program AST node
        """
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                # Handle compound statements (e.g., "point X on Y" returns Program)
                from geometry_prover.dsl.ast_nodes import Program as ProgramNode
                if isinstance(stmt, ProgramNode):
                    # Flatten nested program statements
                    statements.extend(stmt.statements)
                else:
                    statements.append(stmt)
        return Program(statements)

    def parse_statement(self) -> Optional[Statement]:
        """
        Parse a single statement.

        Grammar:
            <statement> ::= <point_decl>
                          | <line_decl>
                          | <circle_decl>
                          | <triangle_decl>
                          | <constraint>
                          | <prove_statement>

        Returns:
            Statement AST node, or None if no valid statement
        """
        if self.match(TokenType.POINT):
            return self.parse_point_decl()
        elif self.match(TokenType.LINE):
            return self.parse_line_decl()
        elif self.match(TokenType.CIRCLE):
            return self.parse_circle_decl()
        elif self.match(TokenType.TRIANGLE):
            return self.parse_triangle_decl()
        elif self.match(TokenType.PROVE):
            return self.parse_prove_statement()
        elif self.match(TokenType.IDENTIFIER, TokenType.ANGLE):
            # Could be a constraint starting with identifier or angle
            return self.parse_constraint()
        else:
            raise self.error(
                f"Unexpected token {self.current_token.type.name}, "
                f"expected statement keyword"
            )

    def parse_point_decl(self) -> Statement:
        """
        Parse point declaration, possibly with "on" clause.

        Grammar:
            <point_decl> ::= "point" <identifier_list>
                          | "point" <identifier> "on" <identifier>
                          | "point" <identifier> "on" "circle" <identifier>

        Returns:
            PointDecl AST node or Program with PointDecl + OnConstraint
        """
        self.expect(TokenType.POINT)

        # Check if this is "point X on ..." syntax (single point with on clause)
        if self.match(TokenType.IDENTIFIER) and self.peek(1) and self.peek(1).type == TokenType.ON:
            point_id = self.parse_identifier()
            self.expect(TokenType.ON)

            # Check for "on circle O" vs "on AB"
            if self.match(TokenType.CIRCLE):
                self.advance()  # consume "circle"
                circle_id = self.parse_identifier()
                # Return a Program with two statements: point decl + on constraint
                from geometry_prover.dsl.ast_nodes import Program
                return Program([
                    PointDecl([point_id]),
                    OnConstraint(point_id, Identifier(f"circle_{circle_id.name}"))
                ])
            else:
                # Regular "on line/segment"
                obj_id = self.parse_identifier()
                # Return a Program with two statements
                from geometry_prover.dsl.ast_nodes import Program
                return Program([
                    PointDecl([point_id]),
                    OnConstraint(point_id, obj_id)
                ])
        else:
            # Regular point declaration: "point A, B, C"
            identifiers = self.parse_identifier_list()
            return PointDecl(identifiers)

    def parse_identifier_list(self) -> List[Identifier]:
        """
        Parse comma-separated list of identifiers.

        Grammar:
            <identifier_list> ::= <identifier>
                                | <identifier> "," <identifier_list>

        Returns:
            List of Identifier nodes
        """
        identifiers = []
        identifiers.append(self.parse_identifier())

        while self.match(TokenType.COMMA):
            self.advance()  # consume comma
            identifiers.append(self.parse_identifier())

        return identifiers

    def parse_line_decl(self) -> LineDecl:
        """
        Parse line declaration.

        Grammar:
            <line_decl> ::= "line" <identifier>

        Returns:
            LineDecl AST node
        """
        self.expect(TokenType.LINE)
        name = self.parse_identifier()
        return LineDecl(name)

    def parse_circle_decl(self) -> CircleDecl:
        """
        Parse circle declaration.

        Grammar:
            <circle_decl> ::= "circle" <identifier> "with" "radius" <number>
                            | "circle" <identifier> "through" <identifier>

        Returns:
            CircleDecl AST node
        """
        self.expect(TokenType.CIRCLE)
        center = self.parse_identifier()

        if self.match(TokenType.WITH):
            self.advance()  # consume 'with'
            self.expect(TokenType.RADIUS)
            radius = self.parse_number()
            return CircleDecl(center, radius=radius)
        elif self.match(TokenType.THROUGH):
            self.advance()  # consume 'through'
            through_point = self.parse_identifier()
            return CircleDecl(center, through_point=through_point)
        else:
            # Simple circle declaration (just center)
            return CircleDecl(center)

    def parse_triangle_decl(self) -> TriangleDecl:
        """
        Parse triangle declaration.

        Grammar:
            <triangle_decl> ::= "triangle" <identifier>

        Returns:
            TriangleDecl AST node
        """
        self.expect(TokenType.TRIANGLE)
        name = self.parse_identifier()
        return TriangleDecl(name)

    def parse_constraint(self) -> Statement:
        """
        Parse constraint statement.

        Grammar:
            <constraint> ::= <segment> "=" <segment>
                          | <segment> "||" <segment>
                          | <segment> "⊥" <segment>
                          | <angle> "=" <angle>
                          | <angle> "=" <number>
                          | <identifier> "on" <identifier>
                          | <identifier> "on" "circle" <identifier>

        Returns:
            Constraint AST node
        """
        # Look ahead to determine constraint type
        if self.peek(1) and self.peek(1).type == TokenType.ON:
            # Point on object: P on AB or P on circle O
            point = self.parse_identifier()
            self.expect(TokenType.ON)

            # Check for "on circle O"
            if self.match(TokenType.CIRCLE):
                self.advance()  # consume "circle"
                circle_id = self.parse_identifier()
                # Use special identifier format to indicate circle
                return OnConstraint(point, Identifier(f"circle_{circle_id.name}"))
            else:
                # Regular "on line/segment"
                obj = self.parse_identifier()
                return OnConstraint(point, obj)

        # Parse left expression (could be segment, angle, or identifier)
        left_expr = self.parse_expression()

        # Check operator
        if self.match(TokenType.EQUALS):
            self.advance()
            right_expr = self.parse_expression()
            return EqualConstraint(left_expr, right_expr)
        elif self.match(TokenType.PARALLEL):
            self.advance()
            # Both sides must be segments
            if not isinstance(left_expr, SegmentExpr):
                left_expr = SegmentExpr(left_expr if isinstance(left_expr, Identifier) else Identifier(str(left_expr)))
            right_expr = self.parse_segment_expr()
            return ParallelConstraint(left_expr, right_expr)
        elif self.match(TokenType.PERPENDICULAR):
            self.advance()
            # Both sides must be segments
            if not isinstance(left_expr, SegmentExpr):
                left_expr = SegmentExpr(left_expr if isinstance(left_expr, Identifier) else Identifier(str(left_expr)))
            right_expr = self.parse_segment_expr()
            return PerpendicularConstraint(left_expr, right_expr)
        else:
            raise self.error(
                f"Expected constraint operator (=, ||, ⊥), got {self.current_token.type.name}"
            )

    def parse_prove_statement(self) -> ProveStatement:
        """
        Parse prove statement.

        Grammar:
            <prove_statement> ::= "prove" <constraint>

        Returns:
            ProveStatement AST node
        """
        self.expect(TokenType.PROVE)
        goal = self.parse_constraint()
        return ProveStatement(goal)

    def parse_expression(self) -> Expression:
        """
        Parse an expression (segment, angle, number, or identifier).

        Returns:
            Expression AST node
        """
        if self.match(TokenType.ANGLE):
            return self.parse_angle_expr()
        elif self.match(TokenType.NUMBER):
            return self.parse_number()
        elif self.match(TokenType.IDENTIFIER):
            # Could be a segment or just an identifier
            return self.parse_segment_expr()
        else:
            raise self.error(
                f"Expected expression, got {self.current_token.type.name}"
            )

    def parse_segment_expr(self) -> SegmentExpr:
        """
        Parse segment expression.

        Grammar:
            <segment> ::= <identifier>

        Returns:
            SegmentExpr AST node
        """
        identifier = self.parse_identifier()
        return SegmentExpr(identifier)

    def parse_angle_expr(self) -> AngleExpr:
        """
        Parse angle expression.

        Grammar:
            <angle> ::= "angle" "(" <identifier> ")"
                      | "∠" <identifier>

        Returns:
            AngleExpr AST node
        """
        if self.match(TokenType.ANGLE):
            self.advance()  # consume 'angle' or '∠'

            # Check for function call syntax: angle(ABC)
            if self.match(TokenType.LPAREN):
                self.advance()  # consume '('
                identifier = self.parse_identifier()
                self.expect(TokenType.RPAREN)
                return AngleExpr(identifier)
            else:
                # Direct usage: angle ABC (less common)
                identifier = self.parse_identifier()
                return AngleExpr(identifier)
        else:
            raise self.error(f"Expected angle, got {self.current_token.type.name}")

    def parse_identifier(self) -> Identifier:
        """
        Parse identifier.

        Returns:
            Identifier AST node
        """
        token = self.expect(TokenType.IDENTIFIER)
        return Identifier(token.value)

    def parse_number(self) -> Number:
        """
        Parse number literal.

        Returns:
            Number AST node
        """
        token = self.expect(TokenType.NUMBER)
        return Number(float(token.value))


def parse_program(text: str) -> Program:
    """
    Convenience function to parse DSL program from text.

    Args:
        text: DSL source code

    Returns:
        Program AST node

    Raises:
        DSLParseError: If parsing fails
    """
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
