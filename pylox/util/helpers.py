from . import exceptions
from ..grammar import token
from ..grammar.literals import AnyLiteral, LoxBool, LoxNil


def to_repr(obj: AnyLiteral) -> str:
    if isinstance(obj, float):
        return f"{obj:g}"
    elif isinstance(obj, str):
        return f'"{obj}"'
    return str(obj)


def to_str(obj: AnyLiteral) -> str:
    if isinstance(obj, float):
        return f"{obj:g}"
    elif isinstance(obj, str):
        return f'{obj}'
    return str(obj)


def is_truthy(obj: AnyLiteral) -> bool:
    if obj == LoxNil():
        return False
    elif isinstance(obj, LoxBool):
        return obj.value
    return True


def is_equal(a: AnyLiteral, b: AnyLiteral) -> LoxBool:
    if isinstance(a, LoxNil) and isinstance(b, LoxNil):
        return LoxBool(True)
    if type(a) == type(b):
        return LoxBool(a == b)
    return LoxBool(False)


def check_num_operand(operator: token.Token, *operands: AnyLiteral):
    if not all(isinstance(operand, float) for operand in operands):
        raise exceptions.LoxRuntimeError(operator, "operand must be a number")
