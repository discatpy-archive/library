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

from typing import Optional

from discord_typings import UserData

from ...core.types import EllipsisOr
from ..utils import parse_data
from .asset import Asset
from .object import DiscordObject

__all__ = ("User",)


class User(DiscordObject):
    """Represents a User type.

    Attributes
    ----------
    id: :class:`int`
        The id of this user
    name: :class:`str`
        The name of this user
    discriminator: :class:`str`
        The 4 digit tag for this user, also called a discriminator
    avatar: Optional[:class:`Asset`]
        The avatar for this user
    bot: EllipsisOr[:class:`bool`]
        If this user is a bot or not
    tfa_enabled: EllipsisOr[:class:`bool`]
        If this user has two-factor authentication or not
    banner: EllipsisOr[Optional[:class:`Asset`]]
        The banner for this user
    flags: EllipsisOr[:class:`int`]
        The flags for this user
    premium_type: EllipsisOr[:class:`int`]
        If the user has Nitro, Nitro Classic, or none
    public_flags: EllipsisOr[:class:`int`]
        The public flags for this user
    """

    __slots__ = (
        "id",
        "name",
        "discriminator",
        "avatar",
        "bot",
        "tfa_enabled",
        "accent_color",
        "banner",
        "flags",
        "premium_type",
        "public_flags",
    )

    def __init__(self, *, data: UserData, bot):
        DiscordObject.__init__(self, data=data, bot=bot)

        self.id: int = int(data["id"])
        self.name: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[Asset] = parse_data(
            data,
            "avatar",
            Asset.from_user_avatar,
            (self._bot, self.id, data["avatar"]),
            default=Asset.from_default_user_avatar(self._bot, int(self.discriminator)),
        )
        self.bot: EllipsisOr[bool] = data.get("bot", ...)
        self.tfa_enabled: EllipsisOr[bool] = data.get("mfa_enabled", ...)
        self.accent_color: EllipsisOr[Optional[int]] = parse_data(data, "accent_color")
        self.banner: EllipsisOr[Optional[Asset]] = parse_data(
            data,
            "banner",
            Asset.from_user_banner,
            (self._bot, self.id, data.get("banner")),
        )
        # TODO: Locales
        self.flags: EllipsisOr[int] = data.get("flags", ...)
        self.premium_type: EllipsisOr[int] = data.get("premium_type", ...)
        self.public_flags: EllipsisOr[int] = data.get("public_flags", ...)

    @property
    def mention(self) -> str:
        """:class:`str` A string that can mention this user."""
        return f"<@{self.id}>"
