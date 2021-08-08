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
    def run_file(cls, path: Union[str, PathLike], dot=Union[str, PathLike]):
        obj = cls()

        path = Path(path)
        with path.open() as f:
            script = f.read()
        try:
            obj.run(script, dot=dot)
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

    @classmethod
    def run_inline(cls, cmd: str, dot=Union[str, PathLike]):
        obj = cls()

        try:
            obj.run(cmd, dot=dot)
        except LoxException as e:
            obj.print_error(e)

    def run(self, source: str, dot: Union[str, PathLike]):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if expression is not None:
            if dot:
                Path(dot).write_text(str(DotDiagram.from_tree(id(expression), expression.dot())))
            print(expression)

    def print_error(self, err: LoxException):
        print(err, file=stderr)
        self.had_error = True
