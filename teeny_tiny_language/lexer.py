from teeny_tiny_language.token import Token, TokenType


def is_space(char: str) -> bool:
    return char == " " or char == "\t" or char == "\r"


class LexerError(Exception):
    pass


class Lexer:

    def __init__(self, input: str) -> None:
        self.input = input
        self.current_pos: int = 0

    @property
    def current_char(self) -> str:
        if self.current_pos >= len(self.input):
            return "\0"
        return self.input[self.current_pos]

    def next_char(self) -> None:
        self.current_pos += 1

    def skip_whitespace(self) -> None:
        while is_space(self.current_char):
            self.next_char()

    def skip_comment(self) -> None:
        if self.current_char == "#":
            while self.current_char != "\n" and self.current_char != "\0":
                self.next_char()

    def is_valid_string_character(self, char: str) -> bool:
        if char == "\n" or char == "\r" or char == "\t" or char == "\\" or char == "%":
            return False
        return True

    def abort(self, message: str) -> None:
        raise LexerError(f"Lexer error: {message}")

    def get_token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()
        if self.current_char == "+":
            token = Token(TokenType.PLUS, self.current_char)
        elif self.current_char == "-":
            token = Token(TokenType.MINUS, self.current_char)
        elif self.current_char == "*":
            token = Token(TokenType.ASTERISK, self.current_char)
        elif self.current_char == "/":
            token = Token(TokenType.SLASH, self.current_char)
        elif self.current_char == "=":
            # check if = or ==
            if self.peek() == "=":
                token = Token(TokenType.EQEQ, "==")
                self.next_char()
            else:
                token = Token(TokenType.EQ, "=")
        elif self.current_char == "!":
            if self.peek() == "=":
                token = Token(TokenType.NOTEQ, "!=")
                self.next_char()
            else:
                self.abort(f"Got invalid token after ! (Token is {self.peek()})")
        elif self.current_char == ">":
            # check if > or >=
            if self.peek() == "=":
                token = Token(TokenType.GTEQ, ">=")
                self.next_char()
            else:
                token = Token(TokenType.GT, ">")
        elif self.current_char == "<":
            # check if < or <=
            if self.peek() == "=":
                token = Token(TokenType.LTEQ, "<=")
                self.next_char()
            else:
                token = Token(TokenType.LT, "<")
        elif self.current_char == '"':
            # +1 to avoid including the quotation marks
            start_pos = self.current_pos + 1
            self.next_char()
            while self.current_char != '"':
                if not self.is_valid_string_character(self.current_char):
                    self.abort(f"Invalid character {self.current_char} found in string.")
                self.next_char()
            token = Token(TokenType.STRING, self.input[start_pos:self.current_pos])
        elif self.current_char == "\n":
            token = Token(TokenType.NEWLINE, self.current_char)
        elif self.current_char == "\0":
            token = Token(TokenType.EOF, "")

        self.next_char()
        return token

    def peek(self) -> str:
        if self.current_pos < len(self.input) - 1:
            return self.input[self.current_pos + 1]
        return "\0"
