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
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ...core.types import Snowflake

if TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("Asset",)

BASE_CDN_PATH = "https://cdn.discordapp.com/"
VALID_IMAGE_FORMATS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif",
]


class Asset:
    """Represents a CDN asset from Discord.

    Attributes
    ----------
    bot: :class:`Bot`
        A reference to the bot.
    format: :type:`str`
        The image format of this Asset.
    key: :type:`str`
        The filename of this Asset.
    path: :type:`str`
        The path to this Asset.
    animated: :type:`bool`
        Whether or not this Asset is animated. If it is, then :attr:`format` will
        be set to `gif`.
    """

    def __init__(self, bot: Bot, path: str, key: str, animated: bool = False):
        self.bot = bot
        self.format = "png" if not animated else "gif"  # by default it's png or gif if animated
        self.key = key
        self.animated = animated
        self.path = path

    @property
    def url(self) -> str:
        """:class:`str` Gets the full URL for this Asset."""
        return BASE_CDN_PATH + self.path + self.key + "." + self.format

    def replace(self, *, size: Optional[int] = None, format: Optional[str] = None) -> str:
        if size is None and not format:
            raise ValueError("Size or format parameters have to be provided!")

        if format and format in VALID_IMAGE_FORMATS:
            if format not in VALID_IMAGE_FORMATS:
                raise ValueError(f"Format parameter has invalid value {format}!")
            self.format = format

        new_url = self.url

        if size is not None:
            if size < 0:
                raise ValueError("Size parameter cannot be below 0!")
            elif not (size & (size - 1)) == 0:
                raise ValueError("Size parameter must be a power of 2!")
            elif size < 16 or size > 4096:
                raise ValueError("Size parameter has to be in-between 16 and 4096 (inclusive)!")

            new_url += "?size={size}"

        return new_url

    async def read(self, *, size: Optional[int] = None, format: Optional[str] = None) -> bytes:
        """Reads the Asset file directly from the Discord CDN.

        Parameters
        ----------
        size: :type:`Optional[int]`
            The optional size to grab the CDN file as.

        Returns
        -------
        :type:`bytes`
            The raw bytes of the file.
        """
        url = self.url
        if size or format:
            url = self.replace(size=size, format=format)

        return await self.bot.http.get_from_cdn(url)

    @classmethod
    def from_custom_emoji(cls, client, emoji_id: Snowflake, animated: bool = False):
        return cls(client, "emojis/", str(emoji_id), animated)

    @classmethod
    def from_guild_icon(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"icons/{guild_id}/", hash, hash.startswith("a_"))

    @classmethod
    def from_guild_splash(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"splashes/{guild_id}/", hash)

    @classmethod
    def from_guild_discovery_splash(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"discovery-splashes/{guild_id}/", hash)

    @classmethod
    def from_guild_banner(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"banners/{guild_id}/", hash, hash.startswith("a_"))

    @classmethod
    def from_user_banner(cls, client, user_id: Snowflake, hash: str):
        return cls(client, f"banners/{user_id}/", hash, hash.startswith("a_"))

    @classmethod
    def from_default_user_avatar(cls, client, discriminator: int):
        return cls(client, "embed/avatars/", str(discriminator % 5))

    @classmethod
    def from_user_avatar(cls, client, user_id: Snowflake, hash: str):
        return cls(client, f"avatars/{user_id}/", hash, hash.startswith("a_"))

    @classmethod
    def from_guild_member_avatar(cls, client, guild_id: Snowflake, user_id: Snowflake, hash: str):
        return cls(
            client,
            f"guilds/{guild_id}/users/{user_id}/avatars/",
            hash,
            hash.startswith("a_"),
        )

    # TODO: Add application related assets, achievement icon, stick pack banner, team icon, sticker

    @classmethod
    def from_role_icon(cls, client, role_id: Snowflake, hash: str):
        return cls(client, f"role-icons/{role_id}/", hash)

    @classmethod
    def from_guild_scheduled_event_cover(cls, client, scheduled_event_id: Snowflake, hash: str):
        return cls(client, f"guild-events/{scheduled_event_id}/", hash)
