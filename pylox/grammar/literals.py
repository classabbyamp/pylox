from typing import Union, Optional


class LoxBool:
    def __init__(self, value: bool = False):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value).lower()

    __str__ = __repr__

    def __eq__(self, o: object) -> bool:
        return self.value == o


class LoxNil:
    def __init__(self):
        self.value = None

    def __str__(self) -> str:
        return "nil"

    def __repr__(self) -> str:
        return "nil"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LoxNil):
            return True
        return o is None


AnyLiteral = Union[str, float, LoxBool, LoxNil]

OptAnyLiteral = Optional[AnyLiteral]

NotStr = Union[float, LoxBool, LoxNil]
