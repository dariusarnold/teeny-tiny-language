import pytest

from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.token import TokenType, Token

SINGLE_CHARACTER_TOKENS = [Token(TokenType.EQ, "="), Token(TokenType.PLUS, "+"),
                           Token(TokenType.MINUS, "-"),
                           Token(TokenType.ASTERISK, "*"),
                           Token(TokenType.SLASH, "/"),
                           Token(TokenType.NEWLINE, "\n")]


@pytest.mark.parametrize("input_token",
                         SINGLE_CHARACTER_TOKENS)
def test_single_character_token(input_token):
    l = Lexer(input_token.text)
    assert l.get_token() == input_token


def test_single_character_tokens_type():
    input = "+-*/\n"
    expected_token_types = [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK,
                            TokenType.SLASH, TokenType.NEWLINE]
    lexer = Lexer(input)
    for expected_token_type in expected_token_types:
        token = lexer.get_token()
        assert token.type == expected_token_type
    assert lexer.get_token().type == TokenType.EOF


def test_single_character_tokens_type_with_space():
    input = "+- *  /\n"
    expected_token_types = [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK,
                            TokenType.SLASH, TokenType.NEWLINE]
    lexer = Lexer(input)
    for expected_token_type in expected_token_types:
        token = lexer.get_token()
        assert token.type == expected_token_type
    assert lexer.get_token().type == TokenType.EOF


def test_single_character_tokens_text():
    input = "+-*/\n"
    expected_token_texts = ["+", "-", "*", "/", "\n"]
    lexer = Lexer(input)
    for expected_token_text in expected_token_texts:
        token = lexer.get_token()
        assert token.text == expected_token_text
    assert lexer.get_token().text == ""


def test_single_character_tokens_text_with_space():
    input = "+- *  /\n"
    expected_token_texts = ["+", "-", "*", "/", "\n"]
    lexer = Lexer(input)
    for expected_token_text in expected_token_texts:
        token = lexer.get_token()
        assert token.text == expected_token_text
    assert lexer.get_token().text == ""
