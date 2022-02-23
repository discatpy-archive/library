"""
The MIT License (MIT)

Copyright (c) 2015-2021 Rapptz
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
import asyncio
import weakref
import aiohttp
import json
import datetime

from . import __version__
from .errors import DisBotPyException, HTTPException

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

    @property
    def bucket(self) -> str:
        return f"{self.channel_id}:{self.guild_id}:{self.path}"

def _get_user_agent():
    user_agent = "DiscordBot (https://github.com/EmreTech/DisBotPy.git, {0}) Python/{1.major}.{1.minor}.{1.micro}"
    return user_agent.format(__version__, sys.version_info)

class MaybeUnlock:
    def __init__(self, lock: asyncio.Lock):
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self):
        return self

    def defer(self):
        self._unlock = False

    def __exit__(self, exc_type, exc, traceback):
        if self._unlock:
            self.lock.release()

def _parse_ratelimit_header(headers: Dict[str, Any]):
    reset_after: Optional[str] = headers.get("X-RateLimit-Reset-After")
    if not reset_after:
        utc = datetime.timezone.utc
        now = datetime.datetime.now(utc)
        reset = datetime.datetime.fromtimestamp(headers.get("X-RateLimit-Reset"))
        return (reset - now).total_seconds()
    else:
        return float(reset_after)

class HTTPClient:
    def __init__(self, connector: Optional[aiohttp.BaseConnector] = None, token: Optional[str] = None):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self.connector = connector
        self._session: Optional[aiohttp.ClientSession] = None # initalized later by static_login
        self._global_ratelimit_over: asyncio.Event = asyncio.Event()
        self._global_ratelimit_over.set()
        self._bucket_locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.token: Optional[str] = token

        self.user_agent = _get_user_agent()

    def recreate_session(self):
        if self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=self.connector
            )

    async def ws_connect(self, url: str):
        kwargs = {
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.user_agent
            },
            "compress": 0,
        }

        return await self._session.ws_connect(url, **kwargs)

    async def request(self, route: Route, **kwargs):
        bucket = route.bucket
        url = route.url
        method = route.method

        lock = self._bucket_locks.get(bucket)
        if lock is None:
            # lock for this bucket has not been initalized
            lock = asyncio.Lock()
            if bucket is not None:
                self._bucket_locks[bucket] = lock

        headers: Dict[str, Any] = {
            "User-Agent": self.user_agent
        }

        if self.token is not None:
            headers["Authorization"] = f"Bot {self.token}"

        data = kwargs.get("json")
        if data is not None:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(data, separators=(",", ":"), ensure_ascii=True)

        # TODO: Manage Audit log reason

        kwargs["headers"] = headers

        if not self._global_ratelimit_over.is_set():
            # global ratelimit is not over, wait
            await self._global_ratelimit_over.wait()

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        # wait for the bucket lock to be unlocked, then lock it again
        await lock.acquire()
        with MaybeUnlock(lock) as m_lock:
            # try to connect 5 times before giving up
            for tries in range(5):
                async with self._session.request(method, url, **kwargs) as response:
                    data = await response.json(encoding="utf-8")
                    resp_code = response.status

                    remaining_req = response.headers.get("X-RateLimit-Remaining")
                    if remaining_req == "0" and resp_code != 429:
                        # this means that the current ratelimit bucket has been exhausted
                        delta = _parse_ratelimit_header(response.headers)
                        m_lock.defer()
                        self.loop.call_later(delta, lock.release)

                    if resp_code >= 200 and resp_code < 300:
                        print("Connection to \"{0}\" succeeded!".format(route.url))
                        return data

                    # we are being ratelimited
                    if resp_code == 429:
                        if response.headers.get("Via") or isinstance(data, str):
                            # probably banned by CloudFlare
                            raise HTTPException(response, data)

                        retry_after = data["retry_after"]
                        is_global = data.get("global", False)
                        if is_global:
                            # unset global ratelimit over event
                            self._global_ratelimit_over.clear()

                        # wait then try again
                        await asyncio.sleep(retry_after)

                        if is_global:
                            self._global_ratelimit_over.set()

                        continue
                    
                    # server error, retry after waiting
                    if resp_code in {500, 502, 504}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    # other error cases
                    if resp_code == 403:
                        raise HTTPException(response, data)
                    elif resp_code == 404:
                        raise HTTPException(response, data)
                    elif resp_code >= 500:
                        raise HTTPException(response, data)
                    else:
                        raise HTTPException(response, data)

            # exhausted retries
            if response is not None:
                if resp_code >= 500:
                    raise HTTPException(response, data)

                raise HTTPException(response, data)

        raise RuntimeError("Got to unreachable section of HTTPClient.request")

    async def close(self):
        return await self._session.close()

    async def login(self, token: str):
        self._session = aiohttp.ClientSession(
            connector=self.connector
        )
        old_token = self.token
        self.token = token

        try:
            # get info about ourselves
            data = await self.request(Route("GET", "/users/@me"))
        except HTTPException as e:
            self.token = old_token
            if e.status == 401:
                raise DisBotPyException("LoginFailure: Improper token has been passed.") from e
            raise

        return data

    async def get_gateway_bot(self, *, encoding: str = "json", zlib: bool = True):
        try:
            data = await self.request(Route("GET", "/gateway/bot"))
        except HTTPException as e:
            raise DisBotPyException("Gateway not found") from e

        if zlib:
            fmt = "{0}?v={1}&encoding={2}&compress=zlib-stream"
        else:
            fmt = "{0}?v={1}&encoding={2}"

        return data["shards"], fmt.format(data["url"], API_VERSION, encoding)

    async def get_user(self, user_id: str):
        return await self.request(Route("GET", "/users/{user_id}", user_id=user_id))

    async def get_message(self, channel_id: str, message_id: str):
        return await self.request(Route("GET", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=message_id))