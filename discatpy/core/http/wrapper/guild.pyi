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
from typing import List, Optional

from discord_typings import PartialChannelData, RoleData, WelcomeChannelData

from ...types import EllipsisOr, Snowflake

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
        user_id: EllipsisOr[Snowflake] = ...,
        action_type: EllipsisOr[int] = ...,
        before: EllipsisOr[Snowflake] = ...,
        limit: int = 50,
    ): ...
    async def create_guild(
        self,
        *,
        name: str,
        icon: EllipsisOr[str] = ...,
        verification_level: EllipsisOr[int] = ...,
        default_message_notifications: EllipsisOr[int] = ...,
        explicit_content_filter: EllipsisOr[int] = ...,
        roles: EllipsisOr[List[RoleData]] = ...,
        channels: EllipsisOr[List[PartialChannelData]] = ...,
        afk_channel_id: EllipsisOr[Snowflake] = ...,
        afk_timeout: EllipsisOr[int] = ...,
        system_channel_id: EllipsisOr[Snowflake] = ...,
        system_channel_flags: EllipsisOr[int] = ...,
    ): ...
    async def modify_guild(
        self,
        *,
        name: EllipsisOr[str] = ...,
        verification_level: EllipsisOr[Optional[int]] = ...,
        default_message_notifications: EllipsisOr[Optional[int]] = ...,
        explicit_content_filter: EllipsisOr[Optional[int]] = ...,
        afk_channel_id: EllipsisOr[Optional[Snowflake]] = ...,
        afk_timeout: EllipsisOr[int] = ...,
        icon: EllipsisOr[Optional[str]] = ...,
        owner_id: EllipsisOr[Snowflake] = ...,
        splash: EllipsisOr[Optional[str]] = ...,
        discovery_splash: EllipsisOr[Optional[str]] = ...,
        banner: EllipsisOr[Optional[str]] = ...,
        system_channel_id: EllipsisOr[Optional[Snowflake]] = ...,
        system_channel_flags: EllipsisOr[int] = ...,
        rules_channel_id: EllipsisOr[Optional[Snowflake]] = ...,
        public_updates_channel_id: EllipsisOr[Optional[Snowflake]] = ...,
        preferred_locale: EllipsisOr[Optional[str]] = ...,
        features: EllipsisOr[List[str]] = ...,
        description: EllipsisOr[Optional[str]] = ...,
        premium_progress_bar_enabled: EllipsisOr[bool] = ...,
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
        enabled: EllipsisOr[Optional[bool]] = ...,
        welcome_channels: EllipsisOr[Optional[List[WelcomeChannelData]]],
        description: EllipsisOr[Optional[str]] = ...,
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
        self, guild_id: Snowflake, *, limit: int = 1, after: EllipsisOr[Snowflake] = ...
    ): ...
    async def search_guild_members(self, guild_id: Snowflake, *, query: str, limit: int = 1): ...
    async def modify_guild_member(
        self,
        guild_id: Snowflake,
        user_id: Snowflake,
        *,
        nick: EllipsisOr[Optional[str]] = ...,
        roles: EllipsisOr[Optional[List[Snowflake]]] = ...,
        mute: EllipsisOr[Optional[bool]] = ...,
        deaf: EllipsisOr[Optional[bool]] = ...,
        channel_id: EllipsisOr[Optional[Snowflake]] = ...,
        communication_disabled_until: EllipsisOr[Optional[datetime]] = ...,
        reason: Optional[str] = None,
    ): ...
    async def modify_current_member(
        self,
        guild_id: Snowflake,
        *,
        nick: EllipsisOr[Optional[str]] = ...,
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
        before: EllipsisOr[Snowflake] = ...,
        after: EllipsisOr[Snowflake] = ...,
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
        permissions: EllipsisOr[str] = ...,
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
        name: EllipsisOr[Optional[str]] = ...,
        permissions: EllipsisOr[Optional[str]] = ...,
        color: EllipsisOr[Optional[int]] = ...,
        hoist: EllipsisOr[Optional[bool]] = ...,
        icon: EllipsisOr[Optional[str]] = ...,
        unicode_emoji: EllipsisOr[Optional[str]] = ...,
        mentionable: EllipsisOr[Optional[bool]] = ...,
        reason: Optional[str] = None,
    ): ...
    async def modify_guild_role_positions(
        self,
        guild_id: Snowflake,
        *,
        id: Snowflake,
        position: EllipsisOr[Optional[int]] = ...,
        reason: Optional[str] = None,
    ): ...
    async def delete_guild_role(self, guild_id: Snowflake, role_id: Snowflake): ...
