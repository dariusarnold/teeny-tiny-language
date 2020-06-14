import pytest

from teeny_tiny_language.parser import Parser, ParserError
from teeny_tiny_language.tokens import Token, TokenType
from tests import test_helpers


def test_yielding():
    p = Parser("LET a = 1\n")
    expected_tokens = [Token(TokenType.LET, "LET"), Token(TokenType.IDENT, "a"),
                       Token(TokenType.EQ, "="), Token(TokenType.NUMBER, "1")]
    for actual_token, expected_token in zip(p.program(), expected_tokens):
        assert actual_token == expected_token


def test_print_hello_world():
    p = Parser("PRINT \"Hello world\"\n")
    tokens = [t for t in p.program()]
    assert tokens == [Token(TokenType.PRINT, "PRINT"), Token(TokenType.STRING, "Hello world"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.EOF, "")]


def test_multiple_print_statements():
    input = """\
PRINT "hello, world!"
PRINT "second line"
PRINT "and a third..."
"""
    p = Parser(input)
    tokens = [t for t in p.program()]
    print(Token(TokenType.NEWLINE, "\n"))
    assert tokens == [Token(TokenType.PRINT, "PRINT"), Token(TokenType.STRING, "hello, world!"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.PRINT, "PRINT"),
                      Token(TokenType.STRING, "second line"), Token(TokenType.NEWLINE, "\n"),
                      Token(TokenType.PRINT, "PRINT"), Token(TokenType.STRING, "and a third..."),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.EOF, "")]


def test_loop():
    input = """\
LABEL loop
PRINT "hello, world!"
GOTO loop
"""
    p = Parser(input)
    tokens = [t for t in p.program()]
    assert tokens == [Token(TokenType.LABEL, "LABEL"), Token(TokenType.IDENT, "loop"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.PRINT, "PRINT"),
                      Token(TokenType.STRING, "hello, world!"), Token(TokenType.NEWLINE, "\n"),
                      Token(TokenType.GOTO, "GOTO"), Token(TokenType.IDENT, "loop"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.EOF, "")]


def test_break():
    input = "JUMP GOTO\n"
    p = Parser(input)
    with pytest.raises(ParserError):
        test_helpers.exhaust(p.program())


def test_expression():
    input = "LET foo = 0\nLET foo = foo * 3 + 2\n"
    p = Parser(input)
    tokens = [t for t in p.program()]
    assert tokens == [Token(TokenType.LET, "LET"), Token(TokenType.IDENT, "foo"),
                      Token(TokenType.EQ, "="), Token(TokenType.NUMBER, "0"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.LET, "LET"),
                      Token(TokenType.IDENT, "foo"), Token(TokenType.EQ, "="),
                      Token(TokenType.IDENT, "foo"), Token(TokenType.ASTERISK, "*"),
                      Token(TokenType.NUMBER, "3"), Token(TokenType.PLUS, "+"),
                      Token(TokenType.NUMBER, "2"), Token(TokenType.NEWLINE, "\n"),
                      Token(TokenType.EOF, "")]


def test_expression_with_if():
    input = """\
LET foo = 1
IF foo > 0 THEN
  PRINT "yes!"
ENDIF
"""
    p = Parser(input)
    tokens = [t for t in p.program()]
    assert tokens == [Token(TokenType.LET, "LET"), Token(TokenType.IDENT, "foo"),
                      Token(TokenType.EQ, "="), Token(TokenType.NUMBER, "1"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.IF, "IF"),
                      Token(TokenType.IDENT, "foo"), Token(TokenType.GT, ">"),
                      Token(TokenType.NUMBER, "0"), Token(TokenType.THEN, "THEN"),
                      Token(TokenType.NEWLINE, "\n"), Token(TokenType.PRINT, "PRINT"),
                      Token(TokenType.STRING, "yes!"), Token(TokenType.NEWLINE, "\n"),
                      Token(TokenType.ENDIF, "ENDIF"), Token(TokenType.NEWLINE, "\n"),
                      Token(TokenType.EOF, "")]
