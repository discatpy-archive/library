# SPDX-License-Identifier: MIT

import inspect
import sys
import typing as t
from contextlib import contextmanager
from importlib import reload

if sys.version_info >= (3, 10):
    from types import UnionType

    union_types = (t.Union, UnionType)
else:
    union_types = (t.Union,)

__all__ = ("type_checking", "get_globals", "evaluate_annotation", "is_union")


@contextmanager
def type_checking():
    """A context manager to enable ``typing.TYPE_CHECKING`` then disable it."""
    t.TYPE_CHECKING = True

    try:
        yield
    finally:
        t.TYPE_CHECKING = False


# TODO: migrate to a more appropriate file
def get_globals(x: object) -> dict[str, t.Any]:
    """Gets all of the globals for x. This automatically enables
    typing.TYPE_CHECKING to ensure we get everything imported.

    Note:
        This will not work with anything defined in the Python
        Interactive Environment because inspect.getmodule does not
        properly work with the Python Interactive Environment.

    Args:
        x: The object you want to grab the globals for.
    """
    module = inspect.getmodule(x)

    if module:
        with type_checking():
            reload(module)

    return module.__dict__


def evaluate_annotation(x: str, globals: dict[str, t.Any], locals: dict[str, t.Any]) -> object:
    """Evaluates x into an object.

    Args:
        x: The string annotation you need to evalulate.
        globals: The globals to evalulate with.
        locals: The locals to evalulate with.
    """
    return eval(x, globals, locals)


def is_union(x: object) -> bool:
    """Determines whether x is a union or not.

    This supports typing.Union, along with types.UnionType introduced in 3.10.

    Args:
        x: The object to test for being a union or not.

    Returns:
        Whether or not the object provided is a union.
    """
    return t.get_origin(x) in union_types
