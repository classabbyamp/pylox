from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from math import nan
from typing import Any, Union

from .dot import escape, token_to_dot
from .token import Token, TokenType
from .exceptions import LoxRuntimeError
from .interpreter import is_truthy, is_equal, check_num_operand


class Expr(ABC):
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

    @abstractmethod
    def eval(self):
        pass


def interpret(expression: Expr) -> Any:
    return expression.eval()


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def eval(self) -> Union[float, str, bool, None]:
        left = self.left.eval()
        right = self.right.eval()

        if self.operator.type is TokenType.MINUS:
            check_num_operand(self.operator, left, right)
            return left - right
        elif self.operator.type is TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            else:
                raise LoxRuntimeError(self.operator, "operands must be both numbers or both strings")
        elif self.operator.type is TokenType.SLASH:
            check_num_operand(self.operator, left, right)
            try:
                return left / right
            except ZeroDivisionError:
                return nan
        elif self.operator.type is TokenType.STAR:
            check_num_operand(self.operator, left, right)
            return left * right

        elif self.operator.type is TokenType.GREATER:
            check_num_operand(self.operator, left, right)
            return left > right
        elif self.operator.type is TokenType.GREATER_EQUAL:
            check_num_operand(self.operator, left, right)
            return left >= right
        elif self.operator.type is TokenType.LESS:
            check_num_operand(self.operator, left, right)
            return left < right
        elif self.operator.type is TokenType.LESS_EQUAL:
            check_num_operand(self.operator, left, right)
            return left <= right

        elif self.operator.type is TokenType.BANG_EQUAL:
            return not is_equal(left, right)
        elif self.operator.type is TokenType.EQUAL_EQUAL:
            return is_equal(left, right)

        return None


@dataclass
class Grouping(Expr):
    expression: Expr

    def eval(self) -> Any:
        return self.expression.eval()


@dataclass
class Literal(Expr):
    value: Any

    def eval(self) -> Any:
        return self.value


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def eval(self) -> Union[float, bool, None]:
        right = self.right.eval()

        if self.operator.type is TokenType.BANG:
            return not is_truthy(right)
        elif self.operator.type is TokenType.MINUS:
            check_num_operand(self.operator, right)
            return -right
        return None
