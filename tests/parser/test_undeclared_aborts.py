import pytest

from teeny_tiny_language.parser import ParserError, Parser
import tests.test_helpers as test_helpers


def test_undeclared_symbol_print():
    p = Parser("PRINT foo")
    with pytest.raises(ParserError) as e:
        test_helpers.exhaust(p.program())
    test_helpers.assert_in_error_msg("foo", e)


def test_undeclared_symbol_in_let():
    p = Parser("LET foo = foo")
    with pytest.raises(ParserError) as e:
        test_helpers.exhaust(p.program())
    test_helpers.assert_in_error_msg("foo", e)
