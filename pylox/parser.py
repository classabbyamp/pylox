from typing import Optional

from .util.exceptions import LoxSyntaxError
from .grammar.expression import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical
from .grammar.statement import Stmt, Print, Repr, Block, Expression, Var, If, While
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
        if self.match(TokenType.FOR):
            return self.for_statement()
        elif self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.REPR):
            return self.repr_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())

        return self.expression_statement()

    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'for'.")

        if self.match(TokenType.SEMICOLON):
            initialiser = None
        elif self.match(TokenType.VAR):
            initialiser = self.var_declaration()
        else:
            initialiser = self.expression_statement()

        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        else:
            condition = Literal(LoxBool(True))
        self.consume(TokenType.SEMICOLON, "Expected ';' after for loop condition.")

        if not self.check(TokenType.RIGHT_PAREN):
            increment: Optional[Expr] = self.expression()
        else:
            increment = None

        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after for loop declaration.")

        body = self.statement()

        # if there is an increment, do the increment at the end of the loop body
        if increment is not None:
            body = Block([body, Expression(increment)])

        # create the loop
        body = While(condition, body)

        # if the loop variable needs init, do it before the loop
        if initialiser is not None:
            body = Block([initialiser, body])

        return body

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition.")
        body = self.statement()

        return While(condition, body)

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition.")

        then_branch = self.statement()
        else_branch = self.statement() if self.match(TokenType.ELSE) else None

        return If(condition, then_branch, else_branch)

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
        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            raise LoxSyntaxError(equals, "Invalid assignment target.")
        return expr

    def or_expr(self) -> Expr:
        expr = self.and_expr()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Logical(expr, operator, right)

        return expr

    def and_expr(self) -> Expr:
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

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

        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
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
