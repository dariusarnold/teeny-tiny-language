import pytest

from teeny_tiny_language.parser import Parser, ParserError


def test_print_hello_world(capsys):
    p = Parser("PRINT \"Hello world\"\n")
    p.program()
    out, err = capsys.readouterr()
    out = out.replace("\n", "")
    assert out == "".join(("PROGRAM", "STATEMENT-PRINT", "NEWLINE"))


def test_multiple_print_statements(capsys):
    input = """\
PRINT "hello, world!"
PRINT "second line"
PRINT "and a third..."
"""
    p = Parser(input)
    p.program()
    out, err = capsys.readouterr()
    out = out.replace("\n", "")
    assert out == "".join(("PROGRAM", "STATEMENT-PRINT", "NEWLINE", "STATEMENT-PRINT", "NEWLINE",
                           "STATEMENT-PRINT", "NEWLINE"))


def test_loop(capsys):
    input = """\
LABEL loop
PRINT "hello, world!"
GOTO loop
"""
    p = Parser(input)
    p.program()
    out, err = capsys.readouterr()
    out = out.replace("\n", "")
    assert out == "".join(("PROGRAM", "STATEMENT-LABEL", "NEWLINE", "STATEMENT-PRINT", "NEWLINE",
                           "STATEMENT-GOTO", "NEWLINE"))


def test_break(capsys):
    input = "JUMP GOTO\n"
    p = Parser(input)
    with pytest.raises(ParserError):
        p.program()

