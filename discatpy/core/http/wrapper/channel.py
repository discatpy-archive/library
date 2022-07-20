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
from typing import List, Optional

from discord_typings import (
    AllowedMentionsData,
    AttachmentData,
    EmbedData,
    MessageReferenceData,
    PartialAttachmentData,
    PermissionOverwriteData,
)

from ...types import EllipsisOr, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = (
    "ChannelEndpointMixin",
    "ThreadsEndpointMixin",
    "MessagesEndpointMixin",
)


class ChannelEndpointMixin(CoreMixin):
    get_channel = APIEndpointData(
        "GET", "/channels/{channel_id}", format_args={"channel_id": Snowflake}
    )
    get_guild_channels = APIEndpointData(
        "GET", "/guilds/{guild_id}/channels", format_args={"guild_id": Snowflake}
    )
    get_channel_invites = APIEndpointData(
        "GET", "/channels/{channel_id}/invites", format_args={"channel_id": Snowflake}
    )
    create_guild_channel = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/channels",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("type", EllipsisOr[Optional[int]], ...),
            ("topic", EllipsisOr[Optional[str]], ...),
            ("bitrate", EllipsisOr[Optional[int]], ...),
            ("user_limit", EllipsisOr[Optional[int]], ...),
            ("rate_limit_per_user", EllipsisOr[Optional[int]], ...),
            ("position", EllipsisOr[Optional[int]], ...),
            ("permission_overwrites", EllipsisOr[Optional[List[PermissionOverwriteData]]], ...),
            ("parent_id", EllipsisOr[Optional[Snowflake]], ...),
            ("nsfw", EllipsisOr[Optional[bool]], ...),
            ("rtc_region", EllipsisOr[Optional[str]], ...),
            ("video_quality_mode", EllipsisOr[Optional[int]], ...),
            ("default_auto_archive_duration", EllipsisOr[Optional[int]], ...),
        ],
    )
    create_channel_invite = APIEndpointData(
        "POST",
        "/channels/{channel_id}/invites",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("max_age", int, 86400),
            ("max_uses", int, 0),
            ("temporary", bool, False),
            ("unique", bool, False),
            ("target_type", int),
            ("target_user_id", Snowflake),
            ("target_application_id", Snowflake),
        ],
    )
    modify_channel = APIEndpointData(
        "PATCH",
        "/channels/{channel_id}",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", EllipsisOr[Optional[str]], ...),
            ("type", EllipsisOr[Optional[int]], ...),
            ("position", EllipsisOr[Optional[int]], ...),
            ("topic", EllipsisOr[Optional[str]], ...),
            ("nsfw", EllipsisOr[Optional[bool]], ...),
            ("rate_limit_per_user", EllipsisOr[Optional[int]], ...),
            ("bitrate", EllipsisOr[Optional[int]], ...),
            ("user_limit", EllipsisOr[Optional[int]], ...),
            ("permission_overwrites", EllipsisOr[Optional[List[PermissionOverwriteData]]], ...),
            ("parent_id", EllipsisOr[Optional[Snowflake]], ...),
            ("rtc_region", EllipsisOr[Optional[str]], ...),
            ("video_quality_mode", EllipsisOr[Optional[int]], ...),
            ("default_auto_archive_duration", EllipsisOr[Optional[int]], ...),
        ],
    )
    modify_guild_channel_positions = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/channels",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("id", Snowflake),
            ("position", Optional[int], None),
            ("lock_permissions", Optional[bool], None),
            ("parent_id", Optional[Snowflake], None),
        ],
    )
    edit_channel_permissions = APIEndpointData(
        "PUT",
        "/channels/{channel_id}/permissions/{overwrite_id}",
        format_args={"channel_id": Snowflake, "overwrite_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("allow", EllipsisOr[str], ...),
            ("deny", EllipsisOr[str], ...),
            ("type", int),
        ],
    )
    delete_channel = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
    )
    follow_news_channel = APIEndpointData(
        "POST",
        "/channels/{channel_id}/followers",
        format_args={"channel_id": Snowflake},
        param_args=[("webhook_channel_id", Snowflake)],
    )
    trigger_typing = APIEndpointData(
        "POST", "/channels/{channel_id}/typing", format_args={"channel_id": Snowflake}
    )


class ThreadsEndpointMixin(CoreMixin):
    get_thread_member = APIEndpointData(
        "GET",
        "/channels/{channel_id}/thread-members/{user_id}",
        format_args={"channel_id": Snowflake, "user_id": Snowflake},
    )
    list_thread_members = APIEndpointData(
        "GET", "/channels/{channel_id}/thread-members", format_args={"channel_id": Snowflake}
    )
    list_public_archived_threads = APIEndpointData(
        "GET",
        "/channels/{channel_id}/threads/archived/public",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("before", EllipsisOr[datetime], ...),
            ("limit", EllipsisOr[int], ...),
        ],
    )
    list_private_archived_threads = APIEndpointData(
        "GET",
        "/channels/{channel_id}/threads/archived/private",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("before", EllipsisOr[datetime], ...),
            ("limit", EllipsisOr[int], ...),
        ],
    )
    list_joined_private_archived_threads = APIEndpointData(
        "GET",
        "/channels/{channel_id}/users/@me/threads/archived/private",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("before", EllipsisOr[datetime], ...),
            ("limit", EllipsisOr[int], ...),
        ],
    )
    start_thread_from_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/messages/{message_id}/threads",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("auto_archive_duration", EllipsisOr[int], ...),
            ("rate_limit_per_user", EllipsisOr[Optional[int]], ...),
        ],
    )
    start_thread_without_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/threads",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("auto_archive_duration", EllipsisOr[int], ...),
            ("type", EllipsisOr[int], ...),
            ("invitable", EllipsisOr[bool], ...),
            ("rate_limit_per_user", EllipsisOr[Optional[int]], ...),
        ],
    )
    join_thread = APIEndpointData(
        "PUT", "/channels/{channel_id}/thread-members/@me", format_args={"channel_id": Snowflake}
    )
    add_thread_member = APIEndpointData(
        "PUT",
        "/channels/{channel_id}/thread-members/{user_id}",
        format_args={"channel_id": Snowflake, "user_id": Snowflake},
    )
    leave_thread = APIEndpointData(
        "DELETE", "/channels/{channel_id}/thread-members/@me", format_args={"channel_id": Snowflake}
    )
    remove_thread_member = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/thread-members/{user_id}",
        format_args={"channel_id": Snowflake, "user_id": Snowflake},
    )


class MessagesEndpointMixin(CoreMixin):
    get_channel_message = APIEndpointData(
        "GET",
        "/channels/{channel_id}/messages/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
    )
    get_channel_messages = APIEndpointData(
        "GET",
        "/channels/{channel_id}/messages",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("around", EllipsisOr[Snowflake], ...),
            ("before", EllipsisOr[Snowflake], ...),
            ("after", EllipsisOr[Snowflake], ...),
            ("limit", int, 50),
        ],
    )
    get_pinned_messages = APIEndpointData(
        "GET", "/channel/{channel_id}/pins", format_args={"channel_id": Snowflake}
    )
    get_reactions = APIEndpointData(
        "GET",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake, "emoji": str},
        param_args=[
            ("after", EllipsisOr[Snowflake], ...),
            ("limit", int, 25),
        ],
    )
    create_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/messages",
        format_args={"channel_id": Snowflake},
        supports_files=True,
        param_args=[
            ("content", EllipsisOr[str], ...),
            ("tts", EllipsisOr[bool], ...),
            ("embeds", EllipsisOr[List[EmbedData]], ...),
            ("allowed_mentions", EllipsisOr[AllowedMentionsData], ...),
            ("message_reference", EllipsisOr[MessageReferenceData], ...),
            # TODO: Components
            ("sticker_ids", EllipsisOr[List[Snowflake]], ...),
            ("attachments", EllipsisOr[List[PartialAttachmentData]], ...),
            ("flags", EllipsisOr[int], ...),
        ],
    )
    create_reaction = APIEndpointData(
        "PUT",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
        format_args={"channel_id": Snowflake, "message_id": Snowflake, "emoji": str},
    )
    edit_message = APIEndpointData(
        "PATCH",
        "/channels/{channel_id}/messages/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_files=True,
        param_args=[
            ("content", EllipsisOr[Optional[str]], ...),
            ("embeds", EllipsisOr[Optional[List[EmbedData]]], ...),
            ("flags", EllipsisOr[Optional[int]], ...),
            ("allowed_mentions", EllipsisOr[Optional[AllowedMentionsData]], ...),
            # TODO: Components
            ("attachments", EllipsisOr[Optional[List[AttachmentData]]], ...),
        ],
    )
    delete_message = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/messages/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_reason=True,
    )
    delete_own_reaction = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
        format_args={"channel_id": Snowflake, "message_id": Snowflake, "emoji": str},
    )
    delete_user_reaction = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}",
        format_args={
            "channel_id": Snowflake,
            "message_id": Snowflake,
            "emoji": str,
            "user_id": Snowflake,
        },
    )
    delete_all_reactions = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/messages/{message_id}/reactions",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
    )
    delete_all_reactions_for_emoji = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake, "emoji": str},
    )
    bulk_delete_messages = APIEndpointData(
        "POST",
        "/channels/{channel_id}/messages/bulk-delete",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[("messages", List[Snowflake])],
    )
    crosspost_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/messages/{message_id}/crosspost",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
    )
    pin_message = APIEndpointData(
        "PUT",
        "/channels/{channel_id}/pins/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_reason=True,
    )
    unpin_message = APIEndpointData(
        "DELETE",
        "/channels/{channel_id}/pins/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_reason=True,
    )
