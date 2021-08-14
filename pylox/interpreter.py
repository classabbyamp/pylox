from typing import Any

from .exceptions import LoxRuntimeError
from .token import Token


def to_str(obj: Any) -> str:
    if obj is None:
        return "nil"
    elif isinstance(obj, float):
        return f"{obj:g}"
    elif isinstance(obj, str):
        return f'"{obj}"'
    return str(obj)


def is_truthy(obj: Any) -> bool:
    if obj is None:
        return False
    elif isinstance(obj, bool):
        return obj
    return True


def is_equal(a: Any, b: Any) -> bool:
    if a is None and b is None:
        return True
    if type(a) == type(b):
        return a == b
    return False


def check_num_operand(operator: Token, *operands: Any):
    if not all(isinstance(operand, float) for operand in operands):
        raise LoxRuntimeError(operator, "operand must be a number")
