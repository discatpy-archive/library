# SPDX-License-Identifier: MIT

import typing as t
from enum import Enum, auto

__all__ = (
    "Unset",
    "UnsetOr",
)


class _UnsetEnum(Enum):
    Unset = auto()

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Unset"

    __str__ = __repr__


T = t.TypeVar("T")
Unset: t.Literal[_UnsetEnum.Unset] = _UnsetEnum.Unset
UnsetOr = t.Union[T, _UnsetEnum]
