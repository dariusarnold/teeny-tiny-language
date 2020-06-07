import pytest

from teeny_tiny_language.lexer import Lexer, LexerError
from teeny_tiny_language.token import Token, TokenType


def test_digit():
    l = Lexer("0")
    assert l.get_token() == Token(TokenType.NUMBER, "0")


def test_digit_following_space_should_ne_be_included():
    l = Lexer("3 a")
    assert l.get_token() == Token(TokenType.NUMBER, "3")
    assert l.get_token() == Token(TokenType.IDENT, "a")


def test_integer():
    l = Lexer("42")
    assert l.get_token() == Token(TokenType.NUMBER, "42")


def test_float():
    l = Lexer("6.92")
    assert l.get_token() == Token(TokenType.NUMBER, "6.92")


def test_missing_leading_digit_aborts():
    l = Lexer(".99")
    with pytest.raises(LexerError):
        l.get_token()


def test_missing_decimal_digit_aborts():
    l = Lexer("1.")
    with pytest.raises(LexerError):
        l.get_token()


def test_float_not_swallowing_following_token():
    l = Lexer("9.8654*")
    assert l.get_token() == Token(TokenType.NUMBER, "9.8654")
    assert l.get_token() == Token(TokenType.ASTERISK, "*")


def test_integer_not_swallowing_following_token():
    l = Lexer("22*")
    assert l.get_token() == Token(TokenType.NUMBER, "22")
    assert l.get_token() == Token(TokenType.ASTERISK, "*")


def test_number_smoketest():
    input = "+-123 9.8654*222/"
    l = Lexer(input)
    expected_tokens = [Token(TokenType.PLUS, "+"), Token(TokenType.MINUS, "-"),
                       Token(TokenType.NUMBER, "123"), Token(TokenType.NUMBER, "9.8654"),
                       Token(TokenType.ASTERISK, "*"), Token(TokenType.NUMBER, "222"),
                       Token(TokenType.SLASH, "/")]
    for expected_token in expected_tokens:
        assert l.get_token() == expected_token
