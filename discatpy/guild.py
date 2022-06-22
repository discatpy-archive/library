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

from datetime import datetime
from typing import Any, Dict, List, Optional, Union, overload

from discord_typings import EmojiData, GuildData, GuildMemberData, RoleData

from .asset import Asset
from .channel import RawChannel
from .object import DiscordObject
from .types.snowflake import *
from .user import User
from .utils import MISSING, MaybeMissing

__all__ = (
    "GuildRole",
    "Emoji",
    "GuildMember",
    "Guild",
)


class GuildRole(DiscordObject):
    """Represents a role contained in a guild.

    Attributes
    ----------
    guild: :type:`Guild`
        The guild this role is tied to.
    id: :type:`Snowflake`
        The id of this role.
    name: :type:`str`
        The name of this role.
    color: :type:`str`
        The hexadecimal id of the color of this role.
    pinned: :type:`bool`
        Whether or not this role is pinned.
    icon: :type:`Optional[Asset]`
        The icon of this role.
    unicode_emoji: :type:`Union[MISSING, None, str]`
        The unicode emoji for this role.
    position: :type:`int`
        The position of this role.
    managed: :type:`bool`
        Whether or not this role is managed via an integration.
    mentionable: :type:`bool`
        Whether or not this role can be mentioned by others.
    """

    __slots__ = (
        "guild",
        "id",
        "name",
        "color",
        "hoist",
        "icon",
        "unicode_emoji",
        "position",
        "permissions",
        "managed",
        "mentionable",
        "tags",
    )

    def __init__(self, d: RoleData, client):
        DiscordObject.__init__(self, d, client)

        self.guild: Optional[Guild] = None
        self._update(d)

    def _update(self, d: RoleData):
        self.id: Snowflake = d.get("id")
        self.name: str = d.get("name")
        self.color: str = hex(d.get("color"))
        self.pinned: bool = d.get("hoist")
        icon_hash: Optional[str] = d.get("icon")
        self.icon: Optional[Asset] = None
        if icon_hash is not None:
            self.icon = Asset.from_role_icon(self.client, self.id, icon_hash)
        self.unicode_emoji: Optional[str] = d.get("unicode_emoji")
        self.position: int = d.get("position")
        self.permissions: str = d.get("permissions")
        self.managed: bool = d.get("managed")
        self.mentionable: bool = d.get("mentionable")
        # TODO: tags

    def to_dict(self) -> RoleData:
        ret_dict: RoleData = {
            "id": self.id,
            "name": self.name,
            "color": int(self.color, 16),
            "hoist": self.pinned,
            "position": self.position,
            "permissions": self.permissions,
            "managed": self.managed,
            "mentionable": self.mentionable,
        }

        if self.icon:
            ret_dict["icon"] = self.icon.key

        if self.unicode_emoji:
            ret_dict["unicode_emoji"] = self.unicode_emoji

        return ret_dict

    def _set_guild(self, new_guild: Guild):
        self.guild = new_guild


class Emoji(DiscordObject):
    """Represents an emoji that may or may not be a custom emoji from a Guild.

    Attributes
    ----------
    guild: :type:`Optional[Guild]`
        The guild this emoji is tied to.
    id: :type:`Optional[Snowflake]`
        The id of this emoji.
    name: :type:`Optional[str]`
        The name of this emoji.
    roles: :type:`Union[MISSING, List[GuildRole]]`
        The roles that can use this emoji.
    creator: :type:`Union[MISSING, User]`
        The user object that added this emoji to the guild.
    require_colons: :type:`Union[MISSING, bool]`
        Whether or not this emoji requires colons to be used.
    managed: :type:`Union[MISSING, bool]`
        Whether or not this emoji is managed.
    animated: :type:`Union[MISSING, bool]`
        Whether or not this emoji is animated.
    available: :type:`Union[MISSING, bool]`
        Whether or not members can use this emoji. This can be False if
        the guild loses a boost level and loses extra emoji slots.
    """

    __slots__ = (
        "guild",
        "roles",
        "id",
        "name",
        "user",
        "require_colons",
        "managed",
        "animated",
        "available",
    )

    def __init__(self, d: EmojiData, client):
        DiscordObject.__init__(self, d, client)

        self.guild: Optional[Guild] = None
        self.roles: Union[MISSING, List[GuildRole]] = None
        self._update(d)

    def _update(self, d: EmojiData):
        self.id: Optional[Snowflake] = d.get("id")
        self.name: Optional[str] = d.get("name")
        self._role_ids: Union[MISSING, List[Snowflake]] = (
            [i for i in d.get("roles")]
            if d.get("roles", MISSING) is not MISSING
            else MISSING
        )
        self.creator: Union[MISSING, User] = (
            User(d.get("user"), self.client)
            if d.get("user", MISSING) is not MISSING
            else MISSING
        )
        self.require_colons: Union[MISSING, bool] = d.get("require_colons", MISSING)
        self.managed: Union[MISSING, bool] = d.get("managed", MISSING)
        self.animated: Union[MISSING, bool] = d.get("animated", MISSING)
        self.available: Union[MISSING, bool] = d.get("available", MISSING)

    def _set_guild(self, new_guild: Guild):
        self.guild = new_guild
        # TODO: initialize roles after setting new guild


class GuildMember(DiscordObject):
    """Represents a member of a guild.

    Attributes
    ----------
    guild: :type:`Guild`
        The guild this member is tied to.
    user: :type:`Optional[User]`
        The underlying user object tied to this member. This may or may not
        be missing.
    nick: :type:`Optional[str]`
        The nickname for this member.
    avatar: :type:`Optional[Asset]`
        The guild specific avatar for this member.
    joined_at: :type:`datetime`
        The date and time when this member joined the guild it's tied to.
    premium_since: :type:`Optional[datetime]`
        TODO: Determine what this represents
    deaf: :type:`bool`
        Whether or not this member is currently deaf in a voice channel.
    mute: :type:`bool`
        Whether or not this member is currently muted in a voice channel.
    pending: :type:`Optional[bool]`
        Whether or not this member has not passed the membership screening.
    timeout_until: :type:`Optional[datetime]`
        The date and time of when this member will have its time out expire, if
        they are currently timed out.
    """

    __slots__ = (
        "guild",
        "roles",
        "avatar",
        "user",
        "nick",
        "joined_at",
        "premium_since",
        "deaf",
        "mute",
        "pending",
        "permissions",
        "timeout_until",
    )

    def __init__(self, d: GuildMemberData, client):
        DiscordObject.__init__(self, d, client)

        self.guild: Optional[Guild] = None
        self.roles: Optional[List[GuildRole]] = None
        self.avatar: Optional[Asset] = None
        self._update(d)

    def _update(self, d: GuildMemberData):
        self.user: Union[MISSING, User] = (
            User.from_dict(self.client, d.get("user"))
            if d.get("user", MISSING) is not MISSING
            else MISSING
        )
        self.nick: Union[MISSING, Optional[str]] = d.get("nick", MISSING)
        self._avatar_hash: Optional[str] = d.get("avatar")
        self._role_ids: List[Snowflake] = d.get("roles")
        self.joined_at: datetime = datetime.fromisoformat(d.get("joined_at"))
        self.premium_since: Optional[datetime] = (
            datetime.fromisoformat(d.get("premium_since"))
            if d.get("premium_since") is not None
            else None
        )
        self.deaf: bool = d.get("deaf")
        self.mute: bool = d.get("mute")
        self.pending: Optional[bool] = d.get("pending")
        raw_timeout_until: Union[MISSING, Optional[str]] = d.get(
            "communication_disabled_until", MISSING
        )
        self.timeout_until: Union[MISSING, Optional[str]] = MISSING
        if raw_timeout_until is not MISSING:
            self.timeout_until = (
                datetime.fromisoformat(raw_timeout_until)
                if raw_timeout_until is not None
                else None
            )

    def to_dict(self) -> GuildMemberData:
        ret_dict: GuildMemberData = {"deaf": self.deaf, "mute": self.mute}

        if self.nick:
            ret_dict["nick"] = self.nick

        if self.roles:
            ret_dict["roles"] = [r.to_dict() for r in self.roles]

        if self.timeout_until:
            ret_dict["communication_disabled_until"] = self.timeout_until.isoformat()

        return ret_dict

    def _set_guild(self, guild: Guild):
        self.guild = guild
        self.avatar = (
            Asset.from_guild_member_avatar(
                self.client, self.guild.id, self.user.id, self._avatar_hash
            )
            if self._avatar_hash is not None
            else None
        )

    async def edit(
        self,
        /,
        nick: Optional[str] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
        timeout_until: Optional[datetime] = None,
    ):
        if nick:
            self.nick = nick

        if self.user.id == self.client.me.id:
            await self.client.http.modify_current_guild_member(self.guild.id, self.nick)
        else:
            if mute is not None:
                self.mute = mute

            if deaf is not None:
                self.deaf = deaf

            if timeout_until:
                self.timeout_until = timeout_until

            await self.client.http.modify_guild_member(
                self.guild.id, self.user.id, self.to_dict()
            )

    async def add_role(self, role: GuildRole):
        if self.guild.id != role.guild.id:
            return

        self.roles.append(role)
        await self.client.http.add_guild_member_role(
            self.guild.id, self.user.id, role.id
        )

    async def remove_role(self, role: GuildRole):
        if self.guild.id != role.guild.id:
            return

        if role in self.roles:
            self.roles.remove(role)
        await self.client.http.remove_guild_member_role(
            self.guild.id, self.user.id, role.id
        )

    async def kick(self):
        await self.guild.kick(self)


class Guild(DiscordObject):
    __slots__ = (
        "id",
        "name",
        "icon",
        "splash",
        "discovery_splash",
        "permissions",
        "afk_timeout",
        "verification_level",
        "default_message_notifications",
        "explicit_content_filter",
        "roles",
        "emojis",
        "features",
        "mfa_level",
        "vanity_url_code",
        "description",
        "banner",
        "premium_tier",
        "premium_subscription_count",
        "preferred_locale",
        "nsfw_level",
        "premium_progress_bar_enabled",
    )

    def __init__(self, d: GuildData, client):
        DiscordObject.__init__(d, client)
        self._update(d)

    def _update(self, d: GuildData):
        self.id: Snowflake = d.get("id")
        self.name: str = d.get("name")
        self._icon_hash: Optional[str] = d.get("icon")
        self._splash_hash: Optional[str] = d.get("splash")
        self._discovery_splash_hash: Optional[str] = d.get("discovery_splash")
        self._owner_id: Snowflake = d.get("owner_id")
        self.permissions: Union[MISSING, str] = d.get("permissions", MISSING)
        self._afk_channel_id: Snowflake = d.get("afk_channel_id")
        self.afk_timeout: int = d.get("afk_timeout")
        # TODO: widgets
        self.verification_level: int = d.get("verification_level")
        self.default_message_notifications: int = d.get("default_message_notifications")
        self.explicit_content_filter: int = d.get("explicit_content_filter")
        self.roles: List[GuildRole] = [
            GuildRole.from_dict(self.client, r) for r in d.get("roles")
        ]
        for r in self.roles:
            r._set_guild(self)
        self.emojis: List[Emoji] = [Emoji(e, self.client) for e in d.get("emojis")]
        for e in self.emojis:
            e._set_guild(self)
        self.features: List[str] = d.get("features")
        self.mfa_level: int = d.get("mfa_level")
        self._system_channel_id: Optional[Snowflake] = d.get("system_channel_id")
        self.system_channel_flags: int = d.get("system_channel_flags")
        self._rules_channel_id: Optional[Snowflake] = d.get("rules_channel_id")
        # TODO: channels, threads, presences, max_presences?, max_members?
        self.vanity_url_code: Optional[str] = d.get("vanity_url_code")
        self.description: Optional[str] = d.get("description")
        self.banner_hash: Optional[str] = d.get("banner")
        self.premium_tier: int = d.get("premium_tier")
        self.premium_subscription_count: Union[MISSING, Optional[int]] = d.get(
            "premium_subscription_count", MISSING
        )
        self.preferred_locale: str = d.get("preferred_locale")
        self._public_updates_channel_id: Optional[Snowflake] = d.get(
            "public_updates_channel_id"
        )
        # TODO: max_video_channel_users, approximate_member_count, welcome_screen
        self.nsfw_level: int = d.get("nsfw_level")
        # TODO: stage_instances, stickers, guild_scheduled_events
        self.premium_progress_bar_enabled: bool = d.get("premium_progress_bar_enabled")

    @property
    async def owner(self):
        raw_owner = await self.client.http.get_guild_member(self.id, self._owner_id)
        return GuildMember.from_dict(self.client, raw_owner)

    @property
    async def afk_channel(self):
        return self.client.grab(self._afk_channel_id, RawChannel)

    @property
    async def system_channel(self):
        return self.client.grab(self._system_channel_id, RawChannel)

    @property
    async def rules_channel(self):
        return self.client.grab(self._rules_channel_id, RawChannel)

    @property
    async def public_updates_channel_id(self):
        return self.client.grab(self._public_updates_channel_id, RawChannel)

    async def fetch_all_channels(self):
        channels = await self.client.http.get_channels(self.id)
        return [RawChannel.from_dict(self.client, c) for c in channels]

    async def fetch_all_members(self, limit: int = 1, after: Snowflake = 0):
        members = await self.client.http.get_guild_members(self.id, limit, after)
        return [GuildMember.from_dict(self.client, m) for m in members]

    async def kick(self, member: GuildMember):
        await self.client.http.remove_guild_member(self.id, member.user.id)
