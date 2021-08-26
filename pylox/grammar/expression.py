from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import nan

from .literals import LoxBool, LoxNil, OptAnyLiteral, AnyLiteral, NotStr
from .token import Token, TokenType
from ..util.exceptions import LoxRuntimeError
from ..util.helpers import is_truthy, is_equal, check_num_operand
from ..env import Env


class Expr(ABC):
    @abstractmethod
    def eval(self, env: Env):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def eval(self, env: Env) -> AnyLiteral:
        left = self.left.eval(env)
        right = self.right.eval(env)

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
            return LoxBool(left > right)
        elif self.operator.type is TokenType.GREATER_EQUAL:
            check_num_operand(self.operator, left, right)
            return LoxBool(left >= right)
        elif self.operator.type is TokenType.LESS:
            check_num_operand(self.operator, left, right)
            return LoxBool(left < right)
        elif self.operator.type is TokenType.LESS_EQUAL:
            check_num_operand(self.operator, left, right)
            return LoxBool(left <= right)

        elif self.operator.type is TokenType.BANG_EQUAL:
            return not is_equal(left, right)
        elif self.operator.type is TokenType.EQUAL_EQUAL:
            return is_equal(left, right)

        return LoxNil()


@dataclass
class Grouping(Expr):
    expression: Expr

    def eval(self, env: Env) -> AnyLiteral:
        return self.expression.eval(env)


@dataclass
class Literal(Expr):
    value: AnyLiteral

    def eval(self, env: Env) -> AnyLiteral:
        return self.value


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def eval(self, env: Env) -> NotStr:
        right = self.right.eval(env)

        if self.operator.type is TokenType.BANG:
            return not is_truthy(right)
        elif self.operator.type is TokenType.MINUS:
            check_num_operand(self.operator, right)
            return -right
        return LoxNil()


@dataclass
class Variable(Expr):
    name: Token

    def eval(self, env: Env) -> OptAnyLiteral:
        return env[self.name]


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

    def eval(self, env: Env) -> AnyLiteral:
        val = self.value.eval(env)

        env.assign(self.name, val)
        return val
