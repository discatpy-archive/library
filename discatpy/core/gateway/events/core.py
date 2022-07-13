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

import inspect
from typing import Callable, List, TypeVar

from ...types import Snowflake, MISSING, MissingOr, MissingType
from ...utils import _create_fn, _from_import, _indent_text

__all__ = ("generate_handlers_from",)

T = TypeVar("T")

def _generate_body(args: List[inspect.Parameter]):
    ret_tuple = _indent_text("return (")

    if len(args) == 1:
        ret_tuple += "cast({0.annotation}, raw), ".format(args[0])
    else:
        for arg in args:
            ret_tuple += "cast({0.annotation}, raw.get(\"{0.name}\", MISSING)), ".format(arg)

    ret_tuple += ")"
    return [ret_tuple,]


def generate_handlers_from(src_cls: type) -> Callable[[T], T]:
    def wrapper(cls: T):
        ignore_keys: List[str] = getattr(src_cls, "__ignore__", [])
        proto_keys = [k for k in dir(src_cls) if k not in ignore_keys and not k.startswith("_")]

        # these function locals will be reused for every function, so it's better to define them here
        func_locals = {
            "Snowflake": Snowflake,
            "MISSING": MISSING,
            "_Missing": MissingType,
            "MissingOr": MissingOr,
        }
        _from_import(
            "typing",
            func_locals,
            [
                "Any",
                "cast",
                "Dict",
                "List",
                "Optional",
                "Tuple",
                "Type",
                "Union",
            ],
        )
        _from_import("discord_typings", func_locals)
        _from_import(
            "datetime",
            func_locals,
            [
                "datetime",
            ],
        )

        for k in proto_keys:
            proto = getattr(src_cls, k)
            sig = inspect.signature(proto)

            params = list(sig.parameters.values())
            params.pop(0) # this should ALWAYS be the self parameter
            
            func_body = _generate_body(params)
            func = _create_fn(f"handle_{k}", ["self", "raw: Any"], func_body, locals=func_locals)
            setattr(cls, f"handle_{k}", func)

        return cls
    return wrapper
