"""
Tests for DSL Lexer.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 2, Task 2.2 - Test Requirements:
- Test tokenization of all valid constructs
- Test error handling for invalid input
- Test line/column tracking for error messages
"""

import pytest
from geometry_prover.dsl.lexer import Lexer, Token, TokenType
from geometry_prover.utils import DSLParseError


class TestLexerBasics:
    """Test basic lexer functionality."""

    def test_empty_input(self):
        """Test lexing empty string."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_whitespace_only(self):
        """Test lexing whitespace."""
        lexer = Lexer("   \t  ")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_comments(self):
        """Test comment handling."""
        lexer = Lexer("# This is a comment\n")
        tokens = lexer.tokenize()
        assert len(tokens) == 1  # Only EOF
        assert tokens[0].type == TokenType.EOF


class TestLexerKeywords:
    """Test keyword tokenization."""

    def test_point_keyword(self):
        """Test 'point' keyword."""
        lexer = Lexer("point")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == "point"

    def test_all_keywords(self):
        """Test all DSL keywords."""
        keywords = [
            ("point", TokenType.POINT),
            ("line", TokenType.LINE),
            ("circle", TokenType.CIRCLE),
            ("triangle", TokenType.TRIANGLE),
            ("on", TokenType.ON),
            ("with", TokenType.WITH),
            ("center", TokenType.CENTER),
            ("radius", TokenType.RADIUS),
            ("through", TokenType.THROUGH),
            ("angle", TokenType.ANGLE),
            ("prove", TokenType.PROVE),
            ("perp", TokenType.PERPENDICULAR),
        ]

        for keyword, expected_type in keywords:
            lexer = Lexer(keyword)
            tokens = lexer.tokenize()
            assert tokens[0].type == expected_type
            assert tokens[0].value == keyword

    def test_keyword_case_insensitive(self):
        """Test that keywords are case-insensitive."""
        for text in ["point", "Point", "POINT", "PoInT"]:
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType.POINT


class TestLexerIdentifiers:
    """Test identifier tokenization."""

    def test_single_letter_identifier(self):
        """Test single letter identifiers."""
        for letter in "ABCPQXYZ":
            lexer = Lexer(letter)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType.IDENTIFIER
            assert tokens[0].value == letter

    def test_multi_char_identifier(self):
        """Test multi-character identifiers."""
        identifiers = ["point1", "P1", "center_O", "line_AB", "x_coord"]
        for ident in identifiers:
            lexer = Lexer(ident)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType.IDENTIFIER
            assert tokens[0].value == ident

    def test_identifier_vs_keyword(self):
        """Test distinguishing identifiers from keywords."""
        lexer = Lexer("point P1")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.POINT  # keyword
        assert tokens[1].type == TokenType.IDENTIFIER  # identifier


class TestLexerNumbers:
    """Test number tokenization."""

    def test_integer(self):
        """Test integer numbers."""
        for num in ["0", "1", "42", "100", "999"]:
            lexer = Lexer(num)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType.NUMBER
            assert tokens[0].value == num

    def test_float(self):
        """Test floating point numbers."""
        for num in ["3.14", "0.5", "99.99", "1.0"]:
            lexer = Lexer(num)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType.NUMBER
            assert tokens[0].value == num

    def test_number_in_expression(self):
        """Test numbers in expressions."""
        lexer = Lexer("radius 5")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.RADIUS
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == "5"


class TestLexerOperators:
    """Test operator tokenization."""

    def test_equals(self):
        """Test equals operator."""
        lexer = Lexer("=")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.EQUALS
        assert tokens[0].value == "="

    def test_parallel_double_pipe(self):
        """Test parallel operator ||."""
        lexer = Lexer("||")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PARALLEL
        assert tokens[0].value == "||"

    def test_parallel_double_slash(self):
        """Test parallel operator //."""
        lexer = Lexer("//")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PARALLEL
        assert tokens[0].value == "//"

    def test_perpendicular_unicode(self):
        """Test perpendicular operator ⊥."""
        lexer = Lexer("⊥")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PERPENDICULAR
        assert tokens[0].value == "⊥"

    def test_perpendicular_keyword(self):
        """Test perpendicular keyword."""
        lexer = Lexer("perp")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PERPENDICULAR

    def test_angle_unicode(self):
        """Test angle symbol ∠."""
        lexer = Lexer("∠")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.ANGLE
        assert tokens[0].value == "∠"


class TestLexerDelimiters:
    """Test delimiter tokenization."""

    def test_comma(self):
        """Test comma."""
        lexer = Lexer(",")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.COMMA

    def test_parentheses(self):
        """Test parentheses."""
        lexer = Lexer("()")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.RPAREN

    def test_identifier_list(self):
        """Test comma-separated identifiers."""
        lexer = Lexer("A, B, C")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "A"
        assert tokens[1].type == TokenType.COMMA
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "B"
        assert tokens[3].type == TokenType.COMMA
        assert tokens[4].type == TokenType.IDENTIFIER
        assert tokens[4].value == "C"


class TestLexerCompleteStatements:
    """Test lexing complete DSL statements."""

    def test_point_declaration(self):
        """Test point declaration statement."""
        lexer = Lexer("point A, B, C")
        tokens = lexer.tokenize()

        expected = [
            TokenType.POINT,
            TokenType.IDENTIFIER,
            TokenType.COMMA,
            TokenType.IDENTIFIER,
            TokenType.COMMA,
            TokenType.IDENTIFIER,
            TokenType.EOF
        ]

        assert [t.type for t in tokens] == expected

    def test_line_declaration(self):
        """Test line declaration."""
        lexer = Lexer("line AB")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.LINE
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "AB"

    def test_circle_declaration(self):
        """Test circle declaration."""
        lexer = Lexer("circle O with radius 5")
        tokens = lexer.tokenize()

        expected = [
            TokenType.CIRCLE,
            TokenType.IDENTIFIER,
            TokenType.WITH,
            TokenType.RADIUS,
            TokenType.NUMBER,
            TokenType.EOF
        ]

        assert [t.type for t in tokens] == expected

    def test_triangle_declaration(self):
        """Test triangle declaration."""
        lexer = Lexer("triangle ABC")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.TRIANGLE
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "ABC"

    def test_constraint_equality(self):
        """Test equality constraint."""
        lexer = Lexer("AB = CD")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[1].type == TokenType.EQUALS
        assert tokens[2].type == TokenType.IDENTIFIER

    def test_constraint_parallel(self):
        """Test parallel constraint."""
        lexer = Lexer("AB || CD")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[1].type == TokenType.PARALLEL
        assert tokens[2].type == TokenType.IDENTIFIER

    def test_prove_statement(self):
        """Test prove statement."""
        lexer = Lexer("prove AB = CD")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.PROVE
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[2].type == TokenType.EQUALS
        assert tokens[3].type == TokenType.IDENTIFIER

    def test_angle_expression(self):
        """Test angle expression."""
        lexer = Lexer("angle(ABC) = angle(DEF)")
        tokens = lexer.tokenize()

        expected = [
            TokenType.ANGLE,
            TokenType.LPAREN,
            TokenType.IDENTIFIER,
            TokenType.RPAREN,
            TokenType.EQUALS,
            TokenType.ANGLE,
            TokenType.LPAREN,
            TokenType.IDENTIFIER,
            TokenType.RPAREN,
            TokenType.EOF
        ]

        assert [t.type for t in tokens] == expected


class TestLexerLineColumnTracking:
    """Test line and column number tracking."""

    def test_single_line_positions(self):
        """Test column tracking on single line."""
        lexer = Lexer("point A, B")
        tokens = lexer.tokenize()

        assert tokens[0].line == 1
        assert tokens[0].column == 1  # "point"

        assert tokens[1].line == 1
        assert tokens[1].column == 7  # "A"

        assert tokens[2].line == 1
        assert tokens[2].column == 8  # ","

    def test_multiline_positions(self):
        """Test line tracking across multiple lines."""
        lexer = Lexer("point A\nline AB\n")
        tokens = lexer.tokenize()

        assert tokens[0].line == 1  # "point"
        assert tokens[1].line == 1  # "A"
        assert tokens[2].line == 2  # "line"
        assert tokens[3].line == 2  # "AB"


class TestLexerErrors:
    """Test error handling."""

    def test_invalid_character(self):
        """Test error on invalid character."""
        lexer = Lexer("point @")
        with pytest.raises(DSLParseError) as exc_info:
            lexer.tokenize()
        assert "Unexpected character '@'" in str(exc_info.value)

    def test_single_pipe(self):
        """Test error on single pipe."""
        lexer = Lexer("AB | CD")
        with pytest.raises(DSLParseError) as exc_info:
            lexer.tokenize()
        assert "expected '||'" in str(exc_info.value)

    def test_single_slash(self):
        """Test error on single slash."""
        lexer = Lexer("AB / CD")
        with pytest.raises(DSLParseError) as exc_info:
            lexer.tokenize()
        assert "expected '//'" in str(exc_info.value)

    def test_error_includes_position(self):
        """Test that errors include line/column."""
        lexer = Lexer("point A\nline @")
        with pytest.raises(DSLParseError) as exc_info:
            lexer.tokenize()
        error = exc_info.value
        assert error.line == 2
        assert error.column is not None


class TestLexerCompletePrograms:
    """Test lexing complete DSL programs."""

    def test_isosceles_triangle_program(self):
        """Test lexing isosceles triangle example."""
        program = """
        point A, B, C
        triangle ABC
        AB = AC
        prove angle(ABC) = angle(ACB)
        """
        lexer = Lexer(program)
        tokens = lexer.tokenize()

        # Should tokenize without errors
        assert tokens[-1].type == TokenType.EOF
        assert len(tokens) > 10  # Multiple statements

    def test_program_with_comments(self):
        """Test program with comments."""
        program = """
        # Declare points
        point A, B, C
        # Create triangle
        triangle ABC
        """
        lexer = Lexer(program)
        tokens = lexer.tokenize()

        # Comments should be skipped
        token_types = [t.type for t in tokens]
        assert TokenType.COMMENT not in token_types


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
