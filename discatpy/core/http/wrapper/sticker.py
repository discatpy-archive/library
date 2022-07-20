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

from typing import Optional

from ...types import EllipsisOr, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = ("StickerEndpointMixin",)


class StickerEndpointMixin(CoreMixin):
    get_sticker = APIEndpointData(
        "GET", "/stickers/{sticker_id}", format_args={"sticker_id": Snowflake}
    )
    get_guild_sticker = APIEndpointData(
        "GET",
        "/guilds/{guild_id}/stickers/{sticker_id}",
        format_args={"guild_id": Snowflake, "sticker_id": Snowflake},
    )
    list_nitro_sticker_packs = APIEndpointData("GET", "/sticker-packs")
    list_guild_stickers = APIEndpointData(
        "GET", "/guilds/{guild_id}/stickers", format_args={"guild_id": Snowflake}
    )
    create_guild_sticker = APIEndpointData(
        "POST",
        "/guilds/{guild_id}/stickers",
        format_args={"guild_id": Snowflake},
        supports_reason=True,
        supports_files=True,
        param_args=[
            ("name", str),
            ("description", str),
            ("tags", str),
        ],
    )
    modify_guild_sticker = APIEndpointData(
        "PATCH",
        "/guilds/{guild_id}/stickers/{sticker_id}",
        format_args={"guild_id": Snowflake, "sticker_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("name", EllipsisOr[str], ...),
            ("description", EllipsisOr[Optional[str]], ...),
            ("tags", EllipsisOr[str], ...),
        ],
    )
    delete_guild_sticker = APIEndpointData(
        "DELETE",
        "/guilds/{guild_id}/stickers/{sticker_id}",
        format_args={"guild_id": Snowflake, "sticker_id": Snowflake},
        supports_reason=True,
    )
