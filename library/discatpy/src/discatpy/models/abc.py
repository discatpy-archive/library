# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from datetime import datetime

import discord_typings as dt
from discatcore import BasicFile
from discatcore.types import Unset, UnsetOr

from .embed import Embed
from .iterators import channel_history
from .message import _send_message  # pyright: ignore[reportPrivateUsage]
from .message import AllowedMentions, MessageFlags

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("Messageable",)


class Messageable:
    bot: Bot

    async def _get_channel_id(self) -> dt.Snowflake:
        return NotImplemented

    async def send(
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
        channel_id = await self._get_channel_id()
        return await self.bot.http.create_message(
            channel_id,
            **_send_message(
                content,
                nonce,
                tts,
                embeds,
                allowed_mentions,
                Unset,
                stickers,
                files,
                flags,
            ),
        )

    async def history(
        self,
        *,
        before: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
        after: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
        around: UnsetOr[t.Union[datetime, dt.Snowflake]] = Unset,
        limit: t.Optional[int] = None,
    ):
        return channel_history(self, before=before, after=after, around=around, limit=limit)
