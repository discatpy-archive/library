"""
The MIT License (MIT)

Copyright (c) 2022-present EmreTech

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import Any

from ._client import _HTTPClient

__all__ = ("HTTPClient",)

def _flatten_tuple(t: tuple[Any]):
    ret: list[Any] = []

    for i in t:
        if isinstance(i, tuple):
            ret.extend(_flatten_tuple(i))
        else:
            ret.append(i)

    return tuple(ret)

class _InheritMetaclass(type):
    """A helper metaclass that allows for the target class to inherit from a tuple of bases.
    This is used because it allows for dynamic bases and it's a little easier to read.
    
    If you're a normal developer, you shouldn't be using this.
    """
    def __new__(cls, name, bases, attrs, **kwargs):
        if "bases_tuple" in kwargs:
            bases = list(bases)
            bases.extend(kwargs.get("bases_tuple"))
            bases = _flatten_tuple(tuple(bases))

            return super(_InheritMetaclass, cls).__new__(cls, name, bases, attrs)
        else:
            raise ValueError("bases_tuple must be passed into kwargs in order to use this metaclass")

class HTTPClient(metaclass=_InheritMetaclass, bases_tuple=(_HTTPClient,)):
    pass