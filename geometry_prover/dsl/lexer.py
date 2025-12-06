"""
Lexer for Geometry DSL.

The lexer converts input text into a stream of tokens for the parser.
Supports all keywords, operators, and constructs defined in the grammar.
"""

from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass


class TokenType(Enum):
    """Types of tokens in the geometry DSL."""

    # Keywords - Basic
    POINT = auto()
    LINE = auto()
    CIRCLE = auto()
    TRIANGLE = auto()
    ON = auto()
    WITH = auto()
    CENTER = auto()
    RADIUS = auto()
    THROUGH = auto()
    ANGLE = auto()
    PROVE = auto()

    # Keywords - Quadrilaterals (NEW)
    RECTANGLE = auto()
    SQUARE = auto()
    PARALLELOGRAM = auto()
    RHOMBUS = auto()
    TRAPEZOID = auto()
    QUADRILATERAL = auto()

    # Keywords - Coordinate Geometry (NEW)
    ORIGIN = auto()
    SLOPE = auto()
    FUNCTION = auto()
    DISTANCE = auto()

    # Operators
    EQUALS = auto()         # =
    PARALLEL = auto()       # || or //
    PERPENDICULAR = auto()  # ⊥ or perp
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    CARET = auto()          # ^

    # Delimiters
    COMMA = auto()          # ,
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    COLON = auto()          # :
    VBAR = auto()           # |
    DEGREE = auto()         # °

    # Literals
    IDENTIFIER = auto()     # A, B, point_1, etc.
    NUMBER = auto()         # 123, 3.14

    # Special
    NEWLINE = auto()
    EOF = auto()            # End of file
    COMMENT = auto()        # # comment


@dataclass
class Token:
    """
    Represents a single token from the lexer.

    Attributes:
        type: The type of token
        value: The string value of the token
        line: Line number (1-indexed)
        column: Column number (1-indexed)
    """

    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class Lexer:
    """
    Lexical analyzer for the Geometry DSL.

    Converts input text into a stream of tokens.
    Tracks line and column numbers for error reporting.
    """

    # Keyword mapping
    KEYWORDS = {
        # Basic keywords
        'point': TokenType.POINT,
        'line': TokenType.LINE,
        'circle': TokenType.CIRCLE,
        'triangle': TokenType.TRIANGLE,
        'on': TokenType.ON,
        'with': TokenType.WITH,
        'center': TokenType.CENTER,
        'radius': TokenType.RADIUS,
        'through': TokenType.THROUGH,
        'angle': TokenType.ANGLE,
        'prove': TokenType.PROVE,
        'perp': TokenType.PERPENDICULAR,

        # Quadrilateral keywords (NEW)
        'rectangle': TokenType.RECTANGLE,
        'square': TokenType.SQUARE,
        'parallelogram': TokenType.PARALLELOGRAM,
        'rhombus': TokenType.RHOMBUS,
        'trapezoid': TokenType.TRAPEZOID,
        'quadrilateral': TokenType.QUADRILATERAL,

        # Coordinate geometry keywords (NEW)
        'origin': TokenType.ORIGIN,
        'slope': TokenType.SLOPE,
        'function': TokenType.FUNCTION,
        'distance': TokenType.DISTANCE,
    }

    def __init__(self, text: str):
        """
        Initialize lexer with input text.

        Args:
            text: The DSL source code to tokenize
        """
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def error(self, message: str) -> Exception:
        """Create a lexer error with current position."""
        from geometry_prover.utils import DSLParseError
        return DSLParseError(message, self.line, self.column)

    def peek(self, offset: int = 0) -> Optional[str]:
        """
        Peek at character without consuming it.

        Args:
            offset: Offset from current position

        Returns:
            Character at position, or None if at end
        """
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None

    def advance(self) -> Optional[str]:
        """
        Consume and return current character.

        Returns:
            Current character, or None if at end
        """
        if self.pos >= len(self.text):
            return None

        char = self.text[self.pos]
        self.pos += 1

        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def skip_whitespace(self) -> None:
        """Skip whitespace characters (spaces and tabs, but not newlines)."""
        while self.peek() in (' ', '\t'):
            self.advance()

    def skip_comment(self) -> None:
        """Skip comment from # to end of line."""
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()

    def read_number(self) -> Token:
        """
        Read a number token (integer or float).

        Returns:
            Token with type NUMBER
        """
        start_line = self.line
        start_column = self.column
        num_str = ''

        # Read integer part
        while self.peek() and self.peek().isdigit():
            num_str += self.advance()

        # Check for decimal point
        if self.peek() == '.' and self.peek(1) and self.peek(1).isdigit():
            num_str += self.advance()  # Add '.'
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()

        return Token(TokenType.NUMBER, num_str, start_line, start_column)

    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword.

        Returns:
            Token with type IDENTIFIER or keyword type
        """
        start_line = self.line
        start_column = self.column
        ident = ''

        # Read alphanumeric characters and underscores
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()

        # Check if it's a keyword
        token_type = self.KEYWORDS.get(ident.lower(), TokenType.IDENTIFIER)

        return Token(token_type, ident, start_line, start_column)

    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire input text.

        Returns:
            List of tokens

        Raises:
            DSLParseError: If invalid characters or malformed tokens encountered
        """
        self.tokens = []

        while self.pos < len(self.text):
            self.skip_whitespace()

            if self.pos >= len(self.text):
                break

            char = self.peek()
            start_line = self.line
            start_column = self.column

            # Comments
            if char == '#':
                self.skip_comment()
                continue

            # Newlines (significant in some contexts)
            elif char == '\n':
                self.advance()
                # Skip multiple newlines
                continue

            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())

            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())

            # Operators and delimiters
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '=', start_line, start_column))

            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))

            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))

            elif char == '-':
                self.advance()
                # Check if it's a negative number
                if self.peek() and self.peek().isdigit():
                    # It's a negative number
                    num_token = self.read_number()
                    num_token.value = '-' + num_token.value
                    self.tokens.append(num_token)
                else:
                    # It's a minus operator
                    self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))

            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.STAR, '*', start_line, start_column))

            elif char == '^':
                self.advance()
                self.tokens.append(Token(TokenType.CARET, '^', start_line, start_column))

            elif char == '°':
                self.advance()
                self.tokens.append(Token(TokenType.DEGREE, '°', start_line, start_column))

            elif char == '|':
                self.advance()
                if self.peek() == '|':
                    # It's parallel operator ||
                    self.advance()
                    self.tokens.append(Token(TokenType.PARALLEL, '||', start_line, start_column))
                else:
                    # It's vertical bar (for distance notation)
                    self.tokens.append(Token(TokenType.VBAR, '|', start_line, start_column))

            elif char == '/':
                self.advance()
                if self.peek() == '/':
                    self.advance()
                    self.tokens.append(Token(TokenType.PARALLEL, '//', start_line, start_column))
                else:
                    raise self.error(f"Unexpected character '/', expected '//'")

            elif char == '⊥':
                self.advance()
                self.tokens.append(Token(TokenType.PERPENDICULAR, '⊥', start_line, start_column))

            elif char == '∠':
                self.advance()
                self.tokens.append(Token(TokenType.ANGLE, '∠', start_line, start_column))

            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))

            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))

            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))

            else:
                raise self.error(f"Unexpected character '{char}'")

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))

        return self.tokens

    def __repr__(self) -> str:
        return f"Lexer(pos={self.pos}, line={self.line}, column={self.column})"
