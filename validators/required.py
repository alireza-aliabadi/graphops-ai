from collections.abc import Callable
from typing import TypeVar, cast, overload

from validators._generic_validation import _validate

T = TypeVar("T")

def non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")

    return value.strip()


def confidence(value: float, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be a number")
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0")

    return float(value)


def positive(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer")
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")

    return value


@overload
def require_non_empty(field: str) -> Callable[[T], T]: ...


@overload
def require_non_empty(field: str, value: str) -> str: ...


def require_non_empty(
    field: str,
    value: str | None = None,
) -> Callable[[T], T] | str:
    if value is None:
        return cast(Callable[[T], T], _validate(field, non_empty))
    return non_empty(value, field)


@overload
def require_confidence(field: str) -> Callable[[T], T]: ...


@overload
def require_confidence(field: str, value: float) -> float: ...


def require_confidence(
    field: str,
    value: float | None = None,
) -> Callable[[T], T] | float:
    if value is None:
        return cast(Callable[[T], T], _validate(field, confidence))
    return confidence(value, field)


@overload
def require_positive(field: str) -> Callable[[T], T]: ...


@overload
def require_positive(field: str, value: int) -> int: ...


def require_positive(
    field: str,
    value: int | None = None,
) -> Callable[[T], T] | int:
    if value is None:
        return cast(Callable[[T], T], _validate(field, positive))
    return positive(value, field)