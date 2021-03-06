import enum


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:

    def __init__(self, type: TokenType, text: str) -> None:
        self.type: TokenType = type
        self.text: str = text

    def __repr__(self):
        text = repr(self.text)
        return f"Token({self.type.name}, {text})"

    def __eq__(self, other: "Token") -> bool:
        return self.type == other.type and self.text == other.text