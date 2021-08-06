from .token import Token


HEADERS = """\
    node [ shape = Mrecord ];
    edge [ dir = none ];
"""


class DotDiagram:
    def __init__(self):
        pass

    @classmethod
    def from_list(cls, tokens: list[Token]):
        obj = cls()
        obj.tokens = tokens
        obj.tree = False
        return obj

    @classmethod
    def from_tree(cls, tokens):
        obj = cls()
        obj.tokens = tokens
        obj.tree = True
        return obj

    def __str__(self) -> str:
        if self.tree:
            toks = ""
        else:
            toks = "\n".join("    " + token_to_dot(tok) for tok in self.tokens)
        return "digraph G {\n" + HEADERS + "\n" + toks + "\n" + "}"


def token_to_dot(self) -> str:
    if self.literal is not None:
        return f"n{id(self):x} [ label = <{'{'}{escape(self.type.name)}|{escape(repr(self.literal))}{'}'}> ];"
    return f"n{id(self):x} [ label = <{'{'}{escape(self.type.name)}{'}'}> ];"


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
    return inp.translate(inp.maketrans(substitutions))
