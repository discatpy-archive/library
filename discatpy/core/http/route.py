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

from dataclasses import dataclass, KW_ONLY
from urllib.parse import quote as _urlquote
from typing import Optional

from ..types import Snowflake

__all__ = ("BucketParams", "Route",)


@dataclass
class BucketParams:
    _: KW_ONLY
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    webhook_id: Optional[Snowflake]
    webhook_token: Optional[str]


class Route:
    def __init__(self, url: str, **params):
        self.params = params
        self.url = url

        # top-level resource parameters
        self.guild_id: Optional[Snowflake] = params.get("guild_id")
        self.channel_id: Optional[Snowflake] = params.get("channel_id")
        self.webhook_id: Optional[Snowflake] = params.get("webhook_id")
        self.webhook_token: Optional[str] = params.get("webhook_token")

    @property
    def endpoint(self):
        return self.url.format_map({k: _urlquote(str(v)) for k, v in self.params.items()})

    @property
    def bucket(self):
        return BucketParams(
            guild_id=self.guild_id, 
            channel_id=self.channel_id, 
            webhook_id=self.webhook_id, 
            webhook_token=self.webhook_token
        )
