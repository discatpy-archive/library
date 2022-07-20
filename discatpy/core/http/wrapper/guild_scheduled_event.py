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

from discord_typings import GuildScheduledEventEntityMetadata

from ...types import EllipsisOr, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = ("GuildScheduledEventEndpointMixin",)


class GuildScheduledEventEndpointMixin(CoreMixin):
    get_guild_scheduled_event = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}",
        format_args={"guild_id": Snowflake, "guild_scheduled_event_id": Snowflake},
        param_args=[("with_user_count", EllipsisOr[bool], ...)],
    )
    get_guild_scheduled_event_users = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users",
        format_args={"guild_id": Snowflake, "guild_scheduled_event_id": Snowflake},
        param_args=[
            ("limit", int, 100),
            ("with_member", bool, False),
            ("before", EllipsisOr[Snowflake], ...),
            ("after", EllipsisOr[Snowflake], ...),
        ],
    )
    list_scheduled_events_for_guild = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/scheduled-events",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("with_user_count", EllipsisOr[bool], ...),
        ],
    )
    create_guild_scheduled_event = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/scheduled-events",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("channel_id", EllipsisOr[Snowflake], ...),
            ("entity_metadata", EllipsisOr[GuildScheduledEventEntityMetadata], ...),
            ("name", str),
            ("privacy_level", int),
            ("scheduled_start_time", datetime),
            ("scheduled_end_time", EllipsisOr[datetime], ...),
            ("description", EllipsisOr[str], ...),
            ("entity_type", int),
            ("image", EllipsisOr[str], ...),
        ],
    )
    modify_guild_scheduled_event = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}",
        format_args={"guild_id": Snowflake, "guild_scheduled_event_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("channel_id", EllipsisOr[Snowflake], ...),
            ("entity_metadata", EllipsisOr[GuildScheduledEventEntityMetadata], ...),
            ("name", EllipsisOr[str], ...),
            ("privacy_level", EllipsisOr[int], ...),
            ("scheduled_start_time", EllipsisOr[datetime], ...),
            ("scheduled_end_time", EllipsisOr[datetime], ...),
            ("description", EllipsisOr[Optional[str]], ...),
            ("entity_type", EllipsisOr[int], ...),
            ("status", EllipsisOr[int], ...),
            ("image", EllipsisOr[str], ...),
        ],
    )
    delete_guild_scheduled_event = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}",
        format_args={"guild_id": Snowflake, "guild_scheduled_event_id": Snowflake},
    )
