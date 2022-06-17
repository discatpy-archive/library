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

import asyncio
from typing import Any, Generic, Union, _SpecialForm, TypeVar

from .types.snowflake import *

__all__ = (
    "Unset",
    "DataEvent",
    "MISSING",
    "MaybeMissing",
    "DISCORD_EPOCH",
    "snowflake_timestamp",
    "snowflake_iwid",
    "snowflake_ipid",
    "snowflake_increment",
    "MultipleValuesDict",
)

# Data Event taken from here: https://gist.github.com/vcokltfre/69bef173a015d08a44e93fd4cbdaadd8

T = TypeVar("T")

class Unset:
    pass

class DataEvent(asyncio.Event, Generic[T]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data: Union[T, Unset] = Unset()

    async def wait(self) -> T:
        await super().wait()

        if isinstance(self.data, Unset):
            raise ValueError("DataEvent data is not set at end of event wait.")

        return self.data

    def set(self, data: T) -> None:
        super().set()
        self.data = data

    def clear(self) -> None:
        super().clear()
        self.data = Unset()

class _MissingDefine:
    __name__ = "MISSING"

    def __eq__(self, other) -> bool:
        raise NotImplementedError("MISSING cannot be compared")

    def __repr__(self):
        return self.__class__.__name__

    def __bool__(self):
        raise NotImplementedError("MISSING is not True or False, it is undefined")

    def __str__(self):
        return self.__repr__()

MISSING: Any = _MissingDefine()

@_SpecialForm
def MaybeMissing(self, parameters):
    return Union[type(MISSING), parameters]

def _ensure_snowflake_is_int(sf: Snowflake) -> int:
    ret_id = sf
    if isinstance(ret_id, str):
        ret_id = int(ret_id)

    return ret_id

DISCORD_EPOCH = 1420070400000

def snowflake_timestamp(id: Snowflake) -> int:
    """
    The timestamp stored in this object's Snowflake ID.

    Parameters
    ----------
    id: :type:`Snowflake`
        The snowflake to extract from
    """
    return (_ensure_snowflake_is_int(id) >> 22) + DISCORD_EPOCH

def snowflake_iwid(id: Snowflake) -> int:
    """
    The internal worker ID stored in this object's
    Snowflake ID.

    Parameters
    ----------
    id: :type:`Snowflake`
        The snowflake to extract from
    """
    return (_ensure_snowflake_is_int(id) & 0x3E0000) >> 17

def snowflake_ipid(id: Snowflake) -> int:
    """
    The internal process ID stored in this object's
    Snowflake ID.

    Parameters
    ----------
    id: :type:`Snowflake`
        The snowflake to extract from
    """
    return (_ensure_snowflake_is_int(id) & 0x1F000) >> 12

def snowflake_increment(id: Snowflake) -> int:
    """
    The increment of the object's Snowflake ID.

    Parameters
    ----------
    id: :type:`Snowflake`
        The snowflake to extract from
    """
    return _ensure_snowflake_is_int(id) & 0xFFF

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

# TODO: Consider replacing this with the multidict from aiohttp
class MultipleValuesDict(dict):
    """A dictionary that supports having multiple values for one key.

    It does this by having the actual value in the dictionary be a list with all
    of those values.
    """
    def __setitem__(self, __k: _KT, __v: _VT) -> None:
        val = __v
        if __k in self:
            old_val = self.pop(__k)
            if not isinstance(old_val, list):
                val = [old_val, __v]
            else:
                val = old_val
                val.append(__v)

        return super().__setitem__(__k, val)

    def get_one(self, __key: _KT, __index: int, /, _type: type = None, default: Any = None):
        """Gets one value from a key that matches index and optionally type.

        If there is only one value assigned to a key, the key provided is not found, or
        there is no value that meets the conditions provided, the default value will be returned.
        
        Parameters
        ----------
        __key: :type:`_KT`
            The key of the value to look for.
        __index: :type:`int`
            The index where the value is contained, if there are multiple values assigned to the
            key.
        _type: :type:`type`
            The type of the value to grab. Defaults to `None`.
        default: :type:`Any`
            The default value to return if getting a value failed.
        """
        values = self.get(__key, default)

        if values is not default and isinstance(values, list):
            val = [v for i, v in enumerate(values) if i == __index][0]

            if _type is not None:
                val = val if isinstance(val, _type) else default

            return val

        return values