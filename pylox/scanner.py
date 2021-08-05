from typing import Any

from . import lox
from .token import Token, TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def scan_token(self) -> Token:
        c = self.advance()

        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in (" ", "\r", "\t"):
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if isdigit(c):
                self.number()
            elif isalpha(c):
                self.identifier()
            else:
                raise lox.LoxException(self.line, "Unexepected character.")

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self, n: int = 1) -> str:
        # self.current has already been incremented, but it's handy for n to default to 1
        n -= 1
        if n <= 0:
            n = 0

        if self.is_at_end() or self.current + n >= len(self.source):
            return ""
        return self.source[self.current + n]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise lox.LoxException(self.line, "Unterminated string.")

        self.advance()
        self.add_token(TokenType.STRING, self.source[self.start+1:self.current-1])

    def number(self):
        while isdigit(self.peek()):
            self.advance()
        if self.peek() == "." and isdigit(self.peek(2)):
            self.advance()
            while isdigit(self.peek()):
                self.advance()
        try:
            self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
        except ValueError:
            raise lox.LoxException(self.line, "Unable to parse number.")

    def identifier(self):
        while isalnum(self.peek()):
            self.advance()

        self.add_token(self.keywords.get(self.source[self.start:self.current], TokenType.IDENTIFIER))

    def add_token(self, type_: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, self.line, literal))


def isdigit(c: str) -> bool:
    if len(c) <= 1:
        return "0" <= c <= "9"
    else:
        return isdigit(c[0]) and isdigit(c[1:])


def isalpha(c: str) -> bool:
    if len(c) <= 1:
        return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"
    else:
        return isalpha(c[0]) and isalpha(c[1:])


def isalnum(c: str) -> bool:
    return isalpha(c) or isdigit(c)
