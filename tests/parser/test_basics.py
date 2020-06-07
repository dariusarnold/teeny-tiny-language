import pytest

from teeny_tiny_language.parser import Parser, ParserError
from teeny_tiny_language.token import TokenType, Token


def test_empty_input_eof():
    p = Parser("")
    assert p.check_token(TokenType.EOF)
    assert p.check_peek(TokenType.EOF)


def test_next_token():
    p = Parser("LET a = 1")
    token1: Token = p.peek_token
    p.next_token()
    assert p.check_token(token1.type)


def test_match_advances_parser():
    p = Parser("\n")
    assert p.check_token(TokenType.NEWLINE)
    p.match(TokenType.NEWLINE)
    assert p.check_token(TokenType.EOF)


def test_match_aborting():
    p = Parser("\n")
    with pytest.raises(ParserError):
        p.match(TokenType.EOF)


def test_match_success():
    p = Parser("LET a = 1")
    assert p.match(TokenType.LET)


def test_check_token_success():
    p = Parser("LET")
    assert p.check_token(TokenType.LET)


def test_check_token_fail():
    p = Parser("LET")
    assert not p.check_token(TokenType.IDENT)


def test_peek_token_success():
    p = Parser("LET a = 1")
    assert p.check_peek(TokenType.IDENT)


def test_peek_token_fail():
    p = Parser("LET a = 1")
    assert not p.check_peek(TokenType.LT)