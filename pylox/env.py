from collections.abc import MutableMapping
from typing import Iterator

from .grammar.token import Token
from .grammar.literals import AnyLiteral, OptAnyLiteral
from .util.exceptions import LoxRuntimeError


class Env(MutableMapping):
    def __init__(self, enclosing: 'Env' = None, repl: bool = False):
        self.enclosing = enclosing
        self.repl = repl

        self._values: dict[str, OptAnyLiteral] = {}

    def __getitem__(self, name: Token) -> OptAnyLiteral:
        try:
            if (val := self._values[name.lexeme]) is not None:
                return val
            raise LoxRuntimeError(name, f"Uninitialised variable '{name.lexeme}'.")
        except KeyError:
            if self.enclosing is not None:
                return self.enclosing[name]
            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def __setitem__(self, name: Token, value: AnyLiteral):
        self._values[name.lexeme] = value

    def __delitem__(self, name: Token):
        del self._values[name.lexeme]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def define(self, name: Token, value: OptAnyLiteral):
        self._values[name.lexeme] = value

    def assign(self, name: Token, value: AnyLiteral):
        if name.lexeme in self._values:
            self[name] = value
        else:
            if self.enclosing is not None:
                self.enclosing.assign(name, value)
            else:
                raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
