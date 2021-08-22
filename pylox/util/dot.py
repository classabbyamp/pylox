from dataclasses import fields

from ..grammar import token, expression


HEADERS = """\
    node [ shape = Mrecord ];
    edge [ dir = none ];
    splines = true;
"""


class DotDiagram:
    def __init__(self, root: int, tree: list[str]):
        self.tokens = tree
        self.root = root

    def __str__(self) -> str:
        toks = "\n".join("    " + ln for ln in self.tokens)
        return "digraph G {\n" + HEADERS + f"    root = n{self.root:x};" + "\n\n" + toks + "\n" + "}"


class DotMixin:
    def dot(self, root: bool = True) -> list[str]:
        output = []
        if root:
            output.append(f"n{id(self):x} [ label = <{escape(type(self).__name__)}> ];")
        for field in fields(self):
            val = getattr(self, field.name)
            if isinstance(val, expression.Expr):
                output.append(f"n{id(val):x} [ label = <{escape(type(val).__name__)}> ];")
                output += val.dot()
            elif isinstance(val, token.Token):
                if val.literal is not None:
                    output.append(f"n{id(val):x} "
                                  f"[ label = <{'{'}{escape(val.type.name)}|{escape(repr(val.literal))}{'}'}> ];")
                output.append(f"n{id(val):x} [ label = <{'{'}{escape(val.type.name)}{'}'}> ];")
            else:
                output.append(f"n{id(val):x} [ label = <{escape(str(val)) if val is not None else 'nil'}> ];")
            output.append(f"n{id(self):x} -> n{id(val):x}")
        return output


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
