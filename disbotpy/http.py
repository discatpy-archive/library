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

from typing import Any, Dict, Optional, Union
from urllib.parse import quote as urlquote
import sys
#import asyncio
import aiohttp

from . import __version__
from .errors import HTTPException

__all__ = (
    "Route",
    "HTTPClient"
)

API_VERSION = 9

class Route:
    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        url: str = self.base + self.path
        if parameters:
            url = url.format_map({k: urlquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

        # some major parameters
        # TODO: Switch str type to Snowflake type except for webhook token
        self.channel_id: Optional[str] = parameters.get("channel_id")
        self.guild_id: Optional[str] = parameters.get("guild_id")
        self.webhook_id: Optional[str] = parameters.get("webhook_id")
        self.webhook_token: Optional[str] = parameters.get("webhook_token")

    @property
    def base(self) -> str:
        return "https://discord.com/api/v{0}".format(API_VERSION)

    #@property
    #def bucket(self) -> str:
    #    return f"{self.channel_id}:{self.guild_id}:{self.path}"

# TODO: Move to a more relevant place like disbotpy.utils
def _get_user_agent():
    user_agent = "DiscordBot (https://github.com/EmreTech/DisBotPy.git, {0}) Python/{1.major}.{1.minor}.{1.micro} aiohttp/{2}"
    return user_agent.format(__version__, sys.version_info, aiohttp.__version__)

class HTTPClient:
    def __init__(self, connector: Optional[aiohttp.BaseConnector] = None, token: Optional[str] = None):
        self.connector = connector
        self._session: Optional[aiohttp.ClientSession] = None # initalized by client
        self.token: Optional[str] = token

        self.user_agent = _get_user_agent()

    def recreate_session(self):
        if self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=self.connector
            )

    async def request(self, route: Route, **kwargs):
        headers = {
            "User-Agent": self.user_agent
        }

        if self.token is not None:
            headers["Authorization"] = f"Bot {self.token}"

        json = kwargs.get("json")
        if json is not None:
            headers["Content-Type"] = "application/json"
            # TODO: Convert dict to str
            kwargs["data"] = kwargs.pop("json")

        kwargs["headers"] = headers

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None
        async with self._session.request(route.method, route.url, **kwargs) as response:
            data = await response.json(encoding="utf-8")
            resp_code = response.status

            if resp_code >= 200 and resp_code < 300:
                print("Connection to \"{0}\" succeeded!".format(route.url))
                return data
            elif resp_code >= 400 and resp_code < 500:
                raise HTTPException("Got {0} client error code when attempting to connect to {1}".format(resp_code, route.path))
            elif resp_code >= 500:
                raise HTTPException("Got {0} server error code when attempting to connect to {1}".format(resp_code, route.path))

        raise RuntimeError("Got to unreachable section of HTTPClient.request")

    async def get_gateway_bot(self):
        return await self.request(Route("GET", "/gateway/bot"))

    async def get_user(self, user_id: str):
        return await self.request(Route("GET", "/users/{user_id}", user_id=user_id))

    async def get_message(self, channel_id: str, message_id: str):
        return await self.request(Route("GET", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=message_id))