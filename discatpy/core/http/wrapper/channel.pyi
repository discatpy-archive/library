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

from datetime import datetime
from typing import Optional

from discord_typings import (
    AllowedMentionsData,
    AttachmentData,
    EmbedData,
    MessageReferenceData,
    PartialAttachmentData,
    PermissionOverwriteData,
)

from ...file import BasicFile
from ...types import MISSING, List, MissingOr, Snowflake

class ChannelEndpointMixin:
    async def get_channel(self, channel_id: Snowflake): ...
    async def get_guild_channels(self, guild_id: Snowflake): ...
    async def get_channel_invites(self, channel_id: Snowflake): ...
    async def create_guild_channel(
        self,
        guild_id: Snowflake,
        *,
        name: str,
        type: MissingOr[Optional[int]] = MISSING,
        topic: MissingOr[Optional[str]] = MISSING,
        bitrate: MissingOr[Optional[int]] = MISSING,
        user_limit: MissingOr[Optional[int]] = MISSING,
        rate_limit_per_user: MissingOr[Optional[int]] = MISSING,
        position: MissingOr[Optional[int]] = MISSING,
        permission_overwrites: MissingOr[Optional[List[PermissionOverwriteData]]] = MISSING,
        parent_id: MissingOr[Optional[Snowflake]] = MISSING,
        nsfw: MissingOr[Optional[bool]] = MISSING,
        rtc_region: MissingOr[Optional[str]] = MISSING,
        video_quality_mode: MissingOr[Optional[int]] = MISSING,
        default_auto_archive_duration: MissingOr[Optional[int]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def create_channel_invite(
        self,
        channel_id: Snowflake,
        *,
        max_age: int = 86400,
        max_uses: int = 0,
        temporary: bool = False,
        unique: bool = False,
        target_type: int,
        target_user_id: Snowflake,
        target_application_id: Snowflake,
        reason: Optional[str] = None,
    ): ...
    async def modify_channel(
        self,
        guild_id: Snowflake,
        *,
        name: MissingOr[Optional[str]] = MISSING,
        type: MissingOr[Optional[int]] = MISSING,
        topic: MissingOr[Optional[str]] = MISSING,
        bitrate: MissingOr[Optional[int]] = MISSING,
        user_limit: MissingOr[Optional[int]] = MISSING,
        rate_limit_per_user: MissingOr[Optional[int]] = MISSING,
        position: MissingOr[Optional[int]] = MISSING,
        permission_overwrites: MissingOr[Optional[List[PermissionOverwriteData]]] = MISSING,
        parent_id: MissingOr[Optional[Snowflake]] = MISSING,
        nsfw: MissingOr[Optional[bool]] = MISSING,
        rtc_region: MissingOr[Optional[str]] = MISSING,
        video_quality_mode: MissingOr[Optional[int]] = MISSING,
        default_auto_archive_duration: MissingOr[Optional[int]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_channel_positions(
        self,
        guild_id: Snowflake,
        *,
        id: Snowflake,
        position: Optional[int] = None,
        lock_permissions: Optional[bool] = None,
        parent_id: Optional[Snowflake] = None,
    ): ...
    async def edit_channel_permissions(
        self,
        channel_id: Snowflake,
        overwrite_id: Snowflake,
        *,
        allow: MissingOr[str] = MISSING,
        deny: MissingOr[str] = MISSING,
        type: int,
        reason: Optional[str] = None,
    ): ...
    async def delete_channel(self, channel_id: Snowflake, *, reason: Optional[str] = None): ...
    async def follow_news_channel(
        self, channel_id: Snowflake, *, webhook_channel_id: Snowflake
    ): ...
    async def trigger_typing(self, channel_id: Snowflake): ...

class ThreadsEndpointMixin:
    async def get_thread_member(self, channel_id: Snowflake, user_id: Snowflake): ...
    async def list_thread_members(self, channel_id: Snowflake): ...
    async def list_public_archived_threads(
        self,
        channel_id: Snowflake,
        *,
        before: MissingOr[datetime] = MISSING,
        limit: MissingOr[int] = MISSING,
    ): ...
    async def list_private_archived_threads(
        self,
        channel_id: Snowflake,
        *,
        before: MissingOr[datetime] = MISSING,
        limit: MissingOr[int] = MISSING,
    ): ...
    async def list_joined_private_archived_threads(
        self,
        channel_id: Snowflake,
        *,
        before: MissingOr[datetime] = MISSING,
        limit: MissingOr[int] = MISSING,
    ): ...
    async def start_thread_from_message(
        self,
        channel_id: Snowflake,
        message_id: Snowflake,
        *,
        name: str,
        auto_archive_duration: MissingOr[int] = MISSING,
        rate_limit_per_user: MissingOr[Optional[int]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def start_thread_without_message(
        self,
        channel_id: Snowflake,
        *,
        name: str,
        auto_archive_duration: MissingOr[int] = MISSING,
        type: MissingOr[int] = MISSING,
        invitable: MissingOr[bool] = MISSING,
        rate_limit_per_user: MissingOr[Optional[int]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def join_thread(self, channel_id: Snowflake): ...
    async def add_thread_member(self, channel_id: Snowflake, user_id: Snowflake): ...
    async def leave_thread(self, channel_id: Snowflake): ...
    async def remove_thread_member(self, channel_id: Snowflake, user_id: Snowflake): ...

class MessagesEndpointMixin:
    async def get_channel_message(self, channel_id: Snowflake, message_id: Snowflake): ...
    async def get_channel_messages(
        self,
        channel_id: Snowflake,
        *,
        around: MissingOr[Snowflake] = MISSING,
        before: MissingOr[Snowflake] = MISSING,
        after: MissingOr[Snowflake] = MISSING,
        limit: int = 50,
    ): ...
    async def get_pinned_messages(self, channel_id: Snowflake): ...
    async def get_reactions(
        self,
        channel_id: Snowflake,
        message_id: Snowflake,
        emoji: str,
        *,
        after: MissingOr[Snowflake] = MISSING,
        limit: int = 25,
    ): ...
    async def create_message(
        self,
        channel_id: Snowflake,
        *,
        content: MissingOr[str] = MISSING,
        tts: MissingOr[bool] = MISSING,
        embeds: MissingOr[List[EmbedData]] = MISSING,
        allowed_mentions: MissingOr[AllowedMentionsData] = MISSING,
        message_reference: MissingOr[MessageReferenceData] = MISSING,
        # TODO: Components
        sticker_ids: MissingOr[List[Snowflake]] = MISSING,
        attachments: MissingOr[List[PartialAttachmentData]] = MISSING,
        flags: MissingOr[int] = MISSING,
        files: MissingOr[List[BasicFile]] = MISSING,
    ): ...
    async def create_reaction(self, channel_id: Snowflake, message_id: Snowflake, emoji: str): ...
    async def edit_message(
        self,
        channel_id: Snowflake,
        message_id: Snowflake,
        *,
        content: MissingOr[str] = MISSING,
        embeds: MissingOr[List[EmbedData]] = MISSING,
        flags: MissingOr[int] = MISSING,
        allowed_mentions: MissingOr[AllowedMentionsData] = MISSING,
        # TODO: Components
        attachments: MissingOr[List[PartialAttachmentData]] = MISSING,
        files: MissingOr[List[BasicFile]] = MISSING,
    ): ...
    async def delete_message(
        self, channel_id: Snowflake, message_id: Snowflake, *, reason: Optional[str] = None
    ): ...
    async def delete_own_reaction(
        self, channel_id: Snowflake, message_id: Snowflake, emoji: str
    ): ...
    async def delete_user_reaction(
        self, channel_id: Snowflake, message_id: Snowflake, emoji: str, user_id: Snowflake
    ): ...
    async def delete_all_reactions(self, channel_id: Snowflake, message_id: Snowflake): ...
    async def delete_all_reactions_for_emoji(
        self, channel_id: Snowflake, message_id: Snowflake, emoji: str
    ): ...
    async def bulk_delete_messages(
        self, channel_id: Snowflake, *, messages: List[Snowflake], reason: Optional[str] = None
    ): ...
    async def crosspost_message(self, channel_id: Snowflake, message_id: Snowflake): ...
    async def pin_message(
        self, channel_id: Snowflake, message_id: Snowflake, *, reason: Optional[str] = None
    ): ...
    async def unpin_message(
        self, channel_id: Snowflake, message_id: Snowflake, *, reason: Optional[str] = None
    ): ...
