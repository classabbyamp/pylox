from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..util.helpers import to_str, to_repr, is_truthy
from ..util.exceptions import LoxBreakException
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


@dataclass
class If(Stmt):
    condition: expression.Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def eval(self, env: Env):
        if is_truthy(self.condition.eval(env)):
            self.then_branch.eval(env)
        elif self.else_branch is not None:
            self.else_branch.eval(env)


@dataclass
class While(Stmt):
    condition: expression.Expr
    body: Stmt

    def eval(self, env: Env):
        try:
            while is_truthy(self.condition.eval(env)):
                self.body.eval(env)
        except LoxBreakException:
            pass


@dataclass
class Break(Stmt):
    def eval(self, env: Env):
        raise LoxBreakException
