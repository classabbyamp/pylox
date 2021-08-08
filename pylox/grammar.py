from dataclasses import dataclass, fields
from typing import Any

from .token import Token
from .dot import escape, token_to_dot


class Expr:
    def dot(self, root: bool = True) -> list[str]:
        output = []
        if root:
            output.append(f"n{id(self):x} [ label = <{escape(type(self).__name__)}> ];")
        for field in fields(self):
            val = getattr(self, field.name)
            if isinstance(val, Expr):
                output.append(f"n{id(val):x} [ label = <{escape(type(val).__name__)}> ];")
                output += val.dot()
            elif isinstance(val, Token):
                output.append(token_to_dot(val))
            else:
                output.append(f"n{id(val):x} [ label = <{escape(str(val)) if val is not None else 'nil'}> ];")
            output.append(f"n{id(self):x} -> n{id(val):x}")
        return output


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: Any


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
