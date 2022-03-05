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

from typing import Any, Dict, List, Optional

from .types.channel import ChannelOverwrite, ChannelType
from .types.snowflake import *
from .abs import APIType
from .mixins import SnowflakeMixin

class RawChannel(APIType, SnowflakeMixin):
    """
    Represents the base for all channel types. Do not implement this yourself,
    instead use `TextChannel`, `VoiceChannel`, or `Thread`.

    Attributes
    ----------
    id: :type:`Snowflake`
        The id of this channel
    type: :type:`int`
        The type of this channel. Look at the `ChannelType` enum to see what
        numbers mean what.
    """
    type: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        type: int = d.get("type")

        ret_cls = cls()
        ret_cls.raw_id = id
        ret_cls.type = type
        return ret_cls

class GuildChannel(RawChannel):
    """
    Represents the base for channels in a guild. Do not implement this
    yourself, instead use `TextChannel`, `VoiceChannel`, or `Thread`.

    This is a child of `RawChannel`.

    Parameters
    ----------
    d: :type:`Dict[str, Any]`
        The dictionary from the Discord API that represents this 
        channel. 
        
        This is passed in in order to initalize the 
        type with the `RawChannel.from_dict()` function

    Attributes
    ----------
    guild_id: :type:`Snowflake`
        The id of the guild that owns this channel
    name: :type:`str`
        The name of this channel
    position: :type:`int`
        Where this channel is placed
    nsfw: :type:`bool`
        Whether or not this channel is NSFW (not safe for work).
        Discord might call this "age restricted" or something similar
    permission_overwrites: :type:`List[ChannelOverwrite]`
        The permission overwrites for this channel
    """
    def __init__(
        self, 
        d: Dict[str, Any],
        guild_id: Snowflake,
        name: str,
        position: int,
        nsfw: bool,
        permission_overwrites: List[ChannelOverwrite]
    ) -> None:
        self = RawChannel.from_dict(d)

        if self.type == ChannelType.DM or self.type == ChannelType.GROUP_DM:
            # TODO: Rephase this to be clearer
            raise TypeError("Expecting GuildChannel, got DMChannel instead")

        self.guild_id = guild_id
        self.name = name
        self.position = position
        self.nsfw = nsfw
        self.permission_overwrites = permission_overwrites

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        guild_id: Snowflake = d.get("guild_id")
        name: str = d.get("name")
        position: int = d.get("position")
        nsfw: bool = d.get("nsfw")
        raw_perm_ows: List[Dict[str, Any]] = d.get("permission_overwrites")
        permission_overwrites: List[ChannelOverwrite] = []

        for i in raw_perm_ows:
            id: Snowflake = i.get("id")
            type: int = i.get("type")
            allow: str = i.get("allow")
            deny: str = i.get("deny")

            overwrite = ChannelOverwrite()
            overwrite.id = id
            overwrite.type = type
            overwrite.allow = allow
            overwrite.deny = deny

            permission_overwrites.append(overwrite)

        return cls(d, guild_id, name, position, nsfw, permission_overwrites)

    @property
    def mention(self) -> Optional[str]:
        """
        Returns a string that can mention this Guild Channel.

        This does type checking to make sure the Guild Channel is not
        a voice or stage channel.
        """
        if self.type == ChannelType.GUILD_VOICE or self.type == ChannelType.GUILD_STAGE_VOICE:
            return None

        return f"<#{self.id}>"

