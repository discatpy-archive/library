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

from typing import Any, Dict, Optional

from .types.snowflake import *
from .types.user import *
from .abs import APIType
from .mixins import SnowflakeMixin
from .utils import get_avatar_url, get_default_avatar_url, get_banner_url

__all__ = (
    "UserAvatar",
    "UserBanner",
    "User",
)

class UserAvatar:
    """
    Represents the avatar of a user.

    Parameters
    ----------
    hash: :type:`str`
        The avatar hash for this user
    user_id: :type:`Snowflake`
        The user id for this user

    Attributes
    ----------
    raw_hash: :type:`str`
        The raw hash of the avatar's url
    url: :type:`str`
        The url for the user's avatar
    is_gif: :type:`bool`
        If the avatar is a GIF or not
    """
    def __init__(self, hash: Optional[str], user_id: Snowflake, discrim: str) -> None:
        self.raw_hash: Optional[str] = hash
        if self.raw_hash:
            self.url = get_avatar_url(user_id, self.raw_hash)
            self.is_gif: bool = self.raw_hash.startswith("a_")
        else:
            self.url = get_default_avatar_url(discrim)
            self.is_gif: bool = False

class UserBanner:
    """
    Represents the banner of a user.

    Parameters
    ----------
    hash: :type:`Optional[str]`
        The banner hash for this user. Might not be specified
    accent_color: :type:`Optional[int]`
        The banner accent color for this user. Should be specified even if the
        banner hash is
    user_id: :type:`Snowflake`
        The user id for this user

    Attributes
    ----------
    raw_hash: :type:`Optional[str]`
        The raw hash of the banner's url
    accent_color: :type:`Optional[str]`
        The accent color for this banner in hexadecimal form
    url: :type:`Optional[str]`
        The url for the user's banner
    is_gif: :type:`bool`
        If the banner is a GIF or not
    """
    def __init__(self, hash: Optional[str], accent_color: Optional[int], user_id: Snowflake) -> None:
        self.raw_hash: Optional[str] = None
        self.accent_color: Optional[str] = None
        self.url: Optional[str] = None
        self.is_gif: bool = False

        if hash and accent_color:
            self.raw_hash = hash if hash else None
            self.accent_color = hex(int(accent_color))
            self.url = get_banner_url(user_id, self.raw_hash)
            self.is_gif = self.raw_hash.startswith("a_")

class User(APIType, SnowflakeMixin):
    """
    Represents a User type. This shouldn't be initalized manually, the rest of the API
    should take care of that for you.

    Attributes
    ----------
    id: :type:`Snowflake`
        The id of this user
    name: :type:`str`
        The name of this user
    discriminator: :type:`str`
        The 4 digit tag for this user, also called a discriminator
    avatar: :type:`UserAvatar`
        The avatar for this user
    bot: :type:`bool`
        If this user is a bot or not
    tfa_enabled: :type:`bool`
        If this user has two-factor authentication or not
    banner: :type:`UserBanner`
        The banner for this user
    flags: :type:`int`
        The flags for this user
    premium_type: :type:`int`
        If the user has Nitro, Nitro Classic, or none
    public_flags: :type:`int`
        The public flags for this user
    """
    def __init__(
        self, 
        id: Snowflake,
        name: str,
        discrim: str,
        avatar: UserAvatar,
        bot: bool,
        tfa_enabled: bool,
        banner: UserBanner,
        flags: int,
        premium_type: int,
        public_flags: int
    ) -> None:
        self.raw_id = id
        self.name = name
        self.discriminator = discrim
        self.avatar = avatar
        self.bot = bot
        self.tfa_enabled = tfa_enabled,
        self.banner = banner
        # TODO: Locales
        self.flags = flags
        self.premium_type = premium_type
        self.public_flags = public_flags

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        name: str = d.get("username")
        discriminator: str = d.get("discriminator")
        avatar: UserAvatar = UserAvatar(d.get("avatar"), id, discriminator)
        bot: bool = d.get("bot", False)
        tfa_enabled: bool = d.get("mfa_enabled", False)
        accent_color: Optional[int] = int(d.get("accent_color")) if d.get("accent_color") is not None else None
        banner: UserBanner = UserBanner(d.get("banner"), accent_color, id)
        # TODO: Locales
        flags: int = d.get("flags", UserFlags.NONE)
        premium_type: int = d.get("premium_type", PremiumTypes.NONE)
        public_flags: int = d.get("public_flags", UserFlags.NONE)

        return cls(id, name, discriminator, avatar, bot, tfa_enabled, banner, flags, premium_type, public_flags)

    @property
    def mention(self) -> str:
        """
        Returns a string that can mention this user.
        """
        return f"<@{self.id}>"