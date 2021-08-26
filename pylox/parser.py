from typing import Optional

from .util.exceptions import LoxSyntaxError
from .grammar.expression import Expr, Binary, Unary, Literal, Grouping, Variable, Assign
from .grammar.statement import Stmt, Print, Repr, Block, Expression, Var
from .grammar.token import Token, TokenType
from .grammar.literals import LoxBool, LoxNil


class Parser:
    def __init__(self, tokens: list[Token], repl: bool = False):
        self.tokens = tokens
        self.repl = repl

        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    # !##### STATEMENTS #####!

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()

            return self.statement()
        except LoxSyntaxError as e:
            self.sync()
            raise e

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name.")
        initialiser: Optional[Expr] = None

        if self.match(TokenType.EQUAL):
            initialiser = self.expression()
        if (self.repl and self.peek().type != TokenType.EOF) or not self.repl:
            self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return Var(name, initialiser)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.REPR):
            return self.repr_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expression_statement()

    def block(self) -> list[Stmt]:
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def print_statement(self) -> Print:
        value = self.expression()
        if (self.repl and self.peek().type != TokenType.EOF) or not self.repl:
            self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def repr_statement(self) -> Repr:
        value = self.expression()
        if (self.repl and self.peek().type != TokenType.EOF) or not self.repl:
            self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Repr(value)

    def expression_statement(self) -> Expression:
        expr = self.expression()
        if (self.repl and self.peek().type != TokenType.EOF) or not self.repl:
            self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Expression(expr)

    # !##### EXPRESSIONS #####!

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            raise LoxSyntaxError(equals, "Invalid assignment target.")
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(LoxBool(False))
        if self.match(TokenType.TRUE):
            return Literal(LoxBool(True))
        if self.match(TokenType.NIL):
            return Literal(LoxNil())
        if self.match(TokenType.NUMBER, TokenType.NAN, TokenType.INFINITY, TokenType.STRING):
            if (lit := self.previous().literal) is not None:
                return Literal(lit)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)

        raise LoxSyntaxError(self.peek(), "Expected expression.")

    # !##### UTILITY #####!

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type_: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type_: TokenType, message: str) -> Token:
        if self.check(type_):
            return self.advance()
        raise LoxSyntaxError(self.peek(), message)

    def sync(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            pk_type = self.peek()
            if pk_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()
