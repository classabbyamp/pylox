from .token import Token


HEADERS = """\
    node [ shape = Mrecord ];
    edge [ dir = none ];
    splines = true;
"""


class DotDiagram:
    def __init__(self):
        self.tokens = None
        self.tree = None
        self.root = None

    @classmethod
    def from_list(cls, tokens: list[Token]):
        obj = cls()
        obj.tokens = tokens
        obj.tree = False
        return obj

    @classmethod
    def from_tree(cls, root: int, tree: list[str]):
        obj = cls()
        obj.tokens = tree
        obj.tree = True
        obj.root = root
        return obj

    def __str__(self) -> str:
        if self.tree:
            toks = "\n".join("    " + ln for ln in self.tokens)
        else:
            toks = "\n".join("    " + token_to_dot(tok) for tok in self.tokens)
        return "digraph G {\n" + HEADERS + f"    root = n{self.root:x};" + "\n\n" + toks + "\n" + "}"


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


def token_to_dot(tok) -> str:
    if tok.literal is not None:
        return f"n{id(tok):x} [ label = <{'{'}{escape(tok.type.name)}|{escape(repr(tok.literal))}{'}'}> ];"
    return f"n{id(tok):x} [ label = <{'{'}{escape(tok.type.name)}{'}'}> ];"


def expr_to_dot(self, expr) -> str:
    ...
