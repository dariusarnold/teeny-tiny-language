import pytest

from teeny_tiny_language.lexer import Lexer, LexerError
from teeny_tiny_language.token import TokenType, Token

TWO_CHARACTER_TOKENS = [Token(TokenType.EQEQ, "=="),
                        Token(TokenType.NOTEQ, "!="),
                        Token(TokenType.LTEQ, "<="),
                        Token(TokenType.GTEQ, ">=")]


@pytest.mark.parametrize("input_token", TWO_CHARACTER_TOKENS)
def test_two_character_tokens(input_token):
    l = Lexer(input_token.text)
    assert l.get_token() == input_token


def test_invalid_second_token_for_not_equal():
    l = Lexer("!+")
    with pytest.raises(LexerError):
        l.get_token()


def test_basic_parsing():
    input = "+-*/>>==!="
    expected_token_types = [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK,
                            TokenType.SLASH, TokenType.GT, TokenType.GTEQ,
                            TokenType.EQ, TokenType.NOTEQ]
    l = Lexer(input)
    for expected_token_type in expected_token_types:
        token = l.get_token()
        assert token.type == expected_token_type
