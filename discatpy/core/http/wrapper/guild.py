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

from ...types import MISSING, MissingOr, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = (
    "GuildEndpointMixin",
    "GuildMemberEndpointMixin",
    "GuildRoleEndpointMixin",
)


class GuildEndpointMixin(CoreMixin):
    get_guild = APIEndpointData(
        "GET",
        "/guilds/{guild_id}",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("with_counts", bool, False),
        ],
    )
    get_guild_preview = APIEndpointData(
        "GET", "/guilds/{guild_id}/preview", format_args={"guild_id": Snowflake}
    )
    get_guild_prune_count = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/prune",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("days", int, 7),
            ("include_roles", Optional[str], None),
        ],
    )
    get_guild_voice_regions = APIEndpointData(
        "GET", "/guilds/{guild_id}/regions", format_args={"guild_id": Snowflake}
    )
    get_guild_invites = APIEndpointData(
        "GET", "/guilds/{guild_id}/invites", format_args={"guild_id": Snowflake}
    )
    get_guild_integrations = APIEndpointData(
        "GET", "/guilds/{guild_id}/integrations", format_args={"guild_id": Snowflake}
    )
    get_guild_widget_settings = APIEndpointData(
        "GET", "/guilds/{guild_id}/widget", format_args={"guild_id": Snowflake}
    )
    get_guild_widget = APIEndpointData(
        "GET", "/guilds/{guild_id}/widget.json", format_args={"guild_id": Snowflake}
    )
    get_guild_vanity_url = APIEndpointData(
        "GET", "/guilds/{guild_id}/vanity-url", format_args={"guild_id": Snowflake}
    )
    get_guild_widget_image = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/widget.png",
        format_args={"guild_id": Snowflake},
        param_args=[("style", str, '"shield"')],
    )
    get_guild_welcome_screen = APIEndpointData(
        "GET", "/guilds/{guild_id}/welcome-screen", format_args={"guild_id": Snowflake}
    )
    get_guild_audit_log = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/audit-logs",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("user_id", MissingOr[Snowflake], MISSING),
            ("action_type", MissingOr[int], MISSING),
            ("before", MissingOr[Snowflake], MISSING),
            ("limit", int, 50),
        ],
    )
    create_guild = APIEndpointData(
        "POST",
        "/guilds",
        param_args=[
            ("name", str),
            ("icon", MissingOr[str], MISSING),
            ("verification_level", MissingOr[int], MISSING),
            ("default_message_notifications", MissingOr[int], MISSING),
            ("explicit_content_filter", MissingOr[int], MISSING),
            ("roles", MissingOr[List[RoleData]], MISSING),
            ("channels", MissingOr[List[PartialChannelData]], MISSING),
            ("afk_channel_id", MissingOr[Snowflake], MISSING),
            ("afk_timeout", MissingOr[int], MISSING),
            ("system_channel_id", MissingOr[Snowflake], MISSING),
            ("system_channel_flags", MissingOr[int], MISSING),
        ],
    )
    modify_guild = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", MissingOr[str], MISSING),
            ("verification_level", MissingOr[Optional[int]], MISSING),
            ("default_message_notifications", MissingOr[Optional[int]], MISSING),
            ("explicit_content_filter", MissingOr[Optional[int]], MISSING),
            ("afk_channel_id", MissingOr[Optional[Snowflake]], MISSING),
            ("afk_timeout", MissingOr[int], MISSING),
            ("icon", MissingOr[Optional[str]], MISSING),
            ("owner_id", MissingOr[Snowflake], MISSING),
            ("splash", MissingOr[Optional[str]], MISSING),
            ("discovery_splash", MissingOr[Optional[str]], MISSING),
            ("banner", MissingOr[Optional[str]], MISSING),
            ("system_channel_id", MissingOr[Optional[Snowflake]], MISSING),
            ("system_channel_flags", MissingOr[int], MISSING),
            ("rules_channel_id", MissingOr[Optional[Snowflake]], MISSING),
            ("public_updates_channel_id", MissingOr[Optional[Snowflake]], MISSING),
            ("preferred_locale", MissingOr[Optional[str]], MISSING),
            ("features", MissingOr[List[str]], MISSING),
            ("description", MissingOr[Optional[str]], MISSING),
            ("premium_progress_bar_enabled", MissingOr[bool], MISSING),
        ],
    )
    modify_guild_mfa_level = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/mfa",
        format_args={"guild_id": Snowflake},
        param_args=[("level", int)],
    )
    modify_guild_widget = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/widget",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("enabled", bool),
            ("channel_id", Optional[Snowflake]),
        ],
    )
    modify_guild_welcome_screen = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/welcome-screen",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("enabled", MissingOr[Optional[bool]], MISSING),
            ("welcome_channels", MissingOr[Optional[List[WelcomeChannelData]]], MISSING),
            ("description", MissingOr[Optional[str]], MISSING),
        ],
    )
    # TODO: modify user voice state/modify current user voice state
    delete_guild = APIEndpointData(
        "DELETE", "/guilds/{guild_id}", format_args={"guild_id": Snowflake}
    )
    delete_guild_integrations = APIEndpointData(
        "DELETE", "/guilds/{guild_id}/integrations", format_args={"guild_id": Snowflake}
    )
    begin_guild_prune = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/prune",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("days", int, 7),
            ("compute_prune_count", bool, True),
            ("include_roles", Optional[List[Snowflake]], None),
        ],
    )


class GuildMemberEndpointMixin(CoreMixin):
    get_guild_member = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/members/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
    )
    list_guild_members = APIEndpointData(
        "GET",
        "/guild/{guild_id}/members",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("limit", int, 1),
            ("after", MissingOr[Snowflake], MISSING),
        ],
    )
    search_guild_members = APIEndpointData(
        "GET",
        "/guild/{guild_id}/members/search",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("query", str),
            ("limit", int, 1),
        ],
    )
    modify_guild_member = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/members/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("nick", MissingOr[Optional[str]], MISSING),
            ("roles", MissingOr[Optional[List[Snowflake]]], MISSING),
            ("mute", MissingOr[Optional[bool]], MISSING),
            ("deaf", MissingOr[Optional[bool]], MISSING),
            ("channel_id", MissingOr[Optional[Snowflake]], MISSING),
            ("communication_disabled_until", MissingOr[Optional[datetime]], MISSING),
        ],
    )
    modify_current_member = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/members/@me",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[("nick", MissingOr[Optional[str]], MISSING)],
    )
    remove_guild_member = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/members/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
        supports_reason=True,
    )
    add_guild_member_role = APIEndpointData(
        "PUT",
        "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake, "role_id": Snowflake},
        supports_reason=True,
    )
    remove_guild_member_role = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake, "role_id": Snowflake},
        supports_reason=True,
    )
    get_guild_ban = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/bans/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
    )
    get_guild_bans = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/bans",
        format_args={"guild_id": Snowflake},
        param_args=[
            ("limit", int, 1000),
            ("before", MissingOr[Snowflake], MISSING),
            ("after", MissingOr[Snowflake], MISSING),
        ],
    )
    create_guild_ban = APIEndpointData(
        "PUT",
        "/guilds/{guild_id}/bans/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("delete_message_days", int, 0),
        ],
    )
    remove_guild_ban = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/bans/{user_id}",
        format_args={"guild_id": Snowflake, "user_id": Snowflake},
        supports_reason=True,
    )


class GuildRoleEndpointMixin(CoreMixin):
    get_guild_roles = APIEndpointData(
        "GET", "/guilds/{guild_id}/roles", format_args={"guild_id": Snowflake}
    )
    create_guild_role = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/roles",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str, '"new role"'),
            ("permissions", str, "0"),
            ("color", int, 0),
            ("hoist", bool, False),
            ("icon", Optional[str], None),
            ("unicode_emoji", Optional[str], None),
            ("mentionable", bool, False),
        ],
    )
    modify_guild_role = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/roles/{role_id}",
        format_args={"guild_id": Snowflake, "role_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", MissingOr[Optional[str]], MISSING),
            ("permissions", MissingOr[Optional[str]], MISSING),
            ("color", MissingOr[Optional[int]], MISSING),
            ("hoist", MissingOr[Optional[bool]], MISSING),
            ("icon", MissingOr[Optional[str]], MISSING),
            ("unicode_emoji", MissingOr[Optional[str]], MISSING),
            ("mentionable", MissingOr[Optional[bool]], MISSING),
        ],
    )
    modify_guild_role_positions = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/roles",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("id", Snowflake),
            ("position", MissingOr[Optional[int]], MISSING),
        ],
    )
    delete_guild_role = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/roles/{role_id}",
        format_args={"guild_id": Snowflake, "role_id": Snowflake},
    )
