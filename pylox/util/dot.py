from dataclasses import fields
from typing import Union

from ..grammar import token, expr, stmt
from .helpers import to_str


HEADERS = """\
    node [ shape = Mrecord ];
    edge [ dir = none ];
    splines = true;
"""


def escape(inp: str) -> str:
    substitutions = {
        "&":  "&amp;",
        '"':  "&quot;",
        "]":  "&#x5D;",
        "<":  "&#x3C;",
        ">":  "&#x3E;",
        " ":  "&#x2423;",
        "\a": "\\a",
        "\b": "\\b",
        "\f": "\\f",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\v": "\\v",
    }
    return inp.translate(inp.maketrans(substitutions))  # type: ignore


def dot(obj: Union[expr.Expr, stmt.Stmt], root: bool = True) -> list[str]:
    output = []
    if root:
        output.append(f"n{id(obj):x} [ label = <{escape(type(obj).__name__)}> ];")
    for field in fields(obj):
        val = getattr(obj, field.name)
        if isinstance(val, expr.Expr) or isinstance(val, stmt.Stmt):
            output.append(f"n{id(val):x} [ label = <{escape(type(val).__name__)}> ];")
            output += dot(val)
        elif isinstance(val, token.Token):
            if val.literal is not None:
                output.append(f"n{id(val):x} "
                              f"[ label = <{'{'}{escape(val.type.name)}|{escape(repr(val.literal))}{'}'}> ];")
            output.append(f"n{id(val):x} [ label = <{'{'}{escape(val.type.name)}{'}'}> ];")
        else:
            output.append(f"n{id(val):x} [ label = <{escape(to_str(val))}> ];")
        output.append(f"n{id(obj):x} -> n{id(val):x}")
    return output


def dot_diagram(root: stmt.Stmt, tree: list[stmt.Stmt]) -> str:
    lines = []
    for s in tree:
        lines += dot(s)
    root_id = id(root)
    nodes = "\n".join("    " + ln for ln in lines)
    return "digraph G {\n" + HEADERS + f"    root = n{root_id:x};" + "\n\n" + nodes + "\n" + "}"
