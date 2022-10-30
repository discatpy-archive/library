# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from collections.abc import Callable
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
            return instance.value & self.value == self.value
        return self.value

    def __set__(self, instance: t.Optional[Flag], value: bool) -> None:
        if instance:
            instance._set_value(self.value, value)  # pyright: ignore[reportPrivateUsage]

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
        member_map: dict[str, FlagMember] = {}

        for name, value in classdict.items():
            if isinstance(value, FlagMember):
                member_map[name] = value

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

    def __init__(self, **kwds: bool):
        self.value = type(self).default_value

        for flag_name, enabled in kwds.items():
            if hasattr(self, flag_name) and isinstance(
                (flag_val := getattr(self, flag_name)), FlagMember
            ):
                self._set_value(flag_val.value, enabled)
            else:
                raise ValueError(f"Invalid flag member with name {flag_name}!")

    def _set_value(self, value: int, enable: bool):
        if enable:
            self.value |= value
        else:
            self.value &= ~value

    def __or__(self, other: t.Union[Flag, FlagMember, int, t.Any]):
        if isinstance(other, int):
            return self.from_value(self.value | other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value | other.value)

        return NotImplemented

    def __and__(self, other: t.Union[Flag, FlagMember, int, t.Any]):
        if isinstance(other, int):
            return self.from_value(self.value & other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value & other.value)

        return NotImplemented

    def __add__(self, other: t.Union[Flag, FlagMember, int, t.Any]):
        return self | other

    def __sub__(self, other: t.Union[Flag, FlagMember, int, t.Any]):
        if isinstance(other, int):
            return self.from_value(self.value & ~other)
        elif isinstance(other, (Flag, FlagMember)):
            return self.from_value(self.value & ~other.value)

        return NotImplemented

    def __invert__(self):
        return self.from_value(~self.value)

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
