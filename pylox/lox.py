from os import PathLike
from pathlib import Path
from sys import stderr
from typing import Union

from .scanner import Scanner
from .parser import Parser
from .interpreter import interpret
from .util.dot import dot_diagram
from .util.exceptions import LoxException


class Lox:
    def __init__(self):
        self.had_error = False

    @classmethod
    def run_file(cls, path: Union[str, PathLike], dot: bool = False):
        obj = cls()

        path = Path(path)
        with path.open() as f:
            script = f.read()
        try:
            obj.run(script, dot_file=path.with_suffix(".dot") if dot else None)
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
    def run_inline(cls, cmd: str, dot: bool = False):
        obj = cls()

        try:
            obj.run(cmd, dot_file=Path("cmd.dot") if dot else None)
        except LoxException as e:
            obj.print_error(e)

    def run(self, source: str, dot_file: Path = None):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        stmts = parser.parse()

        if stmts:
            if dot_file is not None:
                dot_file.write_text(dot_diagram(stmts[0], stmts))
            try:
                interpret(stmts)
            except LoxException as e:
                self.print_error(e)

    def print_error(self, err: LoxException):
        print(err, file=stderr)
        self.had_error = True
