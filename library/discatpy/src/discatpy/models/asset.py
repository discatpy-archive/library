# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t

import attr
from discord_typings import Snowflake

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("AssetPresets", "Asset")

ALL_SUPPORTED_EXTENSIONS = ("png", "jpg", "jpeg", "webp", "gif", "json")


class AssetPresets:
    @staticmethod
    def custom_emoji(emoji_id: Snowflake, /):
        return f"emojis/{emoji_id}", ("png", "jpg", "jpeg", "webp", "gif")

    @staticmethod
    def guild_icon(guild_id: Snowflake, hash: str, /):
        return f"icons/{guild_id}/{hash}", ("png", "jpg", "jpeg", "webp", "gif")

    @staticmethod
    def guild_splash(guild_id: Snowflake, hash: str, /):
        return f"splashes/{guild_id}/{hash}"

    @staticmethod
    def guild_discovery_splash(guild_id: Snowflake, hash: str, /):
        return f"discovery-splashes/{guild_id}/{hash}"

    @staticmethod
    def banner(id: Snowflake, hash: str, /):
        return f"banners/{id}/{hash}", ("png", "jpg", "jpeg", "webp", "gif")

    @staticmethod
    def default_user_avatar(user_discriminator: int, /):
        return f"embed/avatars/{user_discriminator % 5}", ("png",)

    @staticmethod
    def user_avatar(user_id: Snowflake, hash: str, /):
        return f"avatars/{user_id}/{hash}", ("png", "jpg", "jpeg", "webp", "gif")

    @staticmethod
    def guild_member_avatar(guild_id: Snowflake, user_id: Snowflake, hash: str, /):
        return f"guilds/{guild_id}/users/{user_id}/avatars/{hash}", (
            "png",
            "jpg",
            "jpeg",
            "webp",
            "gif",
        )

    @staticmethod
    def application_icon(app_id: Snowflake, hash: str, /):
        return f"app-icons/{app_id}/{hash}", ("png", "jpg", "jpeg", "webp")

    application_cover = application_icon

    @staticmethod
    def application_asset(app_id: Snowflake, asset_id: Snowflake, /):
        return f"app-assets/{app_id}/{asset_id}", ("png", "jpg", "jpeg", "webp")

    @staticmethod
    def achievement_icon(app_id: Snowflake, achievement_id: Snowflake, hash: str, /):
        return f"app-assets/{app_id}/achievements/{achievement_id}/icons/{hash}", (
            "png",
            "jpg",
            "jpeg",
            "webp",
        )

    @staticmethod
    def sticker_pack_banner(banner_asset_id: Snowflake, /):
        return f"app-assets/710982414301790216/store/{banner_asset_id}", (
            "png",
            "jpg",
            "jpeg",
            "webp",
        )

    @staticmethod
    def team_icon(team_id: Snowflake, hash: str, /):
        return f"team-icons/{team_id}/{hash}", ("png", "jpg", "jpeg", "webp")

    @staticmethod
    def sticker(sticker_id: Snowflake, /):
        return f"stickers/{sticker_id}", ("png", "json")

    @staticmethod
    def role_icon(role_id: Snowflake, hash: str, /):
        return f"role-icons/{role_id}/{hash}", ("png", "jpg", "jpeg", "webp")

    @staticmethod
    def guild_scheduled_event_cover(event_id: Snowflake, hash: str, /):
        return f"guild-events/{event_id}/{hash}", ("png", "jpg", "jpeg", "webp")

    @staticmethod
    def guild_member_banner(guild_id: Snowflake, user_id: Snowflake, hash: str, /):
        return f"guilds/{guild_id}/users/{user_id}/banners/{hash}", (
            "png",
            "jpg",
            "jpeg",
            "webp",
            "gif",
        )


def _supported_types_validator(
    instance: Asset, attribute: attr.Attribute[tuple[str, ...]], value: tuple[str, ...]
):
    for v in value:
        if v not in ALL_SUPPORTED_EXTENSIONS:
            raise ValueError(f"supported_types was provided invalid type {v}!")


def _extension_validator(instance: Asset, attribute: attr.Attribute[str], value: str):
    if value not in ALL_SUPPORTED_EXTENSIONS:
        raise ValueError(f"extension was provided invalid type {value}!")

    elif value not in instance.supported_types:
        raise ValueError(f"extension was provided unsupported type {value}!")


def _size_validator(instance: Asset, attribute: attr.Attribute[int], value: int):
    if value < 16 or value > 4096:
        raise ValueError(f"size must be in-between 16 and 4096 (inclusive)!")

    if 2 ** (value.bit_length() - 1) != value:
        raise ValueError(f"size must be a power of two!")


@attr.define(kw_only=True)
class Asset:
    bot: Bot
    url: str
    supported_types: tuple[str, ...] = attr.field(validator=_supported_types_validator)
    extension: str = attr.field(init=False, validator=_extension_validator)
    supports_gif: bool = attr.field(init=False)
    size: int = attr.field(init=False, validator=_size_validator, default=16)

    def __attrs_post_init__(self):
        self.url = self.url.lstrip("/")
        self.supports_gif = (
            self.url.split("/")[1].startswith("a_") and "gif" in self.supported_types
        )
        self.extension = "gif" if self.supports_gif else "png"

    @classmethod
    def from_asset_preset(cls, bot: Bot, preset: tuple[str, tuple[str, ...]]):
        return cls(bot=bot, url=preset[0], supported_types=preset[1])

    @property
    def formatted_url(self):
        return f"https://cdn.discordapp.com/{self.url}.{self.extension}?size={self.size}"

    async def read(self):
        return await self.bot.http.get_from_cdn(self.formatted_url)

    def replace(self, *, size: t.Optional[int] = None, extension: t.Optional[str] = None):
        if size is not None:
            self.size = size
        if extension is not None:
            self.extension = extension.lstrip(".")
