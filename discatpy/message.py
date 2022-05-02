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

from .types.snowflake import Snowflake
from .types.message import *
from .abs import APIType
from .embed import Embed
from .mixins import SnowflakeMixin
from .user import User

class Message(APIType, SnowflakeMixin):
    """
    Represents a message in a Text Channel (guild and DM). This shouldn't be 
    initalized manually, the rest of the API should take care of that for you.

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
    webhook_author: :type:`Dict[str, Any]`
        The author of this message, if it was sent by a webhook
    is_author_webhook: :type:`bool`
        Whether or not this message was sent by a webhook
    content: :type:`str`
        The content of this message
    timestamp: :type:`datetime`
        The timestamp of this message
    edited_timestamp: :type:`datetime`
        The timestamp of the last edit of this message, if applicable
    tts: :type:`bool`
        Whether or not this message was sent with text-to-speech
    mention_everyone: :type:`bool`
        Whether or not this message mentions everyone
    embeds: :type:`List[Embed]`
        The embeds in this message
    reactions: :type:`List[Reaction]`
        The reactions on this message
    pinned: :type:`bool`
        Whether or not this message is pinned
    type: :type:`int`
        The type of this message
    activity: :type:`MessageActivity`
        The activity of this message
    message_reference: :type:`MessageReference`
        The message reference of this message
    flags: :type:`int`
        The flags of this message
    referenced_message: :type:`Message`
        The referenced message of this message
    """
    def __init__(
        self,
        d: Dict[str, Any],
        client,
        id: Snowflake,
        channel_id: Snowflake,
        guild_id: Optional[Snowflake],
        author: Optional[User],
        webhook_author: Optional[Dict[str, Any]],
        is_author_webhook: bool,
        content: str,
        timestamp: datetime,
        edited_timestamp: Optional[datetime],
        tts: bool,
        mention_everyone: bool,
        embeds: List[Embed],
        reactions: List[Reaction],
        pinned: bool,
        type: int,
        activity: MessageActivity,
        message_reference: Optional[MessageReference],
        flags: Optional[int],
        referenced_message: Optional[Any], # this is supposed to be of Message type
    ) -> None:
        super().__init__(d, client)

        self.raw_id = id
        self.channel_id = channel_id
        self.channel = None # initalized later by the cache
        self.guild_id = guild_id
        self.guild = None # initalized later by the cache
        self.author = author
        self.webhook_author = webhook_author
        self.is_author_webhook = is_author_webhook
        self.content = content
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.tts = tts
        self.mention_everyone = mention_everyone
        self.embeds = embeds
        self.reactions = reactions
        self.pinned = pinned
        self.type = type
        self.activity = activity
        self.message_reference = message_reference
        self.flags = flags

        if isinstance(referenced_message, Message) or referenced_message is None:
            self.referenced_message = referenced_message
        else:
            raise TypeError(f"referenced_message should be of type Message, not {type(referenced_message)}")

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        channel_id: Snowflake = d.get("channel_id")
        guild_id: Optional[Snowflake] = d.get("guild_id")
        raw_author: Dict[str, Any] = d.get("author")
        author: Optional[User] = User.from_dict(raw_author) if raw_author.get("webhook_id") is None else None
        webhook_author: Optional[Dict[str, Any]] = raw_author if raw_author.get("webhook_id") is not None else None
        is_author_webhook: bool = webhook_author is not None
        # TODO: member attribute
        content: str = d.get("content")
        timestamp: datetime = datetime.fromisoformat(d.get("timestamp"))
        edited_timestamp: Optional[datetime] = datetime.fromisoformat(d.get("edited_timestamp")) if d.get("edited_timestamp") is not None else None
        tts: bool = d.get("tts")
        mention_everyone: bool = d.get("mention_everyone")
        # TODO: mentions, attachments
        embeds: List[Embed] = [Embed.from_dict(e) for e in d.get("embeds")] if d.get("embeds") is not None else []
        reactions: List[Reaction] = [to_reaction(r) for r in d.get("reactions")] if d.get("reactions") is not None else []
        pinned: bool = d.get("pinned")
        type: int = d.get("type")
        # TODO: application, application_id
        activity: MessageActivity = to_message_activity(d.get("activity"))
        message_reference: Optional[MessageReference] = to_message_reference(d.get("message_reference")) if d.get("message_reference") is not None else None
        flags: Optional[int] = d.get("flags")
        referenced_message: Optional[Message] = cls.from_dict(d.get("referenced_message")) if d.get("referenced_message") is not None else None
        # TODO: interaction & components, thread, sticker_items

        return cls(
            d,
            client,
            id, 
            channel_id, 
            guild_id, 
            author, 
            webhook_author, 
            is_author_webhook, 
            content, 
            timestamp, 
            edited_timestamp, 
            tts, 
            mention_everyone, 
            embeds, 
            reactions, 
            pinned, 
            type, 
            activity, 
            message_reference, 
            flags, 
            referenced_message
        )

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
        message_reference = MessageReference()
        message_reference.message_id = self.id
        # to validify the message reference
        message_reference.channel_id = self.channel_id
        message_reference.guild_id = self.guild_id

        await self.client.http.send_message(
            self.channel_id,
            content,
            embed=embed,
            embeds=embeds,
            msg_reference=message_reference,
            tts=tts
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
        await self.client.http.edit_message(
            self.id,
            self.channel_id,
            content,
            embed=embed,
            embeds=embeds,
        )

    async def pin(self):
        """
        Pins this message.
        """
        await self.client.http.pin_message(self.id, self.channel_id)

    async def unpin(self):
        """
        Unpins this message.
        """
        await self.client.http.unpin_message(self.id, self.channel_id)