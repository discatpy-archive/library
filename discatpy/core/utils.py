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

from typing import Any, Generic, Optional, TypeVar, Union

from .types import Snowflake

__all__ = (
    "DISCORD_EPOCH",
    "SnowflakeUtils",
    "MultipleValuesDict",
)


def _ensure_snowflake_is_int(sf: Snowflake) -> int:
    ret_id = sf
    if isinstance(ret_id, str):
        ret_id = int(ret_id)

    return ret_id


DISCORD_EPOCH = 1420070400000


class SnowflakeUtils:
    @staticmethod
    def snowflake_timestamp(id: Snowflake) -> int:
        """
        The timestamp stored in this object's Snowflake ID.

        Parameters
        ----------
        id: :type:`Snowflake`
            The snowflake to extract from
        """
        return (_ensure_snowflake_is_int(id) >> 22) + DISCORD_EPOCH

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
_DT = TypeVar("_DT")


class MultipleValuesDict(dict, Generic[_KT, _VT]):
    """A dictionary that supports having multiple values for one key.

    It does this by having the actual value in the dictionary be a list with all
    of those values.
    """

    def __setitem__(self, k: _KT, v: _VT) -> None:
        val = v
        if k in self:
            old_val = self.pop(k)
            if not isinstance(old_val, list):
                val = [old_val, v]
            else:
                val = old_val
                val.append(v)

        return super().__setitem__(k, val)

    def get_one(
        self, k: _KT, index: int, *, value_type: Optional[type] = None, default: _DT = None
    ) -> Union[_VT, _DT]:
        """Gets one value from a key that matches index and optionally type.

        If there is only one value assigned to that key then that will be returned.

        If the key provided is not found or there is no value that meets the 
        conditions provided, the default value will be returned.

        Parameters
        ----------
        k: :type:`_KT`
            The key of the value to look for.
        index: :type:`int`
            The index where the value is contained, if there are multiple values assigned to the
            key.
        _type: :type:`Optional[type]` = `None`
            The type of the value to grab. Defaults to `None`.
        default: :type:`_DT` = `None`
            The default value to return if getting a value failed.
        """
        values = self.get(k, default)

        if values is not default and isinstance(values, list):
            val = [v for i, v in enumerate(values) if i == index][0]

            if value_type is not None:
                val = val if isinstance(val, value_type) else default

            return val

        return values
