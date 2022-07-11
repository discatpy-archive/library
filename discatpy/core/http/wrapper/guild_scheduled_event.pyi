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

from ...types import MISSING, MissingOr, Snowflake

class GuildScheduledEventEndpointMixin:
    async def get_guild_scheduled_event(
        self,
        guild_id: Snowflake,
        guild_scheduled_event_id: Snowflake,
        *,
        with_user_count: MissingOr[bool] = MISSING,
    ): ...
    async def get_guild_scheduled_event_users(
        self,
        guild_id: Snowflake,
        guild_scheduled_event_id: Snowflake,
        *,
        limit: int = 100,
        with_member: bool = False,
        before: MissingOr[Snowflake] = MISSING,
        after: MissingOr[Snowflake] = MISSING,
    ): ...
    async def list_scheduled_events_for_guild(
        self, guild_id: Snowflake, *, with_user_count: MissingOr[bool] = MISSING
    ): ...
    async def create_guild_scheduled_event(
        self,
        guild_id: Snowflake,
        *,
        channel_id: MissingOr[Snowflake] = MISSING,
        entity_metadata: MissingOr[GuildScheduledEventEntityMetadata] = MISSING,
        name: str,
        privacy_level: int,
        scheduled_start_time: datetime,
        scheduled_end_time: MissingOr[datetime] = MISSING,
        description: MissingOr[str] = MISSING,
        entity_type: int,
        image: MissingOr[str] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_scheduled_event(
        self,
        guild_id: Snowflake,
        guild_scheduled_event_id: Snowflake,
        *,
        channel_id: MissingOr[Snowflake] = MISSING,
        entity_metadata: MissingOr[GuildScheduledEventEntityMetadata] = MISSING,
        name: MissingOr[str] = MISSING,
        privacy_level: MissingOr[int] = MISSING,
        scheduled_start_time: MissingOr[datetime] = MISSING,
        scheduled_end_time: MissingOr[datetime] = MISSING,
        description: MissingOr[str] = MISSING,
        entity_type: MissingOr[int] = MISSING,
        image: MissingOr[str] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def delete_guild_scheduled_event(
        self, guild_id: Snowflake, guild_scheduled_event_id: Snowflake
    ): ...
