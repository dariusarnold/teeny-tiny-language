from teeny_tiny_language.tokens import Token, TokenType


def test_print_newline_literal(capsys):
    t = Token(TokenType.NEWLINE, "\n")
    print(t)
    out, err = capsys.readouterr()
    assert "\\n" in out


def test_print_eof_zerobyte(capsys):
    t = Token(TokenType.EOF, "")
    print(t)
    out, err = capsys.readouterr()
    assert "" in out
