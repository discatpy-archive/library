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

from typing import Any, Dict, List, overload, TYPE_CHECKING
import asyncio

from .types.channel import ChannelType
from .types.snowflake import *
from .channel import GuildChannel, RawChannel, TextChannel, VoiceChannel
from .guild import Guild
from .message import Message
from .user import User

if TYPE_CHECKING:
    from .client import Client

__all__ = (
    "ClientCache",
)

def _convert_dict_to_channel(client, channel_dict: Dict[str, Any]):
    channel_type = channel_dict.get("type")

    if channel_type == ChannelType.GUILD_TEXT or channel_type == ChannelType.GUILD_NEWS:
        return TextChannel.from_dict(client, channel_dict)
    elif channel_type == ChannelType.GUILD_VOICE or channel_type == ChannelType.GUILD_STAGE_VOICE:
        return VoiceChannel.from_dict(client, channel_dict)

    return TypeError("Invalid channel dict provided")

class ClientCache:
    """
    Represents the Client's internal cache. This stores objects received from the Discord
    API, like for example messages or channels.

    Attributes
    ----------
    client: :type:`Client`
        A reference to the client.
    _obj_cache: :type:`Dict[Snowflake, Any]`
        The internal cache that stores objects received from the Discord API.
    """
    if TYPE_CHECKING:
        client: Client

        @overload
        def __init__(self, client: Client):
            ...

    def __init__(self, client) -> None:
        self.client = client
        self._obj_cache: Dict[Snowflake, Any] = {}

        # TODO: Remove this, there are some "contraditions"
        self.message_ids: List[Snowflake] = []
        self.channel_ids: List[Snowflake] = []
        self.user_ids: List[Snowflake] = []
        self.guild_ids: List[Snowflake] = []
    
    def find(self, id: Snowflake) -> bool:
        """
        Checks if there is an object with that id in the cache.

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

    def get(self, id: Snowflake) -> Any:
        """
        Attempts to grab an object from the cache.
        This will first check if there is any such object in the cache.

        Parameters
        ----------
        id: :type:`Snowflake`
            The id of the object to get.

        Returns
        -------
        :type:`Any`
            The object found, `None` if it doesn't exist.
        """
        return self._obj_cache.get(id)

    def _add(self, obj: Any):
        # the obj variable is expected to be mixed in with the Snowflake Mixin
        if not hasattr(obj, "id"):
            raise ValueError("obj is expected to have id attribute")
        
        self._obj_cache[obj.id] = obj

    def add_message(self, message_obj: Message):
        """
        Adds a message object to the cache.

        Parameters
        ----------
        message_obj: :type:`Message`
            The message object to add.
        """
        message_channel = self.get(message_obj.channel_id)

        if message_channel is None:
            loop = asyncio.get_running_loop()
            message_channel = loop.run_in_executor(self.client.http.get_channel(message_obj.channel_id))
            message_channel = _convert_dict_to_channel(self.client, message_channel)

        message_obj.channel = message_channel
        self._add(message_obj)
        self.message_ids.append(message_obj.id)

    def add_channel(self, channel_obj: RawChannel):
        """
        Adds a channel object to the cache.

        Parameters
        ----------
        channel_obj: :type:`RawChannel`
            The channel object to add.
        """
        if isinstance(channel_obj, GuildChannel):
            channel_guild = self.get(channel_obj.guild_id)

            if channel_guild is None:
                loop = asyncio.get_event_loop()
                channel_guild = loop.run_in_executor(self.client.http.get_guild(channel_obj.guild_id))
                channel_guild = Guild.from_dict(channel_guild)
            
            channel_obj.guild = channel_guild

        self._add(channel_obj)
        self.channel_ids.append(channel_obj.id)

    def add_user(self, user_obj: User):
        """
        Adds a user object to the cache.

        Parameters
        ----------
        user_obj: :type:`User`
            The user object to add.
        """
        self._add(user_obj)
        self.user_ids.append(user_obj.id)

    def add_guild(self, guild_obj: Guild):
        """
        Adds a guild object to the cache.

        Parameters
        ----------
        guild_obj: :type:`Guild`
            The guild object to add.
        """
        self._add(guild_obj)
        self.guild_ids.append(guild_obj.id)

    def remove(self, id: Snowflake):
        """
        Removes an object from the cache with the provided id.

        Parameters
        ----------
        id: :type:`Snowflake`
            The id of the object to remove.
        """
        del self._obj_cache[id]

    def modify(self, obj: Any):
        """
        Modifies an object from the cache by removing then adding it back.

        Parameters
        ----------
        obj: :type:`Any`
            The modified object.
        """
        # the obj variable is expected to be mixed in with the Snowflake Mixin
        if not hasattr(obj, "id"):
            raise ValueError("obj is expected to have id attribute")

        self.remove(obj.id)
        self._add(obj)