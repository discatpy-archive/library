# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from collections.abc import AsyncGenerator
from datetime import datetime

import discord_typings as dt
from discatcore.types import Unset, UnsetOr
from discatcore.utils import DISCORD_EPOCH

if t.TYPE_CHECKING:
    from .abc import Messageable

__all__ = ("channel_history",)


def _datetime_to_snowflake(s: datetime) -> dt.Snowflake:
    if (timestamp := int(s.timestamp() * 1000)) < DISCORD_EPOCH:
        raise ValueError("Timestamp is too old to be a Discord timestamp!")

    return (timestamp - DISCORD_EPOCH) << 22


async def channel_history(
    channel: Messageable,
    *,
    before: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
    after: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
    around: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
    limit: t.Optional[int] = None,
) -> AsyncGenerator[dt.MessageData, None]:
    converted_before = _datetime_to_snowflake(before) if isinstance(before, datetime) else before
    converted_after = _datetime_to_snowflake(after) if isinstance(after, datetime) else after
    converted_around = _datetime_to_snowflake(around) if isinstance(around, datetime) else around
    retrieve = 0

    channel_id = await channel._get_channel_id()  # pyright: ignore[reportPrivateUsage]

    def should_retrieve():
        if limit is None or limit > 100:
            retrieve = 100
        else:
            retrieve = limit
        return retrieve > 0

    while should_retrieve():
        data = t.cast(
            list[dt.MessageData],
            await channel.bot.http.get_channel_messages(
                channel_id,
                before=converted_before,
                after=converted_after,
                around=converted_around,
                limit=retrieve,
            ),
        )

        if len(data):
            if limit:
                limit -= retrieve
            if len(data) < 100:
                limit = 0

            if before is not Unset:
                converted_before = int(data[-1]["id"])
            if after is not Unset:
                converted_after = int(data[0]["id"])
            if around is not Unset:
                converted_around = Unset

        if after is not Unset:
            data = reversed(data)

        for msg in data:
            yield msg
