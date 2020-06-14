import pytest

from teeny_tiny_language.parser import Parser, ParserError
from teeny_tiny_language.tokens import TokenType, Token
from tests import test_helpers


def test_empty_input_eof():
    p = Parser("")
    tokens = [t for t in p.program()]
    assert tokens == [Token(TokenType.EOF, "")]


@pytest.mark.timeout(1)
def test_swallow_consecutive_newlines():
    # This had a bug after converting the code to use yield, where it would hang, the timeout
    # catches that.
    p = Parser("\n\n")
    tokens = [t.type for t in p.program()]
    assert tokens == [TokenType.NEWLINE, TokenType.EOF]


def test_warn_on_missing_final_newline():
    p = Parser("PRINT \"test\"")
    with pytest.raises(ParserError) as e:
        test_helpers.exhaust(p.program())
    test_helpers.assert_in_error_msg("NEWLINE", e)


def test_next_token():
    p = Parser("LET a = 1")
    token1: Token = p.peek_token
    next(p.next_token())
    assert p.check_token(token1.type)


def test_match_advances_parser():
    p = Parser("\n")
    assert p.check_token(TokenType.NEWLINE)
    next(p.match(TokenType.NEWLINE))
    assert p.check_token(TokenType.EOF)


def test_match_aborting():
    p = Parser("\n")
    with pytest.raises(ParserError):
        next(p.match(TokenType.EOF))


def test_match_success():
    p = Parser("LET a = 1")
    assert next(p.match(TokenType.LET))


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