from teeny_tiny_language.lexer import Lexer
from teeny_tiny_language.tokens import TokenType, Token


class ParserError(Exception):
    pass


def is_comparison_operator(token: Token) -> bool:
    return token.type in (TokenType.EQEQ, TokenType.NOTEQ, TokenType.GT, TokenType.GTEQ,
                          TokenType.LT, TokenType.LTEQ)


class Parser:

    def __init__(self, input: str, verbose: bool = True):
        self.lexer = Lexer(input)
        self.verbose = verbose

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
        if self.check_token(TokenType.PRINT):
            self.next_token()
            print("STATEMENT-PRINT")
            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        elif self.check_token(TokenType.IF):
            print("STATEMENT-PRINT")
            self.next_token()
            self.comparison()
            self.match(TokenType.THEN)
            self.newline()
            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()
            self.match(TokenType.REPEAT)
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.match(TokenType.IDENT)

        self.newline()

    # comparison ::= expression("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self) -> None:
        print("COMPARISON")
        self.expression()
        if is_comparison_operator(self.current_token):
            self.next_token()
            self.expression()
        while is_comparison_operator(self.current_token):
            self.next_token()
            self.expression()

    # expression ::= term {("-" | "+") term}
    def expression(self) -> None:
        print("EXPRESSION")
        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    # term ::= unary {( "/" | "*" ) unary }
    def term(self) -> None:
        print("TERM")
        self.unary()
        if self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.next_token()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self) -> None:
        print("UNARY")
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    # primary ::= number | ident
    def primary(self) -> None:
        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            self.next_token()
        else:
            self.abort(f"Unexpected token {self.current_token.text}")

    # newline ::= "\n"+
    def newline(self) -> None:
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while (self.check_token(TokenType.NEWLINE)):
            self.next_token()
