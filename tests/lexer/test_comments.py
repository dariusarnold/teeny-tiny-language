from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.token import TokenType


def test_comment_character():
    l = Lexer("#")
    assert l.get_token().type == TokenType.EOF


def test_only_comment():
    l = Lexer("# comment let a = 1")
    assert l.get_token().type == TokenType.EOF


def test_two_comment_lines():
    l = Lexer("# comment let a = 1\n #hello")
    assert l.get_token().type == TokenType.NEWLINE
    assert l.get_token().type == TokenType.EOF


def test_comment_in_code():
    input = "+- # This is a comment!\n */"
    l = Lexer(input)
    expected_token_types = [TokenType.PLUS, TokenType.MINUS, TokenType.NEWLINE,
                            TokenType.ASTERISK, TokenType.SLASH]
    for expected_token_type in expected_token_types:
        assert l.get_token().type == expected_token_type
