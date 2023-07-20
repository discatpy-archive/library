# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from datetime import datetime
from enum import Enum

import attr
import discord_typings as dt
from discatcore import BasicFile
from discatcore.types import Unset, UnsetOr
from discatcore.utils import Snowflake

from ..flags import Flag, flag
from ..utils.attr_exts import ToDictMixin
from .embed import Embed
from .user import User

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = (
    "AllowedMentions",
    "MessageReference",
    "Attachment",
    "MessageTypes",
    "MessageFlags",
    "Message",
)


@attr.define(kw_only=True)
class AllowedMentions(ToDictMixin[dt.AllowedMentionsData]):
    parse: list[t.Literal["roles", "users", "everyone"]]
    roles: t.Optional[list[dt.Snowflake]] = None
    users: t.Optional[list[dt.Snowflake]] = None
    replied_user: t.Optional[bool] = None


@attr.define(kw_only=True)
class MessageReference(ToDictMixin[dt.MessageReferenceData]):
    message_id: t.Optional[dt.Snowflake] = None
    channel_id: t.Optional[dt.Snowflake] = None
    guild_id: t.Optional[dt.Snowflake] = None
    fail_if_not_exists: bool = True

    @classmethod
    def from_dict(cls, data: dt.MessageReferenceData):
        return cls(**data)


class Attachment:
    def __init__(self, *, bot: Bot, data: dt.AttachmentData):
        self.bot: Bot = bot
        self.data: dt.AttachmentData = data

        self.id: Snowflake = Snowflake(self.data["id"])
        self.filename: str = self.data["filename"]
        self.description: UnsetOr[str] = self.data.get("description", Unset)
        self.content_type: UnsetOr[str] = self.data.get("content_type", Unset)
        self.size: int = self.data["size"]
        self.url: str = self.data["url"]
        self.proxy_url: str = self.data["proxy_url"]
        self.height: UnsetOr[t.Optional[int]] = self.data.get("height", Unset)
        self.width: UnsetOr[t.Optional[int]] = self.data.get("width", Unset)
        self.ephemeral: bool = self.data.get("ephemeral", False)

    async def read(self, *, proxied: bool = False):
        url = self.proxy_url if proxied else self.url
        return await self.bot.http.get_from_cdn(url)


class MessageTypes(int, Enum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24


class MessageFlags(Flag):
    if t.TYPE_CHECKING:

        def __init__(
            self,
            *,
            crossposted: bool = ...,
            is_crosspost: bool = ...,
            suppress_embeds: bool = ...,
            source_message_deleted: bool = ...,
            urgent: bool = ...,
            has_thread: bool = ...,
            ephemeral: bool = ...,
            loading: bool = ...,
            failed_to_mention_some_roles_in_thread: bool = ...,
        ):
            ...

    @flag
    def CROSSPOSTED():
        return 1 << 0

    @flag
    def IS_CROSSPOST():
        return 1 << 1

    @flag
    def SUPPRESS_EMBEDS():
        return 1 << 2

    @flag
    def SOURCE_MESSAGE_DELETED():
        return 1 << 3

    @flag
    def URGENT():
        return 1 << 4

    @flag
    def HAS_THREAD():
        return 1 << 5

    @flag
    def EPHEMERAL():
        return 1 << 6

    @flag
    def LOADING():
        return 1 << 7

    @flag
    def FAILED_TO_MENTION_SOME_ROLES_IN_THREAD():
        return 1 << 8


def _parse_files_to_attachments(files: list[BasicFile]):
    generated_attachments: list[dt.PartialAttachmentData] = []
    for i, file in enumerate(files):
        generated_attachments.append(dt.PartialAttachmentData(id=i, filename=file.filename))
    return generated_attachments


# this is internal and it's intended to not repeat the whole message parameter validation process
# TODO: move to a more appropriate file (maybe a utils file)
def _send_message(
    content: UnsetOr[str],
    nonce: UnsetOr[t.Union[int, str]],
    tts: bool,
    embeds: UnsetOr[list[Embed]],
    allowed_mentions: UnsetOr[AllowedMentions],
    message_reference: UnsetOr[MessageReference],
    # TODO: components
    stickers: UnsetOr[list[dt.Snowflake]],
    files: UnsetOr[list[BasicFile]],
    flags: UnsetOr[t.Union[MessageFlags, int]],
):
    if isinstance(flags, MessageFlags):
        flags = flags.value

    if content is Unset and embeds is Unset and stickers is Unset and files is Unset:
        raise ValueError("At least one of content, embeds, stickers, and files are required!")

    generated_attachments: UnsetOr[list[dt.PartialAttachmentData]] = Unset
    if files is not Unset:
        generated_attachments = _parse_files_to_attachments(files)

    processed_embeds: UnsetOr[list[dt.EmbedData]] = Unset
    if embeds is not Unset:
        processed_embeds = [e.to_dict() for e in embeds]

    processed_allowed_mentions: UnsetOr[dt.AllowedMentionsData] = Unset
    if allowed_mentions is not Unset:
        processed_allowed_mentions = allowed_mentions.to_dict()

    processed_message_reference: UnsetOr[dt.MessageReferenceData] = Unset
    if message_reference is not Unset:
        processed_message_reference = message_reference.to_dict()

    return {
        "content": content,
        "nonce": nonce,
        "tts": tts,
        "embeds": processed_embeds,
        "allowed_mentions": processed_allowed_mentions,
        "message_reference": processed_message_reference,
        "sticker_ids": stickers,
        "attachments": generated_attachments,
        "files": files,
        "flags": flags,
    }


class Message:
    def __init__(self, *, bot: Bot, data: dt.MessageData):
        self.bot: Bot = bot
        self.data: dt.MessageData = data
        # TODO: channel, guild

        self.id: Snowflake = Snowflake(self.data["id"])
        self.channel_id: Snowflake = Snowflake(self.data["channel_id"])
        # TODO: attempt to get user object from cache
        self.author: User = User(bot=self.bot, data=self.data["author"])
        self.content: UnsetOr[str] = self.data.get("content", Unset)
        self.timestamp: datetime = datetime.fromisoformat(self.data["timestamp"])

        self.edited_timestamp: t.Optional[datetime]
        raw_edited_timestamp = self.data.get("edited_timestamp")
        if isinstance(raw_edited_timestamp, str):
            self.edited_timestamp = datetime.fromisoformat(raw_edited_timestamp)
        else:
            self.edited_timestamp = raw_edited_timestamp

        self.tts: bool = self.data["tts"]
        self.mentions: list[User] = [User(bot=self.bot, data=d) for d in self.data["mentions"]]
        self.attachments: UnsetOr[list[Attachment]] = [
            Attachment(bot=self.bot, data=a) for a in self.data["attachments"]
        ]
        self.embeds: UnsetOr[list[Embed]] = [
            Embed.from_dict(d) for d in self.data["embeds"]
        ] or Unset
        self.nonce: UnsetOr[t.Union[int, str]] = self.data.get("nonce", Unset)
        self.pinned: bool = self.data["pinned"]
        self.webhook_id: UnsetOr[dt.Snowflake] = self.data.get("webhook_id", Unset)
        self.type: MessageTypes = MessageTypes(self.data["type"])
        # TODO: activity, application
        self.application_id: UnsetOr[dt.Snowflake] = self.data.get("application_id", Unset)

        self.message_reference: UnsetOr[MessageReference]
        raw_message_reference = self.data.get("message_reference", Unset)
        if isinstance(raw_message_reference, dt.MessageReferenceData):
            self.message_reference = MessageReference.from_dict(raw_message_reference)
        else:
            self.message_reference = raw_message_reference

        self.flags: UnsetOr[MessageFlags]
        raw_flags = self.data.get("flags", Unset)
        if isinstance(raw_flags, int):
            self.flags = MessageFlags.from_value(raw_flags)
        else:
            self.flags = raw_flags

        self.referenced_message: UnsetOr[t.Optional[Message]]
        raw_referenced_message = self.data.get("referenced_message", Unset)
        if isinstance(raw_referenced_message, (dt.ChannelMessageData, dt.GuildMessageData)):
            # TODO: attempt to get message object from cache
            self.referenced_message = Message(bot=self.bot, data=raw_referenced_message)
        else:
            self.referenced_message = raw_referenced_message

        # TODO: interaction, thread, components, sticker_items, stickers

    async def edit(
        self,
        *,
        content: UnsetOr[t.Optional[str]] = Unset,
        embeds: UnsetOr[t.Optional[list[Embed]]] = Unset,
        flags: UnsetOr[t.Optional[t.Union[int, MessageFlags]]] = Unset,
        allowed_mentions: UnsetOr[t.Optional[AllowedMentions]] = Unset,
        # TODO: components
        files: UnsetOr[t.Optional[list[BasicFile]]] = Unset,
    ):
        if isinstance(flags, MessageFlags):
            flags = flags.value

        kwargs: dict[str, t.Any] = {
            "content": content,
            "flags": flags,
            "files": files,
        }

        if embeds is not Unset and embeds is not None:
            kwargs["embeds"] = [e.to_dict() for e in embeds]

        if allowed_mentions is not Unset and allowed_mentions is not None:
            kwargs["allowed_mentions"] = allowed_mentions.to_dict()

        if files is not Unset and files is not None:
            kwargs["attachments"] = _parse_files_to_attachments(files)

        new_msg_data = t.cast(
            dt.MessageData, await self.bot.http.edit_message(self.channel_id, self.id, **kwargs)
        )
        new_msg = Message(bot=self.bot, data=new_msg_data)
        # TODO: edit cache
        return new_msg

    async def reply(
        self,
        content: UnsetOr[str] = Unset,
        *,
        nonce: UnsetOr[t.Union[int, str]] = Unset,
        tts: bool = False,
        embeds: UnsetOr[list[Embed]] = Unset,
        allowed_mentions: UnsetOr[AllowedMentions] = Unset,
        # TODO: components
        stickers: UnsetOr[list[dt.Snowflake]] = Unset,
        files: UnsetOr[list[BasicFile]] = Unset,
        flags: UnsetOr[t.Union[MessageFlags, int]] = Unset,
    ):
        msg_reference = MessageReference(message_id=self.id, channel_id=self.channel_id)
        return await self.bot.http.create_message(
            self.channel_id,
            **_send_message(
                content, nonce, tts, embeds, allowed_mentions, msg_reference, stickers, files, flags
            ),
        )

    async def pin(self, *, reason: t.Optional[str] = None):
        await self.bot.http.pin_message(self.channel_id, self.id, reason)

    async def unpin(self, *, reason: t.Optional[str] = None):
        await self.bot.http.unpin_message(self.channel_id, self.id, reason)
