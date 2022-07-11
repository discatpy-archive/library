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
from typing import Optional

from discord_typings import PartialChannelData, RoleData, WelcomeChannelData

from ...types import MISSING, List, MissingOr, Snowflake

class GuildEndpointMixin:
    async def get_guild(self, guild_id: Snowflake, *, with_counts: bool = False): ...
    async def get_guild_preview(self, guild_id: Snowflake): ...
    async def get_guild_prune_count(
        self, guild_id: Snowflake, *, days: int = 7, include_roles: Optional[str] = None
    ): ...
    async def get_guild_voice_regions(self, guild_id: Snowflake): ...
    async def get_guild_invites(self, guild_id: Snowflake): ...
    async def get_guild_integrations(self, guild_id: Snowflake): ...
    async def get_guild_widget_settings(self, guild_id: Snowflake): ...
    async def get_guild_widget(self, guild_id: Snowflake): ...
    async def get_guild_vanity_url(self, guild_id: Snowflake): ...
    async def get_guild_widget_image(self, guild_id: Snowflake, *, style: str = "shield"): ...
    async def get_guild_welcome_screen(self, guild_id: Snowflake): ...
    async def get_guild_audit_log(
        self,
        guild_id: Snowflake,
        *,
        user_id: MissingOr[Snowflake] = MISSING,
        action_type: MissingOr[int] = MISSING,
        before: MissingOr[Snowflake] = MISSING,
        limit: int = 50,
    ): ...
    async def create_guild(
        self,
        *,
        name: str,
        icon: MissingOr[str] = MISSING,
        verification_level: MissingOr[int] = MISSING,
        default_message_notifications: MissingOr[int] = MISSING,
        explicit_content_filter: MissingOr[int] = MISSING,
        roles: MissingOr[List[RoleData]] = MISSING,
        channels: MissingOr[List[PartialChannelData]] = MISSING,
        afk_channel_id: MissingOr[Snowflake] = MISSING,
        afk_timeout: MissingOr[int] = MISSING,
        system_channel_id: MissingOr[Snowflake] = MISSING,
        system_channel_flags: MissingOr[int] = MISSING,
    ): ...
    async def modify_guild(
        self,
        *,
        name: MissingOr[str] = MISSING,
        verification_level: MissingOr[Optional[int]] = MISSING,
        default_message_notifications: MissingOr[Optional[int]] = MISSING,
        explicit_content_filter: MissingOr[Optional[int]] = MISSING,
        afk_channel_id: MissingOr[Optional[Snowflake]] = MISSING,
        afk_timeout: MissingOr[int] = MISSING,
        icon: MissingOr[Optional[str]] = MISSING,
        owner_id: MissingOr[Snowflake] = MISSING,
        splash: MissingOr[Optional[str]] = MISSING,
        discovery_splash: MissingOr[Optional[str]] = MISSING,
        banner: MissingOr[Optional[str]] = MISSING,
        system_channel_id: MissingOr[Optional[Snowflake]] = MISSING,
        system_channel_flags: MissingOr[int] = MISSING,
        rules_channel_id: MissingOr[Optional[Snowflake]] = MISSING,
        public_updates_channel_id: MissingOr[Optional[Snowflake]] = MISSING,
        preferred_locale: MissingOr[Optional[str]] = MISSING,
        features: MissingOr[List[str]] = MISSING,
        description: MissingOr[Optional[str]] = MISSING,
        premium_progress_bar_enabled: MissingOr[bool] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_mfa_level(self, guild_id: Snowflake, *, level: int): ...
    async def modify_guild_widget(
        self,
        guild_id: Snowflake,
        *,
        enabled: bool,
        channel_id: Optional[Snowflake],
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_welcome_screen(
        self,
        guild_id: Snowflake,
        *,
        enabled: MissingOr[Optional[bool]] = MISSING,
        welcome_channels: MissingOr[Optional[List[WelcomeChannelData]]],
        description: MissingOr[Optional[str]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def delete_guild(self, guild_id: Snowflake): ...
    async def delete_guild_integrations(self, guild_id: Snowflake): ...
    async def begin_guild_prune(
        self,
        guild_id: Snowflake,
        *,
        days: int = 7,
        compute_prune_count: bool = True,
        include_roles: Optional[List[Snowflake]] = None,
    ): ...

class GuildMemberEndpointMixin:
    async def get_guild_member(self, guild_id: Snowflake, user_id: Snowflake): ...
    async def list_guild_members(
        self, guild_id: Snowflake, *, limit: int = 1, after: MissingOr[Snowflake] = MISSING
    ): ...
    async def search_guild_members(self, guild_id: Snowflake, *, query: str, limit: int = 1): ...
    async def modify_guild_member(
        self,
        guild_id: Snowflake,
        user_id: Snowflake,
        *,
        nick: MissingOr[Optional[str]] = MISSING,
        roles: MissingOr[Optional[List[Snowflake]]] = MISSING,
        mute: MissingOr[Optional[bool]] = MISSING,
        deaf: MissingOr[Optional[bool]] = MISSING,
        channel_id: MissingOr[Optional[Snowflake]] = MISSING,
        communication_disabled_until: MissingOr[Optional[datetime]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def modify_current_member(
        self,
        guild_id: Snowflake,
        *,
        nick: MissingOr[Optional[str]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def remove_guild_member(
        self, guild_id: Snowflake, user_id: Snowflake, *, reason: Optional[str] = None
    ): ...
    async def add_guild_member_role(
        self, guild_id: Snowflake, user_id: Snowflake, role_id: Snowflake
    ): ...
    async def remove_guild_member_role(
        self, guild_id: Snowflake, user_id: Snowflake, role_id: Snowflake
    ): ...
    async def get_guild_ban(self, guild_id: Snowflake, user_id: Snowflake): ...
    async def get_guild_bans(
        self,
        guild_id: Snowflake,
        *,
        limit: int = 1000,
        before: MissingOr[Snowflake] = MISSING,
        after: MissingOr[Snowflake] = MISSING,
    ): ...
    async def create_guild_ban(
        self,
        guild_id: Snowflake,
        user_id: Snowflake,
        *,
        delete_message_days: int = 0,
        reason: Optional[str] = None,
    ): ...
    async def remove_guild_ban(
        self, guild_id: Snowflake, user_id: Snowflake, *, reason: Optional[str] = None
    ): ...

class GuildRoleEndpointMixin:
    async def get_guild_roles(self, guild_id: Snowflake): ...
    async def create_guild_role(
        self,
        guild_id: Snowflake,
        *,
        name: str = "new role",
        permissions: MissingOr[str] = MISSING,
        color: int = 0,
        hoist: bool = False,
        icon: Optional[str] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: bool = False,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_role(
        self,
        guild_id: Snowflake,
        role_id: Snowflake,
        *,
        name: MissingOr[Optional[str]] = MISSING,
        permissions: MissingOr[Optional[str]] = MISSING,
        color: MissingOr[Optional[int]] = MISSING,
        hoist: MissingOr[Optional[bool]] = MISSING,
        icon: MissingOr[Optional[str]] = MISSING,
        unicode_emoji: MissingOr[Optional[str]] = MISSING,
        mentionable: MissingOr[Optional[bool]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_role_positions(
        self,
        guild_id: Snowflake,
        *,
        id: Snowflake,
        position: MissingOr[Optional[int]] = MISSING,
        reason: Optional[str] = None,
    ): ...
    async def delete_guild_role(self, guild_id: Snowflake, role_id: Snowflake): ...
