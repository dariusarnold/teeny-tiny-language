from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.token import TokenType, Token


def test_tokentype_comparison():
    assert TokenType.EOF == TokenType.EOF


def test_tokentype_identity():
    assert TokenType.EOF is TokenType.EOF


def test_empty_current_char():
    l = Lexer("")
    assert l.current_char == "\0"


def test_empty_peek():
    l = Lexer("")
    assert l.peek() == "\0"


def test_peek_not_changing_state():
    l = Lexer("+-*")
    assert l.current_char == "+"
    l.peek()
    assert l.current_char == "+"


def test_single_newline_token():
    l = Lexer("\n")
    assert l.get_token().type == TokenType.NEWLINE


def test_basic_next_char():
    input = "LET foo = 123"
    l = Lexer(input)
    for c in input:
        assert l.current_char == c
        l.next_char()
    assert l.current_char == "\0"


def test_basic_peek():
    input = "LET foo = 123"
    l = Lexer(input)
    for c in input[1:]:
        assert l.peek() == c
        l.next_char()
    assert l.peek() == "\0"


def test_indentation_smoketest():
    input = \
        """\
        WHILE a < 3 REPEAT
            PRINT a
            LET a = a + 1
        ENDWHILE
        """
    l = Lexer(input)
    expected_tokens = [Token(TokenType.WHILE, "WHILE"), Token(TokenType.IDENT, "a"),
                       Token(TokenType.LT, "<"), Token(TokenType.NUMBER, "3"),
                       Token(TokenType.REPEAT, "REPEAT"), Token(TokenType.NEWLINE, "\n"),
                       Token(TokenType.PRINT, "PRINT"), Token(TokenType.IDENT, "a"),
                       Token(TokenType.NEWLINE, "\n"), Token(TokenType.LET, "LET"),
                       Token(TokenType.IDENT, "a"), Token(TokenType.EQ, "="),
                       Token(TokenType.IDENT, "a"), Token(TokenType.PLUS, "+"),
                       Token(TokenType.NUMBER, "1"), Token(TokenType.NEWLINE, "\n"),
                       Token(TokenType.ENDWHILE, "ENDWHILE")]
    for expected_token in expected_tokens:
        assert l.get_token() == expected_token
