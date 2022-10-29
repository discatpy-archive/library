# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t

import attr
import discord_typings as dt
from discatcore.types import Unset, UnsetOr

from ..utils.attr_exts import frozen_for_public
from .asset import Asset, AssetPresets
from .user import User

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("Emoji",)


@frozen_for_public
@attr.define(kw_only=True)
class Emoji:
    bot: Bot
    data: dt.EmojiData
    # TODO: guild_owner
    id: t.Optional[dt.Snowflake] = attr.field(init=False)
    name: t.Optional[str] = attr.field(init=False)
    roles: UnsetOr[list[dt.Snowflake]] = attr.field(init=False)
    user: UnsetOr[User] = attr.field(init=False)
    require_colons: UnsetOr[bool] = attr.field(init=False)
    managed: UnsetOr[bool] = attr.field(init=False)
    animated: UnsetOr[bool] = attr.field(init=False)
    available: UnsetOr[bool] = attr.field(init=False)

    def __attrs_post_init__(self):
        self.id = self.data["id"]
        self.name = self.data["name"]
        self.roles = self.data.get("roles", Unset)

        raw_user = self.data.get("user", Unset)
        if isinstance(raw_user, dt.UserData):
            # TODO: attempt to get user object from cache
            self.user = User(bot=self.bot, data=raw_user)
        else:
            self.user = raw_user

        self.require_colons = self.data.get("require_colons", Unset)
        self.managed = self.data.get("managed", Unset)
        self.animated = self.data.get("animated", Unset)
        self.available = self.data.get("available", Unset)

    @property
    def is_custom(self):
        return self.id is not None

    @property
    def asset(self):
        if self.id is None:
            return

        return Asset.from_asset_preset(self.bot, AssetPresets.custom_emoji(self.id))
