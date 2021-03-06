import pytest

from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.tokens import TokenType, Token

KEYWORD_TOKENS = [t for t in TokenType if 100 < t.value < 200]


@pytest.mark.parametrize("keyword_token", KEYWORD_TOKENS)
def test_single_keyword_lexing(keyword_token: TokenType):
    l = Lexer(keyword_token.name)
    assert l.get_token() == Token(keyword_token, keyword_token.name)


def test_greedy_lexing():
    l = Lexer("IF12THEN")
    assert l.get_token() == Token(TokenType.IDENT, "IF12THEN")


def test_keyword_smoketest():
    input = "IF+-123 foo*THEN/"
    l = Lexer(input)
    expected_tokens = [Token(TokenType.IF, "IF"), Token(TokenType.PLUS, "+"),
                       Token(TokenType.MINUS, "-"), Token(TokenType.NUMBER, "123"),
                       Token(TokenType.IDENT, "foo"), Token(TokenType.ASTERISK, "*"),
                       Token(TokenType.THEN, "THEN"), Token(TokenType.SLASH, "/")]
    for expected_token in expected_tokens:
        assert l.get_token() == expected_token
