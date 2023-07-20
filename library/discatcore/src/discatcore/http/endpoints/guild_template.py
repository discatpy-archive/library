# SPDX-License-Identifier: MIT

# this file was auto-generated by scripts/generate_endpoints.py

import typing as t

import discord_typings as dt

from ...types import Unset, UnsetOr
from ..route import Route
from .core import EndpointMixin

__all__ = ("GuildTemplateEndpoints",)


class GuildTemplateEndpoints(EndpointMixin):
    def get_guild_template(self, template_code: dt.Snowflake):
        return self.request(
            Route("GET", "/guilds/templates/{template_code}", template_code=template_code)
        )

    def create_guild_from_guild_template(
        self, template_code: dt.Snowflake, *, name: str, icon: UnsetOr[str] = Unset
    ):
        return self.request(
            Route("POST", "/guilds/templates/{template_code}", template_code=template_code),
            json_params={"name": name, "icon": icon},
        )

    def get_guild_templates(self, guild_id: dt.Snowflake):
        return self.request(Route("GET", "/guilds/{guild_id}/templates", guild_id=guild_id))

    def create_guild_template(
        self, guild_id: dt.Snowflake, *, name: str, description: UnsetOr[t.Optional[str]] = Unset
    ):
        return self.request(
            Route("POST", "/guilds/{guild_id}/templates", guild_id=guild_id),
            json_params={"name": name, "description": description},
        )

    def sync_guild_template(self, guild_id: dt.Snowflake, template_code: dt.Snowflake):
        return self.request(
            Route(
                "PUT",
                "/guilds/{guild_id}/templates/{template_code}",
                guild_id=guild_id,
                template_code=template_code,
            )
        )

    def modify_guild_template(
        self,
        guild_id: dt.Snowflake,
        template_code: dt.Snowflake,
        *,
        name: UnsetOr[str] = Unset,
        description: UnsetOr[t.Optional[str]] = Unset,
    ):
        return self.request(
            Route(
                "PATCH",
                "/guilds/{guild_id}/templates/{template_code}",
                guild_id=guild_id,
                template_code=template_code,
            ),
            json_params={"name": name, "description": description},
        )

    def delete_guild_template(self, guild_id: dt.Snowflake, template_code: dt.Snowflake):
        return self.request(
            Route(
                "DELETE",
                "/guilds/{guild_id}/templates/{template_code}",
                guild_id=guild_id,
                template_code=template_code,
            )
        )
