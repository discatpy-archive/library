# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from enum import EnumMeta, IntFlag as _IntFlag, _EnumDict  # pyright: ignore[reportPrivateUsage]
from functools import reduce
from operator import or_

from typing_extensions import Self

__all__ = (
    "FlagMeta",
    "Flag",
)


class FlagMeta(EnumMeta):
    """A custom EnumMeta class that adds additional support for our implementation of flags."""

    _default_value: int

    def __new__(
        cls: type[Self], name: str, bases: tuple[type, ...], classdict: _EnumDict, **kwds: t.Any
    ) -> Self:
        if int not in bases:
            raise TypeError("Int is a required base for Flags")

        new_cls = super().__new__(cls, name, bases, classdict, **kwds)
        inverted = kwds.pop("inverted", False)
        default_value = 0

        if inverted:
            max_bits = t.cast(
                int, max([e.value for e in new_cls._member_map_.values()])
            ).bit_length()
            default_value = -1 + (2**max_bits)

        setattr(new_cls, "_default_value", default_value)
        return new_cls

    @property
    def default_value(cls) -> int:
        return cls._default_value


class Flag(_IntFlag, metaclass=FlagMeta):
    """A custom flag implementation. Uses FlagMeta as its metaclass."""

    @classmethod
    def all(cls: type[Self]) -> Self:
        member_vals = [f.value for f in cls.__members__.values()]
        all_values = reduce(or_, member_vals)
        return cls(all_values)

    @classmethod
    def none(cls: type[Self]) -> Self:
        return cls(cls.default_value)
