# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from collections.abc import Callable, Mapping

import attr
from discatcore.types import Unset
from typing_extensions import TypeGuard, TypeVarTuple, Unpack

from .typing import get_globals, is_union

if t.TYPE_CHECKING:
    from attr import AttrsInstance

T = t.TypeVar("T")
Ts = TypeVarTuple("Ts")
MT = t.TypeVar("MT", bound=Mapping[str, t.Any])

__all__ = (
    "is_attr_class",
    "fields",
    "ToDictMixin",
    "make_sentinel_converter",
)


def is_attr_class(cls: type) -> TypeGuard[type[AttrsInstance]]:
    """Whether or not the provided class is an attrs class.

    Unlike ``attr.has``, this is a type guard for the provided class being
    an attrs instance.

    Args:
        cls: The class to check for.
    """
    return attr.has(cls)


def fields(cls: type[AttrsInstance]) -> tuple[attr.Attribute[t.Any], ...]:
    """Returns a tuple of all of the fields for an attrs class.

    Unlike ``attr.fields``, this ensures that every field returned is actually
    an attrs field.

    Args:
        cls: The class to check for.

    Raises:
        attr.exceptions.NotAnAttrsClassError: The class provided is not an attrs class.
    """
    return attr.fields(cls)


def _sentinel_to_be_filtered(cls: type[AttrsInstance]) -> t.Optional[tuple[object, ...]]:
    res: t.Optional[tuple[object, ...]] = None

    for field in fields(cls):
        field_type = (
            eval(field.type, get_globals(cls), {}) if isinstance(field.type, str) else field.type
        )
        if is_union(field_type):
            # if we detect Unset, then we should filter that and not None
            union_args = t.get_args(field_type)
            if type(Unset) in union_args:
                res = (Unset,)
            # otherwise, filter out None
            elif type(None) in union_args:
                res = (None,)

    return res


class ToDictMixin(t.Generic[MT]):
    """A mixin that adds an auto-generated to_dict method based on all of the
    fields.

    Unlike ``attr.asdict``, this filters out any sentinels you give it.
    """

    __sentinels_to_filter__: t.Optional[tuple[object, ...]] = None

    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        super().__init_subclass__(**kwargs)

        sentinels: t.Optional[tuple[object, ...]] = kwargs.get("sentinels", None)
        cls.__sentinels_to_filter__ = sentinels

    def to_dict(self) -> MT:
        cls = type(self)
        if not is_attr_class(cls):
            raise attr.exceptions.NotAnAttrsClassError

        data = {field.name: getattr(self, field.name) for field in fields(cls)}

        if self.__sentinels_to_filter__ is None:
            sentinels = _sentinel_to_be_filtered(cls)
        else:
            sentinels = self.__sentinels_to_filter__

        def _should_be_filtered(item: tuple[str, t.Any]) -> bool:
            if sentinels is not None:
                return item[1] not in sentinels
            return True

        return t.cast(MT, dict(filter(_should_be_filtered, data.items())))


def make_sentinel_converter(
    original: Callable[[t.Any], T], *sentinels: Unpack[Ts]
) -> Callable[[t.Any], t.Union[Unpack[Ts], T]]:
    """Creates a converter function that ignores sentinels.

    Args:
        original: The original converter.
        *sentinels: All sentinels to ignore.

    Returns:
        A function that ignores sentinels then wraps the original converter.
    """

    def wrapper(val: t.Any) -> T:
        if val in sentinels:
            return val
        return original(val)

    return wrapper
