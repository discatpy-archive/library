# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t

import discord_typings as dt
from discatcore.types import Unset, UnsetOr

from ..utils.attr_exts import frozen_for_public
from .asset import Asset, AssetPresets
from .user import User

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("Emoji",)


@frozen_for_public
class Emoji:
    def __init__(self, *, bot: Bot, data: dt.EmojiData):
        self.bot: Bot = bot
        self.data: dt.EmojiData = data
        # TODO: guild_owner

        self.id: t.Optional[dt.Snowflake] = self.data["id"]
        self.name: t.Optional[str] = self.data["name"]
        self.roles: UnsetOr[list[dt.Snowflake]] = self.data.get("roles", Unset)

        self.user: UnsetOr[User]
        raw_user = self.data.get("user", Unset)
        if isinstance(raw_user, dt.UserData):
            # TODO: attempt to get user object from cache
            self.user = User(bot=self.bot, data=raw_user)
        else:
            self.user = raw_user

        self.require_colons: UnsetOr[bool] = self.data.get("require_colons", Unset)
        self.managed: UnsetOr[bool] = self.data.get("managed", Unset)
        self.animated: UnsetOr[bool] = self.data.get("animated", Unset)
        self.available: UnsetOr[bool] = self.data.get("available", Unset)

    @property
    def is_custom(self):
        return self.id is not None

    @property
    def asset(self):
        if self.id is None:
            return

        return Asset.from_asset_preset(self.bot, AssetPresets.custom_emoji(self.id))
