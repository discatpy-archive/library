# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from enum import Enum

import attr
import discord_typings as dt
from discatcore.types import Unset, UnsetOr

from ..flags import Flag
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
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


@attr.define(frozen=True)
class User:
    bot_owner: Bot = attr.field(kw_only=True)
    id: dt.Snowflake = attr.field(kw_only=True)
    username: str = attr.field(kw_only=True)
    discriminator: str = attr.field(kw_only=True)
    avatar: t.Optional[t.Union[str, Asset]] = attr.field(kw_only=True)
    bot: UnsetOr[bool] = attr.field(default=Unset, kw_only=True)
    system: UnsetOr[bool] = attr.field(default=Unset, kw_only=True)
    mfa_enabled: UnsetOr[bool] = attr.field(default=Unset, kw_only=True)
    banner: UnsetOr[t.Optional[t.Union[str, Asset]]] = attr.field(default=Unset, kw_only=True)
    accent_color: UnsetOr[t.Optional[int]] = attr.field(
        default=Unset, kw_only=True, converter=Color.from_hex
    )
    # TODO: type to Locales enum
    locale: UnsetOr[dt.Locales] = attr.field(default=Unset, kw_only=True)
    verified: UnsetOr[bool] = attr.field(default=Unset, kw_only=True)
    email: UnsetOr[t.Optional[str]] = attr.field(default=Unset, kw_only=True)
    flags: UnsetOr[int] = attr.field(default=Unset, kw_only=True, converter=UserFlags)
    premium_type: UnsetOr[dt.UserPremiumTypes] = attr.field(
        default=Unset, kw_only=True, converter=UserPremiumTypes
    )
    public_flags: UnsetOr[int] = attr.field(default=Unset, kw_only=True, converter=UserFlags)

    def __attrs_post_init__(self):
        if isinstance(self.avatar, str):
            object.__setattr__(
                self,
                "avatar",
                Asset.from_asset_preset(
                    self.bot_owner, AssetPresets.user_avatar(self.id, self.avatar)
                ),
            )
        if isinstance(self.banner, str):
            object.__setattr__(
                self,
                "banner",
                Asset.from_asset_preset(self.bot_owner, AssetPresets.banner(self.id, self.banner)),
            )

    @classmethod
    def from_dict(cls, data: dt.UserData, bot: Bot):
        return cls(bot_owner=bot, **data)
