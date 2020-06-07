from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.token import TokenType


def test_single_character_tokens_type():
    input = "+-*/"
    expected_token_types = [TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK, TokenType.SLASH]
    lexer = Lexer(input)
    for expected_token_type in expected_token_types:
        token = lexer.get_token()
        assert token.type == expected_token_type
    assert lexer.get_token().type == TokenType.EOF


def test_single_character_tokens_type_with_space():
    input = "+- *  /"
    expected_token_types = [TokenType.PLUS, TokenType.MINUS,
                            TokenType.ASTERISK,
                            TokenType.SLASH]
    lexer = Lexer(input)
    for expected_token_type in expected_token_types:
        token = lexer.get_token()
        assert token.type == expected_token_type
    assert lexer.get_token().type == TokenType.EOF


def test_single_character_tokens_text():
    input = "+-*/"
    expected_token_texts = ["+", "-", "*", "/"]
    lexer = Lexer(input)
    for expected_token_text in expected_token_texts:
        token = lexer.get_token()
        assert token.text == expected_token_text
    assert lexer.get_token().text == ""


def test_single_character_tokens_text_with_space():
    input = "+- *  /"
    expected_token_texts = ["+", "-", "*", "/"]
    lexer = Lexer(input)
    for expected_token_text in expected_token_texts:
        token = lexer.get_token()
        assert token.text == expected_token_text
    assert lexer.get_token().text == ""
