from .grammar.statement import Stmt


def interpret(statements: list[Stmt]):
    for stmt in statements:
        stmt.eval()
