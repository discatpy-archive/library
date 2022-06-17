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

from typing import Optional, TYPE_CHECKING
from .types.snowflake import *

if TYPE_CHECKING:
    from .client import Client

__all__ = (
    "Asset",
)

BASE_CDN_PATH = "https://cdn.discordapp.com/"

class Asset:
    """
    Represents a CDN asset from Discord.

    Attributes
    ----------
    client: :type:`Any`
        A reference to the client.
    format: :type:`str`
        The image format of this Asset.
    key: :type:`str`
        The filename of this Asset.
    path: :type:`str`
        The path to this Asset. This must contain `{0}{1}` at the end in 
        order for the image format & key to be formatted correctly into the path.
    animated: :type:`bool`
        Whether or not this Asset is animated. If it is, then :attr:`format` will 
        be set to `gif`.
    """
    client: Client

    def __init__(self, client: Client, path: str, key: str, animated: bool = False):
        self.client = client
        self.format = ".png" if not animated else ".gif"
        self.key = key
        self.animated = animated
        self.path = path.format(self.key, self.format)

    @property
    def url(self) -> str:
        """
        Gets the full URL for this Asset.

        Returns
        -------
        :type:`str`
            The full URL for this Asset.
        """
        return BASE_CDN_PATH + self.path

    def with_size_as(self, size: int) -> str:
        """
        Processes a CDN url with a certain size. This checks the size according to
        https://discord.com/developers/docs/reference#image-formatting-image-base-url.

        Parameters
        ----------
        size: :type:`int`
            The desired size. This size must be a power of 2 and in-between 16 and 
            4096.

        Returns
        -------
        :type:`str`
            The modified CDN url.
        """
        if size < 0:
            raise ValueError("Size parameter cannot be below 0!")

        if not (size & (size - 1)) == 0:
            raise ValueError("Size parameter must be a power of 2!")

        if size < 16 or size > 4096:
            raise ValueError("Size parameter has to be in-between 16 and 4096!")

        return self.url + f"?size={size}"

    async def read(self, size: Optional[int] = None) -> bytes:
        """
        Reads the Asset file directly from the Discord CDN.

        Parameters
        ----------
        size: :type:`Optional[int]`
            The optional size to grab the CDN file as.

        Returns
        -------
        :type:`bytes`
            The raw bytes of the file.
        """
        url = self.url if not size else self.with_size_as(size)
        return await self.client.http.get_from_cdn(url)

    @classmethod
    def from_custom_emoji(cls, client, emoji_id: Snowflake, animated: bool = False):
        return cls(client, "emojis/{0}{1}", str(emoji_id), animated)

    @classmethod
    def from_guild_icon(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"icons/{guild_id}/" + "{0}{1}", hash, hash.startswith("a_"))

    @classmethod
    def from_guild_splash(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"splashes/{guild_id}/" + "{0}{1}", hash)

    @classmethod
    def from_guild_discovery_splash(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"discovery-splashes/{guild_id}/" + "{0}{1}", hash)

    @classmethod
    def from_guild_banner(cls, client, guild_id: Snowflake, hash: str):
        return cls(client, f"banners/{guild_id}/" + "{0}{1}", hash, hash.startswith("a_"))

    @classmethod
    def from_user_banner(cls, client, user_id: Snowflake, hash: str):
        return cls(client, f"banners/{user_id}/" + "{0}{1}", hash, hash.startswith("a_"))

    @classmethod
    def from_default_user_avatar(cls, client, discriminator: int):
        return cls(client, "embed/avatars/{0}{1}", str(discriminator % 5))

    @classmethod
    def from_user_avatar(cls, client, user_id: Snowflake, hash: str):
        return cls(client, f"avatars/{user_id}/" + "{0}{1}", hash, hash.startswith("a_"))

    @classmethod
    def from_guild_member_avatar(cls, client, guild_id: Snowflake, user_id: Snowflake, hash: str):
        return cls(
            client,
            f"guilds/{guild_id}/users/{user_id}/avatars/" + "{0}{1}",
            hash,
            hash.startswith("a_")
        )

    # TODO: Add application related assets, achievement icon, stick pack banner, team icon, sticker

    @classmethod
    def from_role_icon(cls, client, role_id: Snowflake, hash: str):
        return cls(client, f"role-icons/{role_id}/" + "{0}{1}", hash)

    @classmethod
    def from_guild_scheduled_event_cover(cls, client, scheduled_event_id: Snowflake, hash: str):
        return cls(client, f"guild-events/{scheduled_event_id}/" + "{0}{1}", hash)