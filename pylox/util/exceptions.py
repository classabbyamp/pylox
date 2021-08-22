from ..grammar.token import Token, TokenType


class LoxException(Exception):
    """Exception for internal Lox errors."""
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def __str__(self) -> str:
        return f"[line {self.line}] Error: {self.message}"


class LoxParseError(LoxException):
    def __init__(self, line: int, message: str):
        super().__init__(line, message)

    def __str__(self) -> str:
        return f"[line {self.line}] ParseError: {self.message}"


class LoxSyntaxError(LoxException):
    """Exception for Lox syntax errors."""
    def __init__(self, token: Token, message: str):
        self.line = token.line
        self.where = "'" + token.lexeme + "'" if token.type != TokenType.EOF else "end"
        self.message = message

    def __str__(self) -> str:
        return f"[line {self.line}] SyntaxError at {self.where}: {self.message}"


class LoxRuntimeError(LoxException):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def __str__(self) -> str:
        return f"[line {self.token.line}] RuntimeError at '{self.token.lexeme}': {self.message}"
