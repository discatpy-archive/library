# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from datetime import datetime

import discord_typings as dt
from discatcore import BasicFile
from discatcore.types import Unset, UnsetOr

from .iterators import channel_history

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("Messageable",)


class Messageable:
    bot_owner: Bot

    async def _get_channel_id(self) -> dt.Snowflake:
        return NotImplemented

    async def send_message(
        self,
        content: UnsetOr[str] = Unset,
        *,
        nonce: UnsetOr[t.Union[int, str]] = Unset,
        tts: bool = False,
        # TODO: add embeds, allowed_mentions, components, stickers
        files: UnsetOr[list[BasicFile]] = Unset,
        flags: UnsetOr[int] = Unset,
    ) -> t.Optional[t.Any]:  # TODO: set type hint to message object
        # TODO: automatically generate attachments based on files provided
        channel_id = await self._get_channel_id()
        return await self.bot_owner.http.create_message(
            channel_id, content=content, nonce=nonce, tts=tts, files=files, flags=flags
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
