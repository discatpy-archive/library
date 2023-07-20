# SPDX-License-Identifier: MIT

import typing as t
from urllib.parse import quote as _urlquote

import discord_typings as dt

__all__ = ("Route",)


class Route:
    """Represents a Discord API route. This implements helpful methods that the internals use.

    Args:
        method (str): The method of this REST API route.
        url (str): The raw, unformatted url of this REST API route.
        **params (t.Any): The parameters for the raw, unformatted url.

    Attributes:
        params (dict[str, t.Any]): The parameters for the raw, unformatted url.
        method (str): The method of this REST API route.
        url (str): The raw, unformatted url of this REST API route.
        guild_id (t.Optional[dt.Snowflake]): If included, the guild id parameter.
            This is a top-level parameter, which influences the pseudo-bucket generated.
        channel_id (t.Optional[dt.Snowflake]): If included, the channel id parameter.
            This is a top-level parameter, which influences the pseudo-bucket generated.
        webhook_id (t.Optional[dt.Snowflake]): If included, the webhook id parameter.
            This is a top-level parameter, which influences the pseudo-bucket generated.
        webhook_token (t.Optional[str]): If included, the webhook token parameter.
            This is a top-level parameter, which influences the pseudo-bucket generated.
    """

    def __init__(self, method: str, url: str, **params: t.Any) -> None:
        self.params: dict[str, t.Any] = params
        self.method: str = method
        self.url: str = url

        # top-level resource parameters
        self.guild_id: t.Optional[dt.Snowflake] = params.pop("guild_id", None)
        self.channel_id: t.Optional[dt.Snowflake] = params.pop("channel_id", None)
        self.webhook_id: t.Optional[dt.Snowflake] = params.pop("webhook_id", None)
        self.webhook_token: t.Optional[str] = params.pop("webhook_token", None)

    @property
    def endpoint(self) -> str:
        """The formatted url for this route."""
        top_level_params = {
            k: getattr(self, k)
            for k in ("guild_id", "channel_id", "webhook_id", "webhook_token")
            if getattr(self, k) is not None
        }
        other_params = {k: _urlquote(str(v)) for k, v in self.params.items()}

        return self.url.format_map({**top_level_params, **other_params})

    @property
    def bucket(self) -> str:
        """The pseudo-bucket that represents this route. This is generated with the method and top level parameters filled into the raw url."""
        top_level_params = {
            k: getattr(self, k)
            for k in ("guild_id", "channel_id", "webhook_id", "webhook_token")
            if getattr(self, k) is not None
        }
        other_params = {k: None for k in self.params.keys()}

        return (
            f"{self.method}:{self.url.format_map({**top_level_params, **other_params})}"
        )
