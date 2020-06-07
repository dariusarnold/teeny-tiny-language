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

    def match(self, kind: TokenType) -> bool:
        if not self.check_token(kind):
            self.abort(f"Invalid token type {self.current_token.type}, expected {kind}")
        self.next_token()
        return True

    def next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message: str) -> None:
        raise ParserError(f"Parser error: {message}")

    # Production rules

    # program ::= {statement}
    def program(self) -> None:
        print("PROGRAM")
        while not self.check_token(TokenType.EOF):
            self.statement()

    # statement::= "PRINT" (expression | string) newline
    def statement(self) -> None:
        if self.match(TokenType.PRINT):
            print("STATEMENT-PRINT")
            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        self.newline()

    # newline ::= "\n"+
    def newline(self):
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while (self.check_token(TokenType.NEWLINE)):
            self.next_token()
