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
from typing import TYPE_CHECKING, List, Optional, Union, cast

from discord_typings import (
    GuildMemberData,
    MessageActivityData,
    MessageData,
    MessageReactionData,
    MessageReferenceData,
)
from typing_extensions import Literal, NotRequired, TypedDict

from .enums.channel import ChannelType
from .object import DiscordObject
from .types.snowflake import *
from .user import User
from .utils import MISSING, MissingType

if TYPE_CHECKING:
    from .channel import GuildChannel, RawChannel
    from .embed import Embed
    from .guild import Guild, GuildMember

__all__ = (
    "MessageActivityData",
    "Message",
)


class Message(DiscordObject):
    """
    Represents a message in a Text Channel (guild and DM).

    Attributes
    ----------
    id: :type:`Snowflake`
        The id of this message
    channel_id: :type:`Snowflake`
        The id of the channel this message was sent in
    guild_id: :type:`Snowflake`
        The id of the guild this message was sent in, if applicable
    author: :type:`User`
        The author of this message
    member: :type:`Optional[GuildMember]`
        The member who sent this message, if it's in a guild
    content: :type:`str`
        The content of this message
    timestamp: :type:`datetime`
        The timestamp of this message
    edited_timestamp: :type:`Optional[datetime]`
        The timestamp of the last edit of this message, if applicable
    tts: :type:`bool`
        Whether or not this message was sent with text-to-speech
    mention_everyone: :type:`bool`
        Whether or not this message mentions everyone
    embeds: :type:`List[Embed]`
        The embeds in this message
    reactions: :type:`List[MessageReactionData]`
        The reactions on this message
    pinned: :type:`bool`
        Whether or not this message is pinned
    type: :type:`int`
        The type of this message
    activity: :type:`MessageActivityData`
        The activity of this message
    message_reference: :type:`MessageReferenceData`
        The message reference of this message
    flags: :type:`int`
        The flags of this message
    referenced_message: :type:`Message`
        The referenced message of this message
    """

    __slots__ = (
        "channel",
        "guild",
        "member",
        "id",
        "author",
        "content",
        "timestamp",
        "edited_timestamp",
        "tts",
        "mention_everyone",
        "reactions",
        "pinned",
        "type",
        "activity",
        "message_reference",
        "flags",
        "referenced_message",
    )

    def __init__(self, d: MessageData, client):
        DiscordObject.__init__(self, d, client)

        self.channel: Optional[Union[RawChannel, GuildChannel]] = None
        self.guild: Optional[Guild] = None
        self.member: Optional[GuildMember] = None
        self._update(d)

    def _update(self, d: MessageData):
        self.id: Snowflake = d.get("id")
        self._channel_id: Snowflake = d.get("channel_id")
        self._guild_id: Optional[Snowflake] = d.get("guild_id")
        self.author: User = User.from_dict(self.client, d.get("author"))
        self._member: Optional[GuildMemberData] = d.get("member")
        self.content: str = d.get("content")
        self.timestamp: datetime = datetime.fromisoformat(d.get("timestamp"))
        self.edited_timestamp: Optional[datetime] = (
            datetime.fromisoformat(d.get("edited_timestamp"))
            if d.get("edited_timestamp") is not None
            else None
        )
        self.tts: bool = d.get("tts")
        self.mention_everyone: bool = d.get("mention_everyone")
        # TODO: mentions, attachments, embeds
        self.reactions: Union[MissingType, List[MessageReactionData]] = (
            [cast(r, MessageReactionData) for r in d.get("reactions")]
            if d.get("reactions", MISSING) is not MISSING
            else MISSING
        )
        self.pinned: bool = d.get("pinned")
        self.type: int = d.get("type")
        # TODO: application, application_id
        self.activity: Union[MissingType, MessageActivityData] = (
            cast(d.get("activity"), MessageActivityData)
            if d.get("activity", MISSING) is not MISSING
            else MISSING
        )
        self.message_reference: Union[MissingType, MessageReferenceData] = (
            cast(d.get("message_reference"), MessageReferenceData)
            if d.get("message_reference", MISSING) is not MISSING
            else MISSING
        )
        self.flags: Union[MissingType, int] = d.get("flags", MISSING)
        raw_referenced_message: Union[MissingType, Optional[MessageData]] = d.get(
            "referenced_message", MISSING
        )
        self.referenced_message: Union[MissingType, Optional[Message]] = MISSING
        if raw_referenced_message is not MISSING:
            self.referenced_message = (
                Message(raw_referenced_message, self.client)
                if raw_referenced_message is not None
                else None
            )
        # TODO: interactions, thread, sticker_items

    def _set_channel(self, new_channel: Union[RawChannel, GuildChannel]):
        self.channel = new_channel

        if self.channel.type not in (ChannelType.DM, ChannelType.GROUP_DM):
            self.guild = self.channel.guild  # type: ignore

    def _set_member(self, new_member: GuildMember):
        if self.guild:
            self.member = new_member

    async def reply(
        self,
        content: str,
        /,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: bool = False,
        # TODO: components, stickers, files/attachments
    ):
        """
        Sends a reply message to this message.

        Parameters
        ----------
        content: :type:`str`
            The content of the reply
        embed: :type:`Embed`
            The embed of the reply. You cannot specify both this and embeds.
        embeds: :type:`List[Embed]`
            The embeds of the reply. You cannot specify both this and embed.
        tts: :type:`bool`
            Whether or not the reply should be TTS
        """
        message_reference = MessageReferenceData(message_id=self.id, channel_id=self._channel_id)

        if self._guild_id:
            message_reference["guild_id"] = self._guild_id

        await self.client.http.send_message(
            self._channel_id,
            content,
            embed=embed,
            embeds=embeds,
            msg_reference=message_reference,
            tts=tts,
        )

    async def edit(
        self,
        content: str,
        /,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        # TODO: components, stickers, files/attachments
    ):
        """
        Edits this message.

        Parameters
        ----------
        content: str
            The new content of the message.
        embed: Optional[Embed]
            The new embed of the message.
        embeds: Optional[List[Embed]]
            The new embeds of the message.
        """
        self.content = content

        if embed and embeds:
            raise ValueError("Cannot specify both embed and embeds!")

        if embed:
            self.embeds = [embed]

        if embeds:
            self.embeds = embeds

        await self.client.http.edit_message(
            self.id,
            self._channel_id,
            content,
            embed=embed,
            embeds=embeds,
        )

    async def pin(self):
        """Pins this message."""
        await self.client.http.pin_message(self.id, self._channel_id)
        self.pinned = True

    async def unpin(self):
        """Unpins this message."""
        await self.client.http.unpin_message(self.id, self._channel_id)
        self.pinned = False

    async def pin_or_unpin(self):
        """Pins or unpins this message depending if it's already been pinned or not."""
        if self.pinned:
            await self.unpin()
        else:
            await self.pin()

    async def crosspost(self):
        """Crossposts this message to following channels of the parent News Channel."""
        if self.channel is not None:
            if self.channel.type != ChannelType.GUILD_NEWS:
                raise TypeError(
                    "Parent channel of this message must be a News Channel to crosspost!"
                )

            await self.client.http.crosspost_message(self._channel_id, self.id)
