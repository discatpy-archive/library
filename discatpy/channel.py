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

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union, final

from discord_typings import (
    CategoryChannelData,
    DMChannelData,
    NewsChannelData,
    PartialChannelData,
    PermissionOverwriteData,
    TextChannelData,
    VoiceChannelData,
)
from typing_extensions import NotRequired, TypedDict

from .abs import Messageable
from .enums.channel import ChannelType
from .object import DiscordObject
from .types.snowflake import *
from .user import User
from .utils import MISSING, MissingType

if TYPE_CHECKING:
    from .guild import Guild

__all__ = (
    "RawChannel",
    "GuildChannel",
    "DMChannel",
    "TextChannel",
    "VoiceChannel",
    "CategoryChannel",
)


@final
class GuildChannelData(TypedDict):
    id: Snowflake
    type: int
    guild_id: NotRequired[Snowflake]
    position: int
    permission_overwrites: List[PermissionOverwriteData]
    name: str
    nsfw: bool
    parent_id: Optional[Snowflake]


class RawChannel(DiscordObject):
    """
    Represents the base for all channel types.

    Do not implement this yourself, instead use :class:`TextChannel`,
    :class:`VoiceChannel`, :class:`DMChannel`, or :class:`Thread`.

    Attributes
    ----------
    id: :type:`Snowflake`
        The id of this channel.
    type: :type:`int`
        The type of this channel. Look at the `ChannelType` enum to see what the
        valid values are.
    """

    __slots__ = (
        "id",
        "type",
    )

    def __init__(self, d: PartialChannelData, client):
        DiscordObject.__init__(self, d, client)
        self._update(d)

    def _update(self, d: PartialChannelData):
        self.id: Snowflake = d.get("id")
        self.type: int = d.get("type")

    @classmethod
    def from_dict(cls, client, d: Union[TextChannelData, VoiceChannelData, DMChannelData]):
        """Attempts to convert a dict into a channel object.

        Parameters
        ----------
        client: :type:`Client`
            The parent client of the channel object.
        d: :type:`Union[TextChannelData, VoiceChannelData, DMChannelData]`
            The raw channel dict.
        """
        channel_type: int = d.get("type")  # type: ignore

        if channel_type == ChannelType.DM.value:
            return DMChannel(d, client)
        elif (
            channel_type == ChannelType.GUILD_TEXT.value
            or channel_type == ChannelType.GUILD_NEWS.value
        ):
            return TextChannel(d, client)
        elif (
            channel_type == ChannelType.GUILD_VOICE.value
            or channel_type == ChannelType.GUILD_STAGE_VOICE.value
        ):
            return VoiceChannel(d, client)
        # TODO: categories

        raise TypeError("Invalid channel dict provided")

    def to_dict(self) -> PartialChannelData:
        ret_dict = PartialChannelData(id=self.id, type=self.type)
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
    permission_overwrites: :type:`List[PermissionOverwriteData]`
        The permission overwrites for this channel
    """

    __slots__ = (
        "guild",
        "parent",
        "name",
        "position",
        "nsfw",
        "permission_overwrites",
    )

    def __init__(self, d: GuildChannelData, client):
        RawChannel.__init__(self, d, client)

        if self.type == ChannelType.DM.value or self.type == ChannelType.GROUP_DM.value:
            raise TypeError("Expecting Guild channel type, got DM channel type instead")

        self._guild_id: Union[MissingType, Snowflake] = d.get("guild_id", MISSING)
        self.guild: Optional[Guild] = None
        self._update(d)

    def _update(self, d: GuildChannelData):
        self.name: str = d.get("name")
        self.position: int = d.get("position")
        self.nsfw: bool = d.get("nsfw", False)
        self.permission_overwrites: List[PermissionOverwriteData] = [
            PermissionOverwriteData(i) for i in d.get("permission_overwrites")
        ]
        self._parent_id: Union[MissingType, Optional[Snowflake]] = d.get("parent_id", MISSING)
        self.parent: Optional[GuildChannel] = None

    def to_dict(self) -> GuildChannelData:
        ret_dict: GuildChannelData = super(RawChannel, self).to_dict()
        ret_dict.update(
            {
                "name": self.name,
                "position": self.position,
                "nsfw": self.nsfw,
                "permission_overwrites": self.permission_overwrites,
            }
        )

        if self._guild_id is not MISSING:
            ret_dict["guild_id"] = self._guild_id

        if self._parent_id is not MISSING and self._parent_id is not None:
            ret_dict["parent_id"] = self._parent_id

        return ret_dict

    def _set_guild(self, new_guild: Guild):
        self.guild = new_guild

    def _set_parent(self, new_parent: GuildChannel):
        self.parent = new_parent

    @property
    def mention(self) -> Optional[str]:
        """Returns a string that can mention this Guild Channel."""
        return f"<#{self.id}>"

    async def move(self, /, position: int, parent: Optional[GuildChannel] = None):
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
            parent_id=parent.id if parent is not None else None,
        )


class DMChannel(RawChannel, Messageable):
    """
    Represents a DM channel.
    This is a child of both :class:`RawChannel` and :class:`Messageable`.

    Attributes
    ----------
    """

    __slots__ = (
        "last_message_id",
        "recipients",
        "last_pin_timestamp",
    )

    def __init__(self, d: DMChannelData, client):
        RawChannel.__init__(self, d, client)
        self._update(d)

    def _update(self, d: DMChannelData):
        self.last_message_id: Optional[Snowflake] = d.get("last_message_id")
        self.recipients: List[User] = [User.from_dict(self.client, u) for u in d.get("recipients")]
        raw_last_pin_timestamp: Union[MissingType, Optional[str]] = d.get(
            "last_pin_timestamp", MISSING
        )
        self.last_pin_timestamp: Union[MissingType, Optional[datetime]] = MISSING
        if raw_last_pin_timestamp is not MISSING:
            self.last_pin_timestamp = (
                datetime.fromisoformat(raw_last_pin_timestamp)
                if raw_last_pin_timestamp is not None
                else None
            )


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

    __slots__ = (
        "topic",
        "nsfw",
        "last_message_id",
        "cooldown",
        "last_pin_timestamp",
        "default_auto_archive_duration",
    )

    def __init__(self, d: Union[TextChannelData, NewsChannelData], client):
        GuildChannel.__init__(self, d, client)
        self._update(d)

    def _update(self, d: Union[TextChannelData, NewsChannelData]):
        self.topic: Optional[str] = d.get("topic")
        self.cooldown: int = d.get("rate_limit_per_user", 0)
        self.last_message_id: Optional[Snowflake] = d.get("last_message_id")
        raw_last_pin_timestamp: Union[MissingType, Optional[str]] = d.get(
            "last_pin_timestamp", MISSING
        )
        self.last_pin_timestamp: Union[MissingType, Optional[datetime]] = MISSING
        if raw_last_pin_timestamp is not MISSING:
            self.last_pin_timestamp = (
                datetime.fromisoformat(raw_last_pin_timestamp)
                if raw_last_pin_timestamp is not None
                else None
            )
        self.permissions: Union[MissingType, str] = d.get("permissions", MISSING)

    def to_dict(self) -> Union[TextChannelData, NewsChannelData]:
        ret_dict: Union[TextChannelData, NewsChannelData] = super(GuildChannel, self).to_dict()
        ret_dict.update({"rate_limit_per_user": self.cooldown})

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
        permission_overwrites: Optional[List[PermissionOverwriteData]] = None,
    ):
        if name:
            self.name = name

        if type:
            if not (type == ChannelType.GUILD_TEXT or type == ChannelType.GUILD_NEWS):
                raise TypeError(
                    "You cannot convert a Text Channel to any other channel besides a News Channel!"
                )
            self.type = type

        if topic:
            self.topic = topic

        if nsfw is not None:
            self.nsfw = nsfw

        if cooldown:
            self.cooldown = cooldown

        if permission_overwrites:
            self.permission_overwrites = permission_overwrites

        await self.client.http.modify_channel(self.id, self.to_dict())


class VoiceChannel(GuildChannel):
    """Represents a voice channel used in a guild.
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
    video_quality_mode: :type:`Union[MissingType, int]`
        The video quality of this voice channel
    """

    __slots__ = ("bitrate", "user_limit", "rtc_region", "video_quality_mode")

    def __init__(self, d: VoiceChannelData, client):
        GuildChannel.__init__(self, d, client)
        self._update(d)

    def _update(self, d: VoiceChannelData):
        self.bitrate: int = d.get("bitrate")
        self.user_limit: int = d.get("user_limit")
        self.rtc_region: Optional[str] = d.get("rtc_region")
        self.automatic_rtc_region: bool = self.rtc_region is None
        self.video_quality_mode: Union[MissingType, int] = d.get("video_quality_mode", MISSING)

    def to_dict(self) -> VoiceChannelData:
        ret_dict: VoiceChannelData = super(GuildChannel, self).to_dict()
        ret_dict.update(
            {
                "bitrate": self.bitrate,
                "user_limit": self.user_limit,
                "rtc_region": self.rtc_region,
                "video_quality_mode": self.video_quality_mode,
            }
        )

        return ret_dict

    async def edit(
        self,
        /,
        name: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        permission_overwrites: Optional[List[PermissionOverwriteData]] = None,
        rtc_region: Optional[str] = None,
        video_quality_mode: Optional[int] = None,
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


class CategoryChannel(GuildChannel):
    """Represents a category channel used in a guild.
    This is a child of :class:`GuildChannel`.
    """

    def __init__(self, d: CategoryChannelData, client):
        GuildChannel.__init__(self, d, client)
