from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..util.helpers import to_str
from . import expression


class Stmt(ABC):
    @abstractmethod
    def eval(self):
        pass


@dataclass
class Expression(Stmt):
    expression: expression.Expr

    def eval(self):
        self.expression.eval()


@dataclass
class Print(Stmt):
    expression: expression.Expr

    def eval(self):
        print(to_str(self.expression.eval()))
