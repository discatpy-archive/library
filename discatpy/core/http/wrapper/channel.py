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
from discord_typings import EmbedData, AllowedMentionsData, MessageReferenceData, PartialAttachmentData, PermissionOverwriteData, AttachmentData
from typing import Optional

from ...types import Snowflake, MISSING, MissingOr
from .._client import _HTTPClient
from .core import APIEndpointData, generate_api_wrapper_functions

__all__ = (
    "ChannelEndpointMixin",
    "ThreadsEndpointMixin",
    "MessagesEndpointMixin",
)

@generate_api_wrapper_functions
class ChannelEndpointMixin(_HTTPClient):
    get_channel = APIEndpointData("GET", "/channels/{channel_id}", format_args={"channel_id": Snowflake})
    get_guild_channels = APIEndpointData("GET", "/guilds/{guild_id}", format_args={"guild_id": Snowflake})
    create_guild_channel = APIEndpointData(
        "POST", 
        "/guilds/{guild_id}", 
        format_args={"guild_id": Snowflake}, 
        supports_reason=True, 
        param_args=[
            ("name", str),
            ("type", MissingOr[Optional[int]], MISSING),
            ("topic", MissingOr[Optional[str]], MISSING),
            ("bitrate", MissingOr[Optional[int]], MISSING),
            ("user_limit", MissingOr[Optional[int]], MISSING),
            ("rate_limit_per_user", MissingOr[Optional[int]], MISSING),
            ("position", MissingOr[Optional[int]], MISSING),
            ("permission_overwrites", MissingOr[Optional[list[PermissionOverwriteData]]], MISSING),
            ("parent_id", MissingOr[Optional[Snowflake]], MISSING),
            ("nsfw", MissingOr[Optional[bool]], MISSING),
            ("rtc_region", MissingOr[Optional[str]], MISSING),
            ("video_quality_mode", MissingOr[Optional[int]], MISSING),
            ("default_auto_archive_duration", MissingOr[Optional[int]], MISSING),
        ]
    )
    modify_channel = APIEndpointData(
        "PATCH", 
        "/channels/{channel_id}", 
        format_args={"channel_id": Snowflake}, 
        supports_reason=True,
        param_args=[
            ("name",MissingOr[Optional[str]],MISSING),
            ("type",MissingOr[Optional[int]],MISSING),
            ("position",MissingOr[Optional[int]],MISSING),
            ("topic",MissingOr[Optional[str]],MISSING),
            ("nsfw",MissingOr[Optional[bool]],MISSING),
            ("rate_limit_per_user",MissingOr[Optional[int]],MISSING),
            ("bitrate",MissingOr[Optional[int]],MISSING),
            ("user_limit",MissingOr[Optional[int]],MISSING),
            ("permission_overwrites",MissingOr[Optional[list[PermissionOverwriteData]]], MISSING),
            ("parent_id",MissingOr[Optional[Snowflake]],MISSING),
            ("rtc_region",MissingOr[Optional[str]],MISSING),
            ("video_quality_mode",MissingOr[Optional[int]],MISSING),
            ("default_auto_archive_duration", MissingOr[Optional[int]],MISSING),
        ]
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
        ]
    )
    delete_channel = APIEndpointData("DELETE", "/channels/{channel_id}", format_args={"channel_id": Snowflake})

@generate_api_wrapper_functions
class ThreadsEndpointMixin(_HTTPClient):
    get_thread_member = APIEndpointData("GET", "/channels/{channel_id}/thread-members/{user_id}", format_args={"channel_id": Snowflake, "user_id": Snowflake})
    list_thread_members = APIEndpointData("GET", "/channels/{channel_id}/thread-members", format_args={"channel_id": Snowflake})
    list_public_archived_threads = APIEndpointData(
        "GET", 
        "/channels/{channel_id}/threads/archived/public", 
        format_args={"channel_id": Snowflake}, 
        param_args=[
            ("before", MissingOr[datetime], MISSING),
            ("limit", MissingOr[int], MISSING),
        ]
    )
    list_private_archived_threads = APIEndpointData(
        "GET",
        "/channels/{channel_id}/threads/archived/private",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("before", MissingOr[datetime], MISSING),
            ("limit", MissingOr[int], MISSING),
        ]
    )
    list_joined_private_archived_threads = APIEndpointData(
        "GET",
        "/channels/{channel_id}/users/@me/threads/archived/private",
        format_args={"channel_id": Snowflake},
        param_args=[
            ("before", MissingOr[datetime], MISSING),
            ("limit", MissingOr[int], MISSING),
        ]
    )
    start_thread_from_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/messages/{message_id}/threads",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("auto_archive_duration", MissingOr[int], MISSING),
            ("rate_limit_per_user", MissingOr[Optional[int]], MISSING),
        ]
    )
    start_thread_without_message = APIEndpointData(
        "POST",
        "/channels/{channel_id}/threads",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("auto_archive_duration", MissingOr[int], MISSING),
            ("type", MissingOr[int], MISSING),
            ("invitable", MissingOr[bool], MISSING),
            ("rate_limit_per_user", MissingOr[Optional[int]], MISSING),
        ]
    )
    join_thread = APIEndpointData("PUT", "/channels/{channel_id}/thread-members/@me", format_args={"channel_id": Snowflake})
    add_thread_member = APIEndpointData("PUT", "/channels/{channel_id}/thread-members/{user_id}", format_args={"channel_id": Snowflake, "user_id": Snowflake})
    leave_thread = APIEndpointData("DELETE", "/channels/{channel_id}/thread-members/@me", format_args={"channel_id": Snowflake})
    remove_thread_member = APIEndpointData("DELETE", "/channels/{channel_id}/thread-members/{user_id}", format_args={"channel_id": Snowflake, "user_id": Snowflake})

@generate_api_wrapper_functions
class MessagesEndpointMixin(_HTTPClient):
    get_channel_message = APIEndpointData("GET", "/channels/{channel_id}/messages/{message_id}", format_args={"channel_id": Snowflake, "message_id": Snowflake})
    get_channel_messages = APIEndpointData(
        "GET", 
        "/channels/{channel_id}/messages", 
        format_args={"channel_id": Snowflake},
        param_args=[
            ("around", MissingOr[Snowflake], MISSING),
            ("before", MissingOr[Snowflake], MISSING),
            ("after", MissingOr[Snowflake], MISSING),
            ("limit", int, 50),
        ]
    )
    # TODO: add custom code that checks if content, embeds, and sticker ids are all MISSING then warn
    create_message = APIEndpointData(
        "POST", 
        "/channels/{channel_id}/messages", 
        format_args={"channel_id": Snowflake},
        param_args=[
            ("content", MissingOr[str], MISSING),
            ("tts", MissingOr[bool], MISSING),
            ("embeds", MissingOr[list[EmbedData]], MISSING),
            ("allowed_mentions", MissingOr[AllowedMentionsData], MISSING),
            ("message_reference", MissingOr[MessageReferenceData], MISSING),
            # TODO: Components
            ("sticker_ids", MissingOr[list[Snowflake]], MISSING),
            # TODO: Files
            ("attachments", MissingOr[list[PartialAttachmentData]], MISSING),
            ("flags", MissingOr[int], MISSING),
        ]
    )
    edit_message = APIEndpointData(
        "PATCH",
        "/channels/{channel_id}/messages/{message_id}",
        format_args={"channel_id": Snowflake, "message_id": Snowflake},
        param_args=[
            ("content", MissingOr[Optional[str]], MISSING),
            ("embeds", MissingOr[Optional[list[EmbedData]]], MISSING),
            ("flags", MissingOr[Optional[int]], MISSING),
            ("allowed_mentions", MissingOr[Optional[AllowedMentionsData]], MISSING),
            # TODO: Components, Files
            ("attachments", MissingOr[Optional[list[AttachmentData]]], MISSING)
        ]
    )
    crosspost_message = APIEndpointData("POST", "/channels/{channel_id}/messages/{message_id}/crosspost", format_args={"channel_id": Snowflake, "message_id": Snowflake})
