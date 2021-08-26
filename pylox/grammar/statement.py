from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..util.helpers import to_str, to_repr
from . import token, expression, literals
from ..env import Env


class Stmt(ABC):
    @abstractmethod
    def eval(self, env: Env):
        pass


@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def eval(self, env: Env):
        local_env = Env(env, repl=env.repl)

        for stmt in self.statements:
            stmt.eval(local_env)


@dataclass
class Expression(Stmt):
    expression: expression.Expr

    def eval(self, env: Env):
        val = self.expression.eval(env)
        if env.repl and not isinstance(self.expression, expression.Assign):
            print(to_repr(val))


@dataclass
class Print(Stmt):
    expression: expression.Expr

    def eval(self, env: Env):
        print(to_str(self.expression.eval(env)))


@dataclass
class Repr(Stmt):
    expression: expression.Expr

    def eval(self, env: Env):
        print(to_repr(self.expression.eval(env)))


@dataclass
class Var(Stmt):
    name: token.Token
    initialiser: Optional[expression.Expr]

    def eval(self, env: Env):
        val: literals.OptAnyLiteral = None
        if self.initialiser is not None:
            val = self.initialiser.eval(env)

        env.define(self.name, val)
