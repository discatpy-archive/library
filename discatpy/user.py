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

from typing import Any, Dict, Optional, Union, overload

from discord_typings import UserData

from .asset import Asset
from .object import DiscordObject
from .types.snowflake import *
from .utils import MISSING, MaybeMissing

__all__ = ("User",)


class User(DiscordObject):
    """Represents a User type.

    Attributes
    ----------
    id: :type:`Snowflake`
        The id of this user
    name: :type:`str`
        The name of this user
    discriminator: :type:`str`
        The 4 digit tag for this user, also called a discriminator
    avatar: :type:`Optional[Asset]`
        The avatar for this user
    bot: :type:`Union[MISSING, bool]`
        If this user is a bot or not
    tfa_enabled: :type:`Union[MISSING, bool]`
        If this user has two-factor authentication or not
    banner: :type:`Union[MISSING, None, Asset]`
        The banner for this user
    flags: :type:`Union[MISSING, int]`
        The flags for this user
    premium_type: :type:`Union[MISSING, int]`
        If the user has Nitro, Nitro Classic, or none
    public_flags: :type:`Union[MISSING, int]`
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

    @overload
    def __init__(self, d: UserData, client):
        ...

    def __init__(self, d: Dict[str, Any], client):
        DiscordObject.__init__(self, d, client)
        self._update(d)

    def _update(self, d: Dict[str, Any]):
        self.id: Snowflake = d.get("id")
        self.name: str = d.get("username")
        self.discriminator: str = d.get("discriminator")
        self.avatar: Optional[Asset] = (
            Asset.from_user_avatar(self.client, self.id, d.get("avatar"))
            if d.get("avatar")
            else Asset.from_default_user_avatar(self.client, int(self.discriminator))
        )
        self.bot: MaybeMissing[bool] = d.get("bot", MISSING)
        self.tfa_enabled: MaybeMissing[bool] = d.get("mfa_enabled", MISSING)
        self.accent_color: MaybeMissing[Optional[int]] = MISSING
        if d.get("accent_color", MISSING) is not MISSING:
            self.accent_color = (
                int(d.get("accent_color"))
                if d.get("accent_color") is not None
                else None
            )
        _banner_hash: MaybeMissing[Optional[str]] = d.get("banner", MISSING)
        self.banner: MaybeMissing[Optional[Asset]] = MISSING
        if _banner_hash is not MISSING:
            self.banner = (
                Asset.from_user_banner(self.client, self.id, _banner_hash)
                if _banner_hash is not None
                else None
            )
        # TODO: Locales
        self.flags: MaybeMissing[int] = d.get("flags", MISSING)
        self.premium_type: MaybeMissing[int] = d.get("premium_type", MISSING)
        self.public_flags: MaybeMissing[int] = d.get("public_flags", MISSING)

    @property
    def mention(self) -> str:
        """
        Returns a string that can mention this user.
        """
        return f"<@{self.id}>"
