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

from typing import Any, Callable, Dict, Mapping, Optional, Tuple, TypeVar, Union

__all__ = ("parse_data",)

T = TypeVar("T")
D = TypeVar("D")

def parse_data(
    dict: Mapping[str, Any],
    key: str,
    convert_func: Optional[Callable[..., T]] = None,
    args: Tuple[Any, ...] = (), # this has to be provided in a raw tuple because *args isn't possible in this function
    kwargs: Dict[str, Any] = {}, # same here
    *,
    default: D = ...,
    _skip_none_check: bool = False
) -> Union[T, D, None]:
    val = dict.get(key, default)
    if val not in ((default, None) if not _skip_none_check else (default,)):
        return convert_func(*args, **kwargs) if convert_func else val
    return val
