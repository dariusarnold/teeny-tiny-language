import pytest

from teeny_tiny_language.parser import Parser, ParserError


def test_print_undefined_variable():
    p = Parser("PRINT index")
    with pytest.raises(ParserError):
        p.program()


def test_goto_undeclared_label():
    p = Parser("GOTO main")
    with pytest.raises(ParserError) as e:
        p.program()
    # check if label name in undeclared label
    assert "main" in e.value.args[0]


def test_nonsensical_comparison_operator():
    p = Parser("IF 1 + 1 THEN\nENDIF")
    with pytest.raises(ParserError):
        p.program()