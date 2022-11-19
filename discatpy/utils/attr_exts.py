# SPDX-License-Identifier: MIT
from __future__ import annotations

import inspect
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

__all__ = ("is_attr_class", "ToDictMixin", "make_sentinel_converter", "frozen_for_public")


def is_attr_class(cls: type) -> TypeGuard[type[AttrsInstance]]:
    """Whether or not the provided class is an attrs class.

    Unlike ``attr.has``, this is a type guard for the provided class being
    an attrs instance.

    Args:
        cls: The class to check for.
    """
    return attr.has(cls)


def _sentinel_to_be_filtered(cls: type[AttrsInstance]) -> t.Optional[tuple[object, ...]]:
    res: t.Optional[tuple[object, ...]] = None

    for field in attr.fields(cls):
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

        data = {field.name: getattr(self, field.name) for field in attr.fields(cls)}

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


def _get_unique_setattr(cls: type) -> Callable[[object, str, t.Any], None]:
    for base in cls.__mro__[1:]:
        if (
            base_setattr := getattr(base, "__setattr__", object.__setattr__)
        ) is not object.__setattr__:
            return base_setattr

    return object.__setattr__


def frozen_for_public(cls: type[T]) -> type[T]:
    """Decorator to take any class and make it frozen when an attribute
    is set outside of a frame inside a class method.

    This works by taking the previous frame and checking if that frame is inside of a
    class method. If not, then ``attr.exceptions.FrozenAttributeError`` is raised.

    Args:
        cls: The class to modify.

    Returns:
        The modified class.
    """

    def __frozen_setattr__(self: T, name: str, value: t.Any):
        __original_setattr__ = _get_unique_setattr(cls).__get__(self, cls)

        stack = inspect.stack()
        assert len(stack) > 1

        last_frame = stack[1]
        self_param = last_frame.frame.f_locals.get("self")

        if isinstance(self_param, cls) and self_param is self:
            __original_setattr__(name, value)
        else:
            raise attr.exceptions.FrozenAttributeError

    setattr(cls, "__setattr__", __frozen_setattr__)
    return cls
