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

from ...types import MISSING, MissingOr, Snowflake

class GuildTemplateEndpointMixin:
    async def get_guild_template(self, template_code: str): ...
    async def get_guild_templates(self, guild_id: Snowflake): ...
    async def create_guild_template(
        self, guild_id: Snowflake, *, name: str, description: MissingOr[Optional[str]] = MISSING
    ): ...
    async def create_guild_from_guild_template(
        self, template_code: str, *, name: str, icon: MissingOr[str] = MISSING
    ): ...
    async def modify_guild_template(
        self,
        guild_id: Snowflake,
        *,
        name: MissingOr[str] = MISSING,
        description: MissingOr[Optional[str]] = MISSING,
    ): ...
    async def delete_guild_template(self, guild_id: Snowflake, template_code: str): ...
    async def sync_guild_template(self, guild_id: Snowflake, template_code: str): ...