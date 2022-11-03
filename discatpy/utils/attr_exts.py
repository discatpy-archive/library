# SPDX-License-Identifier: MIT
from __future__ import annotations

import inspect
import typing as t
from collections.abc import Callable, Mapping
from types import FunctionType

import attr
from discatcore.types import Unset

from .typing import evaluate_annotation, get_globals, is_union

T = t.TypeVar("T")
TT = t.TypeVar("TT", bound=type)
MT = t.TypeVar("MT", bound=Mapping[str, t.Any])

__all__ = ("ToDictMixin", "make_sentinel_converter", "frozen_for_public")

_no_sentinel_found = object()


def _sentinel_to_be_filtered(cls: type) -> object:
    res: object = _no_sentinel_found

    for field in attr.fields(cls):
        field_type = (
            evaluate_annotation(field.type, get_globals(cls), {})
            if isinstance(field.type, str)
            else field.type
        )
        if is_union(field_type):
            # if we detect Unset, then we should filter that and not None
            union_args = t.get_args(field_type)
            if type(Unset) in union_args:
                res = Unset
            # otherwise, filter out None
            elif type(None) in union_args:
                res = None

    return res


# this is defined outside of ToDictMixin because I don't want to pollute
# the subclasses with internal stuff
def _generate_to_dict(cls: type[ToDictMixin[MT]]) -> Callable[[t.Any], MT]:
    function_template = """
def to_dict(self):
    data = {{{0}}}
    return dict(filter(_should_be_filtered, data.items()))
""".lstrip()

    dict_define = ",".join(f'"{field.name}":self.{field.name}' for field in attr.fields(cls))
    sentinel = _sentinel_to_be_filtered(cls)

    def _should_be_filtered(item: tuple[str, t.Any]) -> bool:
        if sentinel is not _no_sentinel_found:
            return item[1] is not sentinel
        return True

    function_code = compile(
        function_template.format(dict_define), "<ToDictMixin.to_dict method>", "exec"
    )
    _globals = {"_should_be_filtered": _should_be_filtered}
    _locals = {}
    exec(function_code, _globals, _locals)
    return t.cast(Callable[[t.Any], MT], _locals["to_dict"])


class ToDictMixin(t.Generic[MT]):
    """A mixin that adds an auto-generated to_dict method based on all of the
    fields.

    Unlike ``attr.asdict``, this filters out attributes that are ``None`` or ``Unset``.
    """

    _actual_to_dict_: t.Optional[Callable[[t.Any], MT]] = None

    def to_dict(self) -> MT:
        if not self._actual_to_dict_:
            self._actual_to_dict_ = _generate_to_dict(type(self))
        return self._actual_to_dict_(self)


def make_sentinel_converter(
    original: Callable[[t.Any], T], *sentinels: t.Any
) -> Callable[[t.Any], T]:
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


def frozen_for_public(cls: type[T]) -> type[T]:
    """Decorator to take any attrs-generated class and make it frozen when an attribute
    is set outside of a frame inside a class method.

    This works by taking the previous frame and checking if that frame is inside of a
    class method. If not, then ``attr.exceptions.FrozenAttributeError`` is raised.

    Args:
        cls: The attrs-generated class to modify.

    Raises:
        ``attrs.exceptions.NotAnAttrsClassError``: The class provided is not attrs-generated.

    Returns:
        The modified attrs-generated class.
    """
    if not attr.has(cls):
        raise attr.exceptions.NotAnAttrsClassError

    def __frozen_setattr__(self: T, name: str, value: t.Any):
        __original_setattr__ = t.cast(
            FunctionType,
            getattr(cls.__mro__[1], "__setattr__", object.__setattr__),
        ).__get__(self, cls)

        stack = inspect.stack()
        assert len(stack) > 1

        self_param = stack[1].frame.f_locals.get("self")
        if isinstance(self_param, cls) and self_param is self:
            __original_setattr__(name, value)
        else:
            raise attr.exceptions.FrozenAttributeError

    setattr(cls, "__setattr__", __frozen_setattr__)
    return cls
