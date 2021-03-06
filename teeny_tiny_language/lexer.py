from typing import Optional, List

from teeny_tiny_language.tokens import Token, TokenType


def is_space(char: str) -> bool:
    return char == " " or char == "\t" or char == "\r"


class LexerError(Exception):
    pass


VALID_KEYWORDS: List[TokenType] = [t for t in TokenType if 100 < t.value < 200]


class Lexer:

    def __init__(self, input: str) -> None:
        # add trailing newline to simplify special cases in parsing
        self.input = f"{input}"
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

    def is_keyword(self, text: str) -> Optional[TokenType]:
        for keyword in VALID_KEYWORDS:
            if text == keyword.name:
                return keyword
        return None

    def abort(self, message: str) -> None:
        raise LexerError(f"Lexer error: {message}")

    def get_token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()
        token = None
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
                self.abort(
                    f"Got invalid token after ! (Token is {self.peek()})")
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
                    self.abort(
                        f"Invalid character {self.current_char} found in string.")
                self.next_char()
            token = Token(TokenType.STRING,
                          self.input[start_pos:self.current_pos])
        elif self.current_char.isdigit():
            start_pos = self.current_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == ".":
                self.next_char()
                if not self.peek().isdigit():
                    self.abort(f"Got invalid character after . ({self.peek()})")
                self.next_char()
                while self.peek().isdigit():
                    self.next_char()
                # since we only peeked at the next digit to not consume a token following after the
                # last digit of the number, we have to +1 here to include last digit
                token = Token(TokenType.NUMBER, self.input[start_pos:self.current_pos + 1])
            else:
                token = Token(TokenType.NUMBER,
                              self.input[start_pos:self.current_pos + 1])
        elif self.current_char == ".":
            self.abort("Missing leading digit for number")
        elif self.current_char.isalpha():
            start_pos = self.current_pos
            while self.peek().isalnum():
                self.next_char()
            token_text = self.input[start_pos:self.current_pos + 1]
            keyword = self.is_keyword(token_text)
            if keyword:
                token = Token(keyword, token_text)
            else:
                token = Token(TokenType.IDENT, token_text)
        elif self.current_char == "\n":
            token = Token(TokenType.NEWLINE, self.current_char)
        elif self.current_char == "\0":
            token = Token(TokenType.EOF, "")

        if token is None:
            self.abort(f"Lexing error: Unknown token {self.current_char}")

        self.next_char()
        return token

    def peek(self) -> str:
        if self.current_pos < len(self.input) - 1:
            return self.input[self.current_pos + 1]
        return "\0"
