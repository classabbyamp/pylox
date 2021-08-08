from os import PathLike
from pathlib import Path
from sys import stderr
from typing import Union

from .scanner import Scanner
from .parser import Parser
from .dot import DotDiagram
from .exceptions import LoxException


class Lox:
    def __init__(self):
        self.had_error = False

    @classmethod
    def run_file(cls, path: Union[str, PathLike]):
        obj = cls()

        path = Path(path)
        with path.open() as f:
            script = f.read()
        try:
            obj.run(script)
        except LoxException as e:
            obj.print_error(e)

        if obj.had_error:
            raise SystemExit(65)

    @classmethod
    def run_prompt(cls):
        obj = cls()

        while True:
            try:
                line = input("::<> ")
            except EOFError:
                break

            try:
                obj.run(line)
            except LoxException as e:
                obj.print_error(e)

            obj.had_error = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if expression is not None:
            print(DotDiagram.from_tree(id(expression), expression.dot()))

    def print_error(self, err: LoxException):
        print(err, file=stderr)
        self.had_error = True
