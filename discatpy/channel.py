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
from datetime import datetime

from .types.channel import ChannelOverwrite, ChannelType, to_channel_overwrite
from .types.snowflake import *
from .abs import APIType, Messageable
from .mixins import SnowflakeMixin

class RawChannel(APIType, SnowflakeMixin):
    """
    Represents the base for all channel types. Do not implement this yourself,
    instead use `TextChannel`, `VoiceChannel`, `DMChannel`, or `Thread`.

    Attributes
    ----------
    type: :type:`int`
        The type of this channel. Look at the `ChannelType` enum to see what the
        valid values are.
    """
    def __init__(self, d: Dict[str, Any], client, id: Snowflake, type: int):
        super().__init__(d, client)
        self.raw_id = id
        self.type = type

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        type: int = d.get("type")

        return cls(d, client, id, type)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = {
            "id": self.id,
            "type": self.type
        }
        return ret_dict

class GuildChannel(RawChannel):
    """
    Represents the base for channels in a guild. Do not implement this
    yourself, instead use :class:`TextChannel`, :class:`VoiceChannel`, 
    or :class:`Thread`.

    This is a child of :class:`RawChannel`.

    Parameters
    ----------
    d: :type:`Dict[str, Any]`
        The dictionary from the Discord API that represents this 
        channel. 
        
        This is passed in in order to initalize the 
        type with the :meth:`RawChannel.from_dict()` function

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
        client,
        guild_id: Snowflake,
        name: str,
        position: int,
        nsfw: bool,
        permission_overwrites: List[ChannelOverwrite],
        parent_id: Snowflake
    ) -> None:
        self = RawChannel.from_dict(client, d)

        if self.type == ChannelType.DM or self.type == ChannelType.GROUP_DM:
            raise TypeError("Expecting Guild channel type, got DM channel type instead")

        self.guild_id = guild_id
        self.name = name
        self.position = position
        self.nsfw = nsfw
        self.permission_overwrites = permission_overwrites
        self.parent_id = parent_id

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        guild_id: Snowflake = d.get("guild_id")
        name: str = d.get("name")
        position: int = d.get("position")
        nsfw: bool = d.get("nsfw", False)
        permission_overwrites: List[ChannelOverwrite] = [to_channel_overwrite(i) for i in d.get("permission_overwrites")] if d.get("permission_overwrites") is not None else []
        parent_id = d.get("parent_id")

        return cls(d, client, guild_id, name, position, nsfw, permission_overwrites, parent_id)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = RawChannel.to_dict()
        ret_dict.update({
            "guild_id": self.guild_id,
            "name": self.name,
            "position": self.position,
            "nsfw": self.nsfw,
            "parent_id": self.parent_id
        })

        if self.permission_overwrites:
            ret_dict["permission_overwrites"] = self.permission_overwrites

        return ret_dict

    @property
    def mention(self) -> Optional[str]:
        """
        Returns a string that can mention this Guild Channel.
        """
        return f"<#{self.id}>"

class TextChannel(GuildChannel, Messageable):
    """
    Represents a text channel used in a guild.

    This is a child of both :class:`GuildChannel` and :class:`Messageable`.

    Parameters
    ----------
    d: :type:`Dict[str, Any]`
        The dictionary from the Discord API that represents this 
        channel. 
        
        This is passed in in order to initalize the 
        type with the :meth:`GuildChannel.from_dict()` function

    Attributes
    ----------
    topic: :type:`Optional[str]`
        The topic of this text channel
    cooldown: :type:`int`
        The cooldown or rate limit per user of this text channel
    last_message_id: :type:`Optional[Snowflake]`
        The id of the last message sent in this text channel
    last_pin_timestamp: :type:`Optional[datetime]`
        The time of the last pin in this text channel
    permissions: :type:`Optional[str]`
        The permissions for the invoking user in this text channel.
        This is only set for slash command interactions
    """
    def __init__(
        self,
        d: Dict[str, Any],
        client,
        topic: Optional[str],
        cooldown: int,
        last_message_id: Optional[Snowflake],
        last_pin_timestamp: Optional[datetime],
        permissions: Optional[str]
    ) -> None:
        self = GuildChannel.from_dict(client, d)

        self.channel_id = self.raw_id
        self.topic = topic
        self.cooldown = cooldown
        self.last_message_id = last_message_id
        self.last_pin_timestamp = last_pin_timestamp
        self.permissions = permissions

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        topic: Optional[str] = d.get("topic")
        cooldown: int = d.get("rate_limit_per_user", 0)
        last_message_id: Optional[Snowflake] = d.get("last_message_id")
        last_pin_timestamp: Optional[datetime] = datetime.fromisoformat(d.get("last_pin_timestamp")) if d.get("last_pin_timestamp") is not None else None
        permissions: Optional[str] = d.get("permissions")

        return cls(d, client, topic, cooldown, last_message_id, last_pin_timestamp, permissions)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = GuildChannel.to_dict()
        ret_dict.update({
            "rate_limit_per_user": self.cooldown
        })

        if self.topic:
            ret_dict["topic"] = self.topic

        return ret_dict

    async def edit(
        self,
        /,
        name: Optional[str] = None,
        type: Optional[int] = None,
        position: Optional[int] = None,
        topic: Optional[str] = None,
        nsfw: Optional[bool] = None,
        cooldown: Optional[int] = None,
        permission_overwrites: Optional[List[ChannelOverwrite]] = None,
        parent_id: Optional[Snowflake] = None
    ):
        if name:
            self.name = name

        if type:
            if not (type == ChannelType.GUILD_TEXT or type == ChannelType.GUILD_NEWS):
                raise TypeError("You cannot convert a Text Channel to any other channel besides a News Channel!")
            self.type = type

        if position:
            self.position = position

        if topic:
            self.topic = topic

        # ensure we aren't actually comparing the bool and instead comparing if it's None
        if nsfw is not None:
            self.nsfw = nsfw

        if cooldown:
            self.cooldown = cooldown

        if permission_overwrites:
            self.permission_overwrites = permission_overwrites

        if parent_id:
            self.parent_id = parent_id

        await self.client.http.modify_channel(self.id, self.to_dict())

class VoiceChannel(GuildChannel):
    """
    Represents a voice channel used in a guild.

    This is a child of :class:`GuildChannel`.

    Parameters
    ----------
    d: :type:`Dict[str, Any]`
        The dictionary from the Discord API that represents this 
        channel. 
        
        This is passed in in order to initalize the 
        type with the :meth:`GuildChannel.from_dict()` function

    Attributes
    ----------
    bitrate: :type:`int`
        The bitrate of this voice channel
    user_limit: :type:`int`
        The user limit of this voice channel
    rtc_region: :type:`Optional[str]`
        The region of this voice channel
    automatic_rtc_region: :type:`bool`
        Whether or not this voice channel has automatic regions
    video_quality_mode: :type:`int`
        The video quality of this voice channel
    """
    def __init__(
        self, 
        d: Dict[str, Any], 
        client, 
        bitrate: int,
        user_limit: int,
        rtc_region: Optional[str],
        automatic_rtc_region: bool,
        video_quality_mode: int
    ):
        self = GuildChannel.from_dict(client, d)

        self.bitrate = bitrate
        self.user_limit = user_limit
        self.rtc_region = rtc_region
        self.automatic_rtc_region = automatic_rtc_region
        self.video_quality_mode = video_quality_mode

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        bitrate: int = d.get("bitrate")
        user_limit: int = d.get("user_limit")
        rtc_region: Optional[str] = d.get("rtc_region")
        automatic_rtc_region: bool = rtc_region is None
        video_quality_mode: int = d.get("video_quality_mode", 1)

        return cls(d, client, bitrate, user_limit, rtc_region, automatic_rtc_region, video_quality_mode)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = GuildChannel.to_dict()
        ret_dict.update({
            "bitrate": self.bitrate,
            "user_limit": self.user_limit,
            "rtc_region": self.rtc_region,
            "video_quality_mode": self.video_quality_mode
        })

        return ret_dict

    async def edit(
        self, 
        /, 
        name: Optional[str] = None, 
        position: Optional[int] = None, 
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        permission_overwrites: Optional[List[ChannelOverwrite]] = None,
        parent_id: Optional[Snowflake] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[int] = None
    ):
        if name:
            self.name = name

        if position:
            self.position = position

        if bitrate:
            self.bitrate = bitrate

        if user_limit:
            self.user_limit = user_limit

        if permission_overwrites:
            self.permission_overwrites = permission_overwrites

        if parent_id:
            self.parent_id = parent_id

        if rtc_region:
            self.rtc_region = rtc_region

        if video_quality_mode:
            self.video_quality_mode = video_quality_mode

        await self.client.http.modify_channel(self.id, self.to_dict())