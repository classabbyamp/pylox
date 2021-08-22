from typing import Any

from .grammar.expression import Expr


def interpret(expression: Expr) -> Any:
    return expression.eval()
