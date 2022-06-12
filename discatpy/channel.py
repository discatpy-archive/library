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

from typing import Any, Dict, List, Optional, overload, TYPE_CHECKING
from datetime import datetime

from .types.channel import ChannelOverwrite, ChannelType, to_channel_overwrite
from .types.snowflake import *
from .abs import Messageable
from .mixins import SnowflakeMixin
from .object import DiscordObject
from .user import User

if TYPE_CHECKING:
    from .guild import Guild

__all__ = (
    "RawChannel",
    "GuildChannel",
    "DMChannel",
    "TextChannel",
    "VoiceChannel",
)

def _convert_dict_to_channel(client, channel_dict: Dict[str, Any]):
    channel_type = channel_dict.get("type")

    if channel_type == ChannelType.DM:
        return DMChannel.from_dict(client, channel_dict)
    elif channel_type == ChannelType.GUILD_TEXT or channel_type == ChannelType.GUILD_NEWS:
        return TextChannel.from_dict(client, channel_dict)
    elif channel_type == ChannelType.GUILD_VOICE or channel_type == ChannelType.GUILD_STAGE_VOICE:
        return VoiceChannel.from_dict(client, channel_dict)

    raise TypeError("Invalid channel dict provided")

class RawChannel(DiscordObject, SnowflakeMixin):
    """
    Represents the base for all channel types. 
    
    Do not implement this yourself, instead use :class:`TextChannel`, 
    :class:`VoiceChannel`, :class:`DMChannel`, or :class:`Thread`.

    Attributes
    ----------
    type: :type:`int`
        The type of this channel. Look at the `ChannelType` enum to see what the
        valid values are.
    """
    def __init__(self, d: Dict[str, Any], client):
        DiscordObject.__init__(self, d, client)
        self.raw_id = d.get("id")
        self.type: int = d.get("type")

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
    if TYPE_CHECKING:
        guild: Guild
        parent: "GuildChannel"

    def __init__(
        self,
        d: Dict[str, Any],
        client
    ) -> None:
        RawChannel.__init__(self, d, client)

        if self.type == ChannelType.DM or self.type == ChannelType.GROUP_DM:
            raise TypeError("Expecting Guild channel type, got DM channel type instead")

        self._guild_id: Snowflake = d.get("guild_id")
        self.guild = None # initialized later by the cache
        self.name: str = d.get("name")
        self.position: int = d.get("position")
        self.nsfw: bool = d.get("nsfw", False)
        self.permission_overwrites: List[ChannelOverwrite] = [to_channel_overwrite(i) for i in d.get("permission_overwrites")] if d.get("permission_overwrites") is not None else []
        self._parent_id = d.get("parent_id")
        self.parent = None # initialized later by the cache

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = super(RawChannel, self).to_dict()
        ret_dict.update({
            "guild_id": self._guild_id,
            "name": self.name,
            "position": self.position,
            "nsfw": self.nsfw,
            "parent_id": self._parent_id
        })

        if self.permission_overwrites:
            ret_dict["permission_overwrites"] = self.permission_overwrites

        return ret_dict

    if TYPE_CHECKING:
        @overload
        def _set_guild(self, new_guild: Guild):
            ...

    def _set_guild(self, new_guild: Any):
        self.guild = new_guild

    def _set_parent(self, new_parent: "GuildChannel"):
        self.parent = new_parent

    @property
    def mention(self) -> Optional[str]:
        """
        Returns a string that can mention this Guild Channel.
        """
        return f"<#{self.id}>"

    async def move(self, /, position: int, parent: "GuildChannel | None" = None):
        """Moves this channel to a new position and/or to a new parent.

        Parameters
        ----------
        position: :type:`int`
            The position to move the channel to.
        parent: :type:`Optional[GuildChannel]`
            The new parent to move the channel to. Defaults to None.
        """
        self.position = position

        if parent:
            self._set_parent(parent)

        await self.client.http.modify_channel_positions(
            self._guild_id, 
            self.id, 
            position=position, 
            parent_id=parent.id if parent else None
        )

class DMChannel(RawChannel, Messageable):
    """
    Represents a DM channel.

    This is a child of both :class:`RawChannel` and :class:`Messageable`.

    Attributes
    ----------
    recipients: :type:`List[User]`
        The recipients of this DM.
    """
    def __init__(self, d: Dict[str, Any], client, recipient: User) -> None:
        RawChannel.__init__(self, d, client)
        self.recipient = recipient

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        recipient: User = User.from_dict(client, d.get("recipients")[0])
        return cls(d, client, recipient)

class TextChannel(GuildChannel, Messageable):
    """
    Represents a text channel used in a guild.

    This is a child of both :class:`GuildChannel` and :class:`Messageable`.

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
        GuildChannel.__init__(self, d, client)

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
        ret_dict: Dict[str, Any] = super(GuildChannel, self).to_dict()
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
        topic: Optional[str] = None,
        nsfw: Optional[bool] = None,
        cooldown: Optional[int] = None,
        permission_overwrites: Optional[List[ChannelOverwrite]] = None
    ):
        if name:
            self.name = name

        if type:
            if not (type == ChannelType.GUILD_TEXT or type == ChannelType.GUILD_NEWS):
                raise TypeError("You cannot convert a Text Channel to any other channel besides a News Channel!")
            self.type = type

        if topic:
            self.topic = topic

        # ensure we aren't actually comparing the bool and instead comparing if it's None
        if nsfw is not None:
            self.nsfw = nsfw

        if cooldown:
            self.cooldown = cooldown

        if permission_overwrites:
            self.permission_overwrites = permission_overwrites

        await self.client.http.modify_channel(self.id, self.to_dict())

class VoiceChannel(GuildChannel):
    """
    Represents a voice channel used in a guild.

    This is a child of :class:`GuildChannel`.

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
        GuildChannel.__init__(self, d, client)

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
        ret_dict: Dict[str, Any] = super(GuildChannel, self).to_dict()
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
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        permission_overwrites: Optional[List[ChannelOverwrite]] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[int] = None
    ):
        if name:
            self.name = name

        if bitrate:
            self.bitrate = bitrate

        if user_limit:
            self.user_limit = user_limit

        if permission_overwrites:
            self.permission_overwrites = permission_overwrites

        if rtc_region:
            self.rtc_region = rtc_region

        if video_quality_mode:
            self.video_quality_mode = video_quality_mode

        await self.client.http.modify_channel(self.id, self.to_dict())