from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import nan
from typing import Any, Union

from .literals import LoxBool, LoxNil
from .token import Token, TokenType
from ..util.exceptions import LoxRuntimeError
from ..util.helpers import is_truthy, is_equal, check_num_operand


class Expr(ABC):
    @abstractmethod
    def eval(self):
        pass


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
    value: Union[str, float, LoxBool, LoxNil]

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
