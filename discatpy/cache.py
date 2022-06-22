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
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

from .enums.channel import ChannelType
from .types.snowflake import *
from .utils import MultipleValuesDict

if TYPE_CHECKING:
    from .channel import RawChannel, GuildChannel
    from .client import Client
    from .guild import Guild
    from .message import Message
    from .user import User

__all__ = ("ClientCache",)


class ClientCache:
    """
    Represents the Client's internal cache. This stores objects received from the Discord
    API, like for example messages or channels.

    Attributes
    ----------
    client: :type:`Client`
        A reference to the client.
    _obj_cache: :type:`MultipleValuesDict[Snowflake, Any]`
        The internal cache that stores objects received from the Discord API.
    """

    def __init__(self, client: Client):
        self.client: Client = client
        self._obj_cache: MultipleValuesDict[Snowflake, Any] = MultipleValuesDict()

    def find(self, id: Snowflake) -> bool:
        """Checks if there is an object with that id in the cache.

        Parameters
        ----------
        id: :type:`Snowflake`
            The id to check for.

        Returns
        -------
        :type:`bool`
            A bool corresponding to if the id was found in the cache or not.
        """
        _obj = self._obj_cache.get(id)
        return _obj is not None

    def get(self, id: Snowflake) -> Union[List[Any], Any, None]:
        """Grabs all objects with the provided id from the cache.

        Parameters
        ----------
        id: :type:`Snowflake`
            The id of the object to get.

        Returns
        -------
        :type:`Optional[Union[List[Any], Any]]`
            All objects found with that id, None if not found.
        """
        return self._obj_cache.get(id)

    def get_type(self, id: Snowflake, t: type) -> Union[Any, None]:
        """Grabs an object with a specific type.

        Parameters
        ----------
        id: :type:`Snowflake`
            The id of the object to get.
        t: :type:`Any`
            The type of the object to get.

        Returns
        -------
        :type:`Optional[Any]`
            The object found with that type, None if not found.
        """
        objs = self.get(id)
        if objs and isinstance(objs, list):
            ret_obj: List[Any] = [
                o for o in objs if isinstance(o, t) or issubclass(o, t)
            ]
            return ret_obj[0] if len(ret_obj) > 0 else None

        return objs

    def add_message(self, message_obj: Message):
        """Adds a message object to the cache.

        Parameters
        ----------
        message_obj: :type:`Message`
            The message object to add.
        """
        message_obj._set_channel(
            self.client.grab(message_obj._channel_id, "RawChannel")
        )
        self._obj_cache[message_obj.id] = message_obj

    def add_channel(self, channel_obj: Union[RawChannel, GuildChannel]):
        """Adds a channel object to the cache.

        Parameters
        ----------
        channel_obj: :type:`RawChannel`
            The channel object to add.
        """
        if (
            channel_obj.type == ChannelType.DM.value
            or channel_obj.type == ChannelType.GROUP_DM.value
        ):
            # TODO: Consider removing this since all guilds the bot is in should already exist in the cache
            channel_obj._set_guild(self.client.grab(channel_obj._guild_id, "Guild"))

            if channel_obj._parent_id is not None:
                channel_obj._set_parent(
                    self.client.grab(channel_obj._parent_id, "RawChannel")
                )

        self._obj_cache[channel_obj.id] = channel_obj

    def add_user(self, user_obj: User):
        """Adds a user object to the cache.

        Parameters
        ----------
        user_obj: :type:`User`
            The user object to add.
        """
        self._obj_cache[user_obj.id] = user_obj

    def add_guild(self, guild_obj: Guild):
        """Adds a guild object to the cache.

        Parameters
        ----------
        guild_obj: :type:`Guild`
            The guild object to add.
        """
        self._obj_cache[guild_obj.id] = guild_obj

    def remove(self, obj: Any):
        """Removes an object from the cache.

        Parameters
        ----------
        obj: :type:`Any`
            The object to remove from the cache.
        """
        objs = self._obj_cache[obj.id]
        if isinstance(objs, list):
            for o in objs:
                if o == obj:
                    self._obj_cache[obj.id].pop(obj)
        else:
            if objs == obj:
                self._obj_cache.pop(obj)
