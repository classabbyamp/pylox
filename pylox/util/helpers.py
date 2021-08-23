from typing import Any, Union

from . import exceptions
from ..grammar import token
from ..grammar.literals import LoxBool, LoxNil


def to_str(obj: Union[str, float, LoxBool, LoxNil]) -> str:
    if isinstance(obj, float):
        return f"{obj:g}"
    elif isinstance(obj, str):
        return f'"{obj}"'
    return str(obj)


def is_truthy(obj: Any) -> bool:
    if obj == LoxNil():
        return False
    elif isinstance(obj, bool):
        return obj
    return True


def is_equal(a: Any, b: Any) -> bool:
    if isinstance(a, LoxNil) and isinstance(b, LoxNil):
        return True
    if type(a) == type(b):
        return a == b
    return False


def check_num_operand(operator: token.Token, *operands: Any):
    if not all(isinstance(operand, float) for operand in operands):
        raise exceptions.LoxRuntimeError(operator, "operand must be a number")
