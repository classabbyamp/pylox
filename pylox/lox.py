from os import PathLike
from pathlib import Path
from sys import stderr
from typing import Union

from .scanner import Scanner


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
            obj.error(e.line, e.message)

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
                obj.error(e.line, e.message)

            obj.had_error = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        print(tokens)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}", file=stderr)
        self.had_error = True

class LoxException(Exception):
    """Exception for internal Lox errors."""
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message
