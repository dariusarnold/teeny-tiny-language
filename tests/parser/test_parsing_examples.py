import pytest

from teeny_tiny_language.parser import Parser, ParserError


def test_print_hello_world(capsys):
    p = Parser("PRINT \"Hello world\"\n")
    p.program()
    out, err = capsys.readouterr()
    out = out.replace("\n", "")
    assert out == "".join(("PROGRAM", "STATEMENT-PRINT", "NEWLINE"))


def test_print_hello_world_without_newline(capsys):
    p = Parser("PRINT \"Hello world\"")
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


def test_expression(capsys):
    input = "LET foo = foo * 3 + 2\n"
    p = Parser(input)
    p.program()
    out, err = capsys.readouterr()
    out = out.replace("\n", "")
    assert out == "".join(("PROGRAM", "STATEMENT-LET", "EXPRESSION", "TERM", "UNARY",
                           "PRIMARY (foo)", "UNARY", "PRIMARY (3)", "TERM", "UNARY", "PRIMARY (2)",
                           "NEWLINE"))

def test_expression_with_if(capsys):
    input = """\
LET foo = foo * 3 + 2
IF foo > 0 THEN
  PRINT "yes!"
ENDIF
"""
    expected_output = """PROGRAM
STATEMENT-LET
EXPRESSION
TERM
UNARY
PRIMARY (foo)
UNARY
PRIMARY (3)
TERM
UNARY
PRIMARY (2)
NEWLINE
STATEMENT-IF
COMPARISON
EXPRESSION
TERM
UNARY
PRIMARY (foo)
EXPRESSION
TERM
UNARY
PRIMARY (0)
NEWLINE
STATEMENT-PRINT
NEWLINE
NEWLINE
"""
    p = Parser(input)
    p.program()
    out, err = capsys.readouterr()
    assert out == expected_output
