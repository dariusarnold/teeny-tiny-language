import pytest

from teeny_tiny_language.lexer import Lexer, LexerError


def test_contains_underscore():
    l = Lexer("foo_bar")
    # get first identifier
    l.get_token()
    with pytest.raises(LexerError):
        l.get_token()