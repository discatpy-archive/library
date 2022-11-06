# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from collections.abc import Callable, Iterator
from functools import reduce
from operator import or_

from typing_extensions import Self

__all__ = (
    "FlagMember",
    "flag",
    "FlagMeta",
    "Flag",
)


class FlagMember:
    def __init__(self, name: str, value: int):
        self._name_ = name
        self._value_ = value

    def __get__(self, instance: t.Optional[Flag], _: type[Flag]) -> t.Union[int, bool]:
        if instance:
            return instance.has(self.value)
        return self.value

    def __set__(self, instance: t.Optional[Flag], toggle: bool) -> None:
        if instance:
            instance.set(self.value, toggle)

    @property
    def name(self) -> str:
        return self._name_

    @property
    def value(self) -> int:
        return self._value_


def flag(func: Callable[..., int]) -> FlagMember:
    return FlagMember(func.__name__, func())


class FlagMeta(type):
    """An EnumMeta-like metaclass that implements custom flags.

    Custom flags have some differences from stdlib flags. The most noticeable ones are:

    - the type of each member is a separate class and not an instance of the new class itself
    - every member has to be a FlagMember (defined via the flag decorator or defined explicitly)
    - you can set members to a bool value to turn them off or on
    - you can get members to get a bool value corresponding to whether or not it's on
    """

    _default_value: int
    __members__: dict[str, FlagMember]

    def __new__(
        cls: type[Self],
        name: str,
        bases: tuple[type, ...],
        classdict: dict[str, t.Any],
        **kwds: t.Any,
    ) -> Self:
        member_map: dict[str, FlagMember] = {
            n: v for n, v in classdict.items() if isinstance(v, FlagMember)
        }

        default_value: int = 0
        if kwds.pop("inverted", False):
            max_bits = max([fm.value for fm in member_map.values()]).bit_length()
            default_value = (2**max_bits) - 1

        ns: dict[str, t.Any] = {
            "__members__": member_map,
            "_default_value": default_value,
            **classdict,
        }

        return super().__new__(cls, name, bases, ns, **kwds)

    @property
    def default_value(cls) -> int:
        return cls._default_value


class Flag(metaclass=FlagMeta):
    """A custom flag implementation. Uses ``FlagMeta`` as its metaclass."""

    value: int
    _default_value: t.ClassVar[int]
    __members__: t.ClassVar[dict[str, FlagMember]]

    def __init__(self, **kwds: bool):
        self.value = type(self).default_value

        for flag_name, enabled in kwds.items():
            if hasattr(self, flag_name) and flag_name in self.__members__:
                self.set(self.__members__[flag_name].value, enabled)
            else:
                raise ValueError(f"Invalid flag member {flag_name}!")

    def set(self, value: int, toggle: bool):
        if toggle:
            self.value |= value
        else:
            self.value &= ~value

    def has(self, value: int):
        return self.value & value == value

    def __or__(self, other: t.Any):
        if isinstance(other, int):
            return self.from_value(self.value | other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value | other.value)

        return NotImplemented

    def __and__(self, other: t.Any):
        if isinstance(other, int):
            return self.from_value(self.value & other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value & other.value)

        return NotImplemented

    def __add__(self, other: t.Any):
        return self | other

    def __sub__(self, other: t.Any):
        if isinstance(other, int):
            return self.from_value(self.value & ~other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value & ~other.value)

        return NotImplemented

    def __invert__(self):
        return self.from_value(~self.value)

    def __contains__(self, item: t.Any):
        if isinstance(item, int):
            return self.has(item)

        return NotImplemented

    __ror__ = __or__
    __rand__ = __and__
    __radd__ = __add__
    __rsub__ = __sub__

    def __iter__(self) -> Iterator[tuple[str, bool]]:
        for name in self.__members__:
            yield name, getattr(self, name)

    @classmethod
    def from_value(cls: type[Self], value: int) -> Self:
        self = cls()
        self.value = value
        return self

    @classmethod
    def all(cls: type[Self]) -> Self:
        member_vals = [f.value for f in cls.__members__.values()]
        all_values = reduce(or_, member_vals)
        return cls.from_value(all_values)

    @classmethod
    def none(cls: type[Self]) -> Self:
        return cls.from_value(cls.default_value)
