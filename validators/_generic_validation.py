from collections.abc import Callable
from functools import wraps
from inspect import signature
from typing import ParamSpec, TypeVar, cast

P = ParamSpec("P")
R = TypeVar("R")
V = TypeVar("V")


def _validate(
    field: str,
    validator: Callable[[V, str], V],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound = signature(func).bind(*args, **kwargs)
            value = cast(V, bound.arguments[field])
            bound.arguments[field] = validator(value, field)
            return func(*bound.args, **bound.kwargs)

        return wrapper

    return decorator