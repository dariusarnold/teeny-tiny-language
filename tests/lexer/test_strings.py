import pytest

from teeny_tiny_language.lexer import Lexer, LexerError
from teeny_tiny_language.token import Token, TokenType


def test_single_string():
    l = Lexer("\"I am a string\"")
    assert l.get_token() == Token(TokenType.STRING, "I am a string")


INVALID_STRING_CHARACTERS = ["\n", "\t", "\\", "%", "\r"]


@pytest.mark.parametrize("input_string", INVALID_STRING_CHARACTERS)
def test_abort_on_invalid_string_character(input_string):
    l = Lexer(f"\"{input_string}\"")
    with pytest.raises(LexerError):
        l.get_token()


def test_string_smoketest():
    input = "+- /\"I am a string != 4 \"*"
    expected_tokens = [Token(TokenType.PLUS, "+"), Token(TokenType.MINUS, "-"),
                       Token(TokenType.SLASH, "/"),
                       Token(TokenType.STRING, "I am a string != 4 "),
                       Token(TokenType.ASTERISK, "*")]
    l = Lexer(input)
    for expected_token in expected_tokens:
        assert l.get_token() == expected_token
