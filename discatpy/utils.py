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
from typing import Generic, Union, TypeVar

from .types.snowflake import *

T = TypeVar("T")

__all__ = (
    "Unset",
    "DataEvent",
    "DISCORD_EPOCH",
    "snowflake_timestamp",
    "snowflake_iwid",
    "snowflake_ipid",
    "snowflake_increment",
    "get_avatar_url",
    "get_default_avatar_url",
    "get_banner_url",
)

# Data Event taken from here: https://gist.github.com/vcokltfre/69bef173a015d08a44e93fd4cbdaadd8

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

BASE_CDN_PATH = "https://cdn.discordapp.com/"

def get_avatar_url(id: Snowflake, hash: str):
    """
    Returns the avatar url of a user.

    Parameters
    ----------
    id: :type:`Snowflake`
        The user id
    hash: :type:`str`
        The avatar hash
    """
    return BASE_CDN_PATH + "avatars/" + str(id) + "/" + hash

def get_default_avatar_url(discrim: str):
    """
    Returns the default avatar url of a user.
    This is calculated with their discriminator.

    Parameters
    ----------
    discrim: :type:`str`
        The discriminator for this user
    """
    return BASE_CDN_PATH + "embed/avatars/" + str(int(discrim) % 5) + ".png"

def get_banner_url(id: Snowflake, hash: str):
    """
    Returns the banner url of a user or guild.

    Parameters
    ----------
    id: :type:`Snowflake`
        The user/guild id
    hash: :type:`str`
        The banner hash
    """
    return BASE_CDN_PATH + "banners/" + str(id) + "/" + hash