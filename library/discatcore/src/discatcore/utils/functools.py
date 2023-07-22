# SPDX-License-Identifier: MIT

import typing as t

from typing_extensions import Self

__all__ = ("classproperty",)

T = t.TypeVar("T")
ClsT = t.TypeVar("ClsT")


class classproperty(t.Generic[ClsT, T]):
    def __init__(self, fget: t.Callable[[ClsT], T], /) -> None:
        self.fget: "classmethod[ClsT, ..., T]"
        self.getter(fget)

    def getter(self, fget: t.Callable[[ClsT], T], /) -> Self:
        if not isinstance(fget, classmethod):
            raise ValueError(f"Callable {fget.__name__} is not a classmethod!")

        self.fget = fget
        return self

    def __get__(self, obj: t.Optional[t.Any], type: t.Optional[ClsT]) -> T:
        return self.fget.__func__(type)
