from teeny_tiny_language.lexer import Lexer


def test_empty_current_char():
    l = Lexer("")
    assert l.current_char == "\0"


def test_empty_peek():
    l = Lexer("")
    assert l.peek() == "\0"


def test_basic_next_char():
    input = "LET foo = 123"
    l = Lexer(input)
    for c in input:
        assert l.current_char == c
        l.next_char()
    assert l.current_char == "\0"


def test_basic_peek():
    input = "LET foo = 123"
    l = Lexer(input)
    for c in input[1:]:
        assert l.peek() == c
        l.next_char()
    assert l.peek() == "\0"
