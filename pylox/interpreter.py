from .env import Env
from .grammar.statement import Stmt


class Interpreter:
    def __init__(self) -> None:
        self.env = Env(repl=True)

    def interpret(self, statements: list[Stmt]):
        for stmt in statements:
            stmt.eval(self.env)
