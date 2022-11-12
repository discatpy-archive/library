# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from enum import Enum

import attr
import discord_typings as dt
from discatcore.types import Unset, UnsetOr

from ..flags import Flag, flag
from ..utils.attr_exts import frozen_for_public
from .asset import Asset, AssetPresets
from .color import Color

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = (
    "UserPremiumTypes",
    "UserFlags",
    "User",
)


class UserPremiumTypes(int, Enum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class UserFlags(Flag):
    if t.TYPE_CHECKING:
        def __init__(
            self,
            staff: bool = ...,
            partner: bool = ...,
            hypesquad: bool = ...,
            bug_hunter_level_1: bool = ...,
            hypesquad_online_house_1: bool = ...,
            hypesquad_online_house_2: bool = ...,
            hypesquad_online_house_3: bool = ...,
            premium_early_supporter: bool = ...,
            team_pseudo_user: bool = ...,
            bug_hunter_level_2: bool = ...,
            verified_bot: bool = ...,
            early_verified_bot_developer: bool = ...,
            certified_moderator: bool = ...,
            bot_http_interactions: bool = ...,
            active_developer: bool = ...,
        ) -> None:
            ...
    @flag
    def STAFF():
        return 1 << 0

    @flag
    def PARTNER():
        return 1 << 1

    @flag
    def HYPESQUAD():
        return 1 << 2

    @flag
    def BUG_HUNTER_LEVEL_1():
        return 1 << 3

    @flag
    def HYPESQUAD_ONLINE_HOUSE_1():
        return 1 << 6

    @flag
    def HYPESQUAD_ONLINE_HOUSE_2():
        return 1 << 7

    @flag
    def HYPESQUAD_ONLINE_HOUSE_3():
        return 1 << 8

    @flag
    def PREMIUM_EARLY_SUPPORTER():
        return 1 << 9

    @flag
    def TEAM_PSEUDO_USER():
        return 1 << 10

    @flag
    def BUG_HUNTER_LEVEL_2():
        return 1 << 14

    @flag
    def VERIFIED_BOT():
        return 1 << 16

    @flag
    def VERIFIED_DEVELOPER():
        return 1 << 17

    @flag
    def CERTIFIED_MODERATOR():
        return 1 << 18

    @flag
    def BOT_HTTP_INTERACTIONS():
        return 1 << 19

    @flag
    def ACTIVE_DEVELOPER():
        return 1 << 22


@frozen_for_public
@attr.define(kw_only=True)
class User:
    bot: Bot
    data: dt.UserData
    id: dt.Snowflake = attr.field(init=False)
    username: str = attr.field(init=False)
    discriminator: str = attr.field(init=False)
    avatar: Asset = attr.field(init=False)
    is_bot: bool = attr.field(init=False)
    is_system: bool = attr.field(init=False)
    mfa_enabled: UnsetOr[bool] = attr.field(init=False)
    banner: UnsetOr[t.Optional[Asset]] = attr.field(init=False)
    accent_color: UnsetOr[t.Optional[Color]] = attr.field(init=False)
    # TODO: type to Locales enum
    locale: UnsetOr[dt.Locales] = attr.field(init=False)
    is_verified: UnsetOr[bool] = attr.field(init=False)
    email: UnsetOr[t.Optional[str]] = attr.field(init=False)
    flags: UnsetOr[UserFlags] = attr.field(init=False)
    premium_type: UnsetOr[UserPremiumTypes] = attr.field(init=False)
    public_flags: UnsetOr[UserFlags] = attr.field(init=False)

    def __attrs_post_init__(self):
        self.id = self.data["id"]
        self.username = self.data["username"]
        self.discriminator = self.data["discriminator"]

        raw_avatar = self.data.get("avatar")
        if isinstance(raw_avatar, str):
            self.avatar = Asset.from_asset_preset(
                self.bot, AssetPresets.user_avatar(self.id, raw_avatar)
            )
        else:
            self.avatar = Asset.from_asset_preset(
                self.bot, AssetPresets.default_user_avatar(int(self.discriminator))
            )

        self.is_bot = self.data.get("bot", False)
        self.is_system = self.data.get("system", False)
        self.mfa_enabled = self.data.get("mfa_enabled", Unset)

        raw_banner = self.data.get("banner", Unset)
        if isinstance(raw_banner, str):
            self.banner = Asset.from_asset_preset(
                self.bot, AssetPresets.banner(self.id, raw_banner)
            )
        else:
            self.banner = raw_banner

        raw_accent_color = self.data.get("accent_color", Unset)
        if isinstance(raw_accent_color, int):
            self.accent_color = Color.from_hex(raw_accent_color)
        else:
            self.accent_color = raw_accent_color

        self.locale = self.data.get("locale", Unset)
        self.is_verified = self.data.get("verified", Unset)

        raw_flags = self.data.get("flags", Unset)
        if isinstance(raw_flags, int):
            self.flags = UserFlags.from_value(raw_flags)
        else:
            self.flags = raw_flags

        raw_premium_type = self.data.get("premium_type", Unset)
        if isinstance(raw_premium_type, int):
            self.premium_type = UserPremiumTypes(raw_premium_type)
        else:
            self.premium_type = raw_premium_type

        raw_public_flags = self.data.get("public_flags", Unset)
        if isinstance(raw_public_flags, int):
            self.public_flags = UserFlags.from_value(raw_public_flags)
        else:
            self.public_flags = raw_public_flags
