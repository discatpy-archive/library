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

from datetime import datetime
from typing import Any, Dict, List, Optional

from .types.snowflake import Snowflake
from .abs import APIType
from .asset import Asset
from .mixins import SnowflakeMixin
from .user import User

__all__ = (
    "GuildRole",
    "GuildMember",
    "Guild",
)

class GuildRole(APIType, SnowflakeMixin):
    def __init__(
        self, 
        d: Dict[str, Any], 
        client,
        id: Snowflake,
        name: str,
        color: int,
        pinned: bool,
        icon_hash: Optional[str],
        unicode_emoji: Optional[str],
        position: int,
        managed: bool,
        mentionable: bool
    ):
        super().__init__(d, client)

        self.raw_id = id
        self.name = name
        self.color = hex(color)
        self.pinned = pinned
        self.icon = Asset.from_role_icon(self.client, self.id, icon_hash) if icon_hash is not None else None
        self.unicode_emoji = unicode_emoji
        self.position = position
        self.managed = managed
        self.mentionable = mentionable

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        name: str = d.get("name")
        color: int = d.get("color")
        pinned: bool = d.get("hoist")
        icon_hash: Optional[str] = d.get("icon")
        unicode_emoji: Optional[str] = d.get("unicode_emoji")
        position: int = d.get("position")
        # TODO: permissions
        managed: bool = d.get("managed")
        mentionable: bool = d.get("mentionable")
        # TODO: tags

        return cls(d, client, id, name, color, pinned, icon_hash, unicode_emoji, position, managed, mentionable)


class GuildMember(APIType):
    def __init__(
        self,
        d: Dict[str, Any],
        client,
        user: Optional[User],
        nick: Optional[str],
        avatar_hash: Optional[str],
        joined_at: datetime,
        premium_since: Optional[datetime],
        deaf: bool,
        mute: bool,
        pending: Optional[bool],
        timeout_until: Optional[datetime]
    ) -> None:
        super().__init__(d, client)

        self.user = user
        self.nick = nick
        self.avatar = avatar_hash # initalized later by _set_guild
        self.joined_at = joined_at
        self.premium_since = premium_since
        self.deaf = deaf
        self.mute = mute
        self.pending = pending
        self.timeout_until = timeout_until

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        user: Optional[User] = User.from_dict(client, d.get("user")) if d.get("user") is not None else None
        nick: Optional[str] = d.get("nick")
        avatar_hash: Optional[str] = d.get("avatar")
        # TODO: roles
        joined_at: datetime = datetime.fromisoformat(d.get("joined_at"))
        premium_since: Optional[datetime] = datetime.fromisoformat(d.get("premium_since")) if d.get("premium_since") is not None else None
        deaf: bool = d.get("deaf")
        mute: bool = d.get("mute")
        pending: Optional[bool] = d.get("pending")
        # TODO: permissions
        timeout_until: Optional[datetime] = datetime.fromisoformat(d.get("communication_disabled_until")) if d.get("communication_disabled_until") is not None else None

        return cls(d, client, user, nick, avatar_hash, joined_at, premium_since, deaf, mute, pending, timeout_until)

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = {"deaf":self.deaf, "mute":self.mute}

        if self.nick:
            ret_dict["nick"] = self.nick

        # TODO: roles

        if self.timeout_until:
            ret_dict["communication_disabled_until"] = self.timeout_until.isoformat()

        return ret_dict

    def _set_guild(self, guild: "Guild"):
        self.guild = guild
        self.avatar = Asset.from_guild_member_avatar(self.client, self.guild.id, self.user.id, self.avatar) if self.avatar is not None else None

    async def edit(self, /, nick: Optional[str] = None, mute: Optional[bool] = None, deaf: Optional[bool] = None, timeout_until: Optional[datetime] = None):
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

            await self.client.http.modify_guild_member(self.guild.id, self.user.id, self.to_dict())

    async def add_role(self, role: GuildRole):
        await self.client.http.add_guild_member_role(self.guild.id, self.user.id, role.id)

    async def remove_role(self, role: GuildRole):
        await self.client.http.remove_guild_member_role(self.guild.id, self.user.id, role.id)

class Guild(APIType, SnowflakeMixin):
    def __init__(
        self, 
        d: Dict[str, Any], 
        client, 
        id: Snowflake, 
        name: str, 
        icon_hash: Optional[str],
        splash_hash: Optional[str],
        discovery_splash_hash: Optional[str],
        owner_id: Snowflake,
        afk_channel_id: Snowflake,
        afk_timeout: int,
        verification_level: int,
        default_message_notifications: int,
        explicit_content_filter: int,
        features: List[str],
        mfa_level: int,
        system_channel_id: Optional[Snowflake],
        rules_channel_id: Optional[Snowflake],
        vanity_url_code: Optional[str],
        description: Optional[str],
        banner_hash: Optional[str],
        premium_tier: int,
        premium_subscription_count: Optional[int],
        preferred_locale: str,
        public_updates_channel_id: Optional[Snowflake],
        nsfw_level: int,
        premium_progress_bar_enabled: bool  
    ):
        super().__init__(d, client)

        self.raw_id = id
        self.name = name
        self.icon = Asset.from_guild_icon(self.client, self.id, icon_hash) if icon_hash is not None else None
        self.splash = Asset.from_guild_splash(self.client, self.id, splash_hash) if splash_hash is not None else None
        self.discovery_splash = Asset.from_guild_discovery_splash(self.client, self.id, discovery_splash_hash) if discovery_splash_hash else None
        self._owner_id = owner_id
        self._afk_channel_id = afk_channel_id
        self.afk_timeout = afk_timeout
        self.verification_level = verification_level
        self.default_message_notifications = default_message_notifications
        self.explicit_content_filter = explicit_content_filter
        self.features = features
        self.mfa_level = mfa_level
        self._system_channel_id = system_channel_id
        self._rules_channel_id = rules_channel_id
        self.vanity_url_code = vanity_url_code
        self.description = description
        self.banner = Asset.from_guild_banner(self.client, self.id, banner_hash) if banner_hash is not None else None
        self.premium_tier = premium_tier
        self.premium_subscription_count = premium_subscription_count
        self.preferred_locale = preferred_locale
        self._public_updates_channel_id = public_updates_channel_id
        self.nsfw_level = nsfw_level
        self.premium_progress_bar_enabled = premium_progress_bar_enabled

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        name: str = d.get("name")
        icon_hash: Optional[str] = d.get("icon")
        splash_hash: Optional[str] = d.get("splash")
        discovery_splash_hash: Optional[str] = d.get("discovery_splash")
        owner_id: Snowflake = d.get("owner_id")
        # TODO: permissions
        afk_channel_id: Snowflake = d.get("afk_channel_id")
        afk_timeout: int = d.get("afk_timeout")
        # TODO: widgets
        verification_level: int = d.get("verification_level")
        default_message_notifications: int = d.get("default_message_notifications")
        explicit_content_filter: int = d.get("explicit_content_filter")
        # TODO: roles, emojis
        features: List[str] = d.get("features")
        mfa_level: int = d.get("mfa_level")
        system_channel_id: Optional[Snowflake] = d.get("system_channel_id")
        # TODO: system channel flags
        rules_channel_id: Optional[Snowflake] = d.get("rules_channel_id")
        # TODO: channels, threads, presences, max_presences?, max_members?
        vanity_url_code: Optional[str] = d.get("vanity_url_code")
        description: Optional[str] = d.get("description")
        banner_hash: Optional[str] = d.get("banner")
        premium_tier: int = d.get("premium_tier")
        premium_subscription_count: Optional[int] = d.get("premium_subscription_count")
        preferred_locale: str = d.get("preferred_locale")
        public_updates_channel_id: Optional[Snowflake] = d.get("public_updates_channel_id")
        # TODO: max_video_channel_users, approximate_member_count, welcome_screen
        nsfw_level: int = d.get("nsfw_level")
        # TODO: stage_instances, stickers, guild_scheduled_events
        premium_progress_bar_enabled: bool = d.get("premium_progress_bar_enabled")

        return cls(
            d, 
            client, 
            id, 
            name, 
            icon_hash, 
            splash_hash, 
            discovery_splash_hash, 
            owner_id, 
            afk_channel_id, 
            afk_timeout,
            verification_level,
            default_message_notifications,
            explicit_content_filter,
            features,
            mfa_level,
            system_channel_id,
            rules_channel_id,
            vanity_url_code,
            description,
            banner_hash,
            premium_tier,
            premium_subscription_count,
            preferred_locale,
            public_updates_channel_id,
            nsfw_level,
            premium_progress_bar_enabled
        )

    @property
    async def owner(self):
        raw_owner = await self.client.http.get_guild_member(self.id, self._owner_id)
        return GuildMember.from_dict(self.client, raw_owner)

    async def fetch_all_channels(self):
        channels = await self.client.http.get_channels(self.id)
        # TODO: convert channels into their appropriate objects

    async def fetch_all_members(self, limit: int = 1, after: Snowflake = 0):
        members = await self.client.http.get_guild_members(self.id, limit, after)
        return [GuildMember.from_dict(self.client, m) for m in members]