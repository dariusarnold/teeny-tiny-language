from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.token import TokenType, Token


class ParserError(Exception):
    pass


class Parser:

    def __init__(self, input: str):
        self.lexer = Lexer(input)

        self.current_token: Token = self.lexer.get_token()
        self.peek_token: Token = self.lexer.get_token()

    def check_token(self, kind: TokenType) -> bool:
        return self.current_token.type == kind

    def check_peek(self, kind: TokenType) -> bool:
        return self.peek_token.type == kind

    def match(self, kind: TokenType) -> None:
        if not self.check_token(kind):
            self.abort(f"Invalid token type {self.current_token.type}, expected {kind}")
        self.next_token()

    def next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message: str) -> None:
        raise ParserError(f"Parser error: {message}")