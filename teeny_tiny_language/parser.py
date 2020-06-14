from typing import Iterable

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

        self.symbols = set()
        self.labels_declared = set()
        self.labels_gotoed = set()

        self.current_token: Token = self.lexer.get_token()
        self.peek_token: Token = self.lexer.get_token()

    def check_token(self, kind: TokenType) -> bool:
        return self.current_token.type == kind

    def check_peek(self, kind: TokenType) -> bool:
        return self.peek_token.type == kind

    def match(self, kind: TokenType) -> None:
        if not self.check_token(kind):
            self.abort(f"Invalid token type {self.current_token.type}, expected {kind}")
        yield from self.next_token()

    def next_token(self) -> Token:
        old_token = self.current_token
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()
        yield old_token

    def abort(self, message: str) -> None:
        raise ParserError(f"Parser error: {message}")

    def make_gen(self):
        return self.program()

    # Production rules

    # program ::= {statement}
    def program(self) -> Iterable[Token]:
        while not self.check_token(TokenType.EOF):
            yield from self.statement()
        yield Token(TokenType.EOF, "")

    # statement::= "PRINT" (expression | string) newline
    def statement(self) -> None:
        if self.check_token(TokenType.PRINT):
            yield from self.next_token()
            if self.check_token(TokenType.STRING):
                yield from self.next_token()
            else:
                yield from self.expression()
        elif self.check_token(TokenType.IF):
            yield from self.next_token()
            yield from self.comparison()
            yield from self.match(TokenType.THEN)
            yield from self.newline()
            while not self.check_token(TokenType.ENDIF):
                yield from self.statement()
            yield from self.match(TokenType.ENDIF)
        elif self.check_token(TokenType.WHILE):
            yield from self.next_token()
            yield from self.comparison()
            yield from self.match(TokenType.REPEAT)
            while not self.check_token(TokenType.ENDWHILE):
                yield from self.statement()
            yield from self.match(TokenType.ENDWHILE)
        elif self.check_token(TokenType.LABEL):
            yield from self.next_token()
            self.labels_declared.add(self.current_token.text)
            yield from self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            yield from self.next_token()
            if self.current_token.text in self.labels_declared:
                self.labels_gotoed.add(self.current_token.text)
            else:
                self.abort(f"Cannot GOTO undeclared label {self.current_token.text}.")
            yield from self.match(TokenType.IDENT)
        elif self.check_token(TokenType.LET):
            yield from self.next_token()
            # Store Identifier token and add it so seen symbols after the expression call, so a
            # statement like LET a = a is invalid, because the right a will only be known in the
            # symbol table after the whole statement is parsed.
            identifier = self.current_token
            yield from self.match(TokenType.IDENT)
            yield from self.match(TokenType.EQ)
            yield from self.expression()
            self.symbols.add(identifier.text)
        elif self.check_token(TokenType.INPUT):
            yield from self.next_token()
            yield from self.match(TokenType.IDENT)
        elif self.check_token(TokenType.NEWLINE):
            # empty lines are allowed, but dont need to be transpiled
            pass
        else:
            self.abort(
                f"Invalid statement at {self.current_token.text}: {self.current_token.type.name}")
        yield from self.newline()

    # comparison ::= expression("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self) -> None:
        yield from self.expression()
        if is_comparison_operator(self.current_token):
            yield from self.next_token()
            yield from self.expression()
        else:
            self.abort(f"Expected comparison operator instead of {self.current_token}")
        while is_comparison_operator(self.current_token):
            yield from self.next_token()
            yield from self.expression()

    # expression ::= term {("-" | "+") term}
    def expression(self) -> None:
        yield from self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            yield from self.next_token()
            yield from self.term()

    # term ::= unary {( "/" | "*" ) unary }
    def term(self) -> None:
        yield from self.unary()
        if self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            yield from self.next_token()
            yield from self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self) -> None:
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            yield from self.next_token()
        yield from self.primary()

    # primary ::= number | ident
    def primary(self) -> None:
        if self.check_token(TokenType.NUMBER):
            yield from self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.current_token.text not in self.symbols:
                self.abort(f"Undeclared symbol {self.current_token.text}")
            yield from self.next_token()
        else:
            self.abort(f"Unexpected token {self.current_token.type.name}")

    # newline ::= "\n"+
    def newline(self) -> None:
        yield from self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            # dont yield to swallow following newlines
            next(self.next_token())
