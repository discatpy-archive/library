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

from ...types import List, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = ("EmojiEndpointMixin",)


class EmojiEndpointMixin(CoreMixin):
    list_guild_emojis = APIEndpointData(
        "GET", "/guilds/{guild_id}/emojis", format_args={"guild_id": Snowflake}
    )
    get_guild_emoji = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/emojis/{emoji_id}",
        format_args={"guild_id": Snowflake, "emoji_id": Snowflake},
    )
    create_guild_emoji = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/emojis",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("image", str),
            ("roles", List[Snowflake]),
        ],
    )
    modify_guild_emoji = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/emojis/{emoji_id}",
        format_args={"guild_id": Snowflake, "emoji_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", str),
            ("roles", List[Snowflake]),
        ],
    )
    delete_guild_emoji = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/emojis/{emoji_id}",
        format_args={"guild_id": Snowflake, "emoji_id": Snowflake},
        supports_reason=True,
    )
