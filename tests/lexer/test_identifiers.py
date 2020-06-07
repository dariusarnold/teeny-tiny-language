from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.tokens import Token, TokenType


def test_single_identifier_alpha_only():
    l = Lexer("foo1")
    assert l.get_token() == Token(TokenType.IDENT, "foo1")


def test_single_identifier_alphanum():
    l = Lexer("foo1")
    assert l.get_token() == Token(TokenType.IDENT, "foo1")
