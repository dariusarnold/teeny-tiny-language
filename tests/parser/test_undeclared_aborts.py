import pytest

from teeny_tiny_language.parser import ParserError, Parser


def assert_in_error_msg(text: str, e):
    assert text in e.value.args[0]


def test_undeclared_symbol_print():
    p = Parser("PRINT foo")
    with pytest.raises(ParserError) as e:
        p.program()
    assert_in_error_msg("foo", e)


def test_undeclared_symbol_in_let():
    p = Parser("LET foo = foo")
    with pytest.raises(ParserError) as e:
        p.program()
    assert_in_error_msg("foo", e)
