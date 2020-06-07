from teeny_tiny_language.token import Token, TokenType

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

    def get_token(self) -> Token:
        if self.current_char == "+":
            token = Token(TokenType.PLUS, self.current_char)
        elif self.current_char == "-":
            token = Token(TokenType.MINUS, self.current_char)
        elif self.current_char == "*":
            token = Token(TokenType.ASTERISK, self.current_char)
        elif self.current_char == "/":
            token = Token(TokenType.SLASH, self.current_char)
        elif self.current_char == "\n":
            pass
        elif self.current_char == "\0":
            token = Token(TokenType.EOF, "")
        self.next_char()
        return token
