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

import json
import aiohttp
import asyncio
import sys
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import quote as _urlquote

from ... import __version__
from ..errors import DisCatPyException, HTTPException
from ..types import MISSING, MissingOr, MissingType
from .ratelimiter import Ratelimiter, BucketResolutor

BASE_API_URL = "https://discord.com/api/v{0}"
VALID_API_VERSIONS = [9, 10]
DEFAULT_API_VERSION = 9

__all__ = ("_HTTPClient",)

@dataclass
class _PreparedData:
    json: MissingOr[Any]
    files: MissingType # TODO: Switch this to MissingOr[Files] once files are added

class _HTTPClient:
    __slots__ = (
        "token",
        "_resolutor",
        "_ratelimiter",
        "_api_version",
        "_api_url",
        "_session",
        "user_agent",
    )

    def __init__(self, token: str, *, api_version: Optional[int] = None):
        self.token = token
        self._resolutor = BucketResolutor()
        self._ratelimiter = Ratelimiter(self._resolutor)
        self._api_version = api_version if api_version is not None and api_version in VALID_API_VERSIONS else DEFAULT_API_VERSION
        self._api_url = BASE_API_URL.format(self._api_version)

        self.__session: Optional[aiohttp.ClientSession] = None
        self.user_agent = "DiscordBot (https://github.com/EmreTech/DisCatPy/tree/api-refactor, {0}) Python/{1.major}.{1.minor}.{1.micro}".format(__version__, sys.version_info)

    @property
    def _session(self):
        if self.__session.closed or self.__session is None:
            self.__session = aiohttp.ClientSession(headers={"User-Agent": self.user_agent})

        return self.__session

    async def ws_connect(self, url: str):
        """Starts a websocket connection.
        
        Parameters
        ----------
        url: :class:`str`
            The url of the websocket to connect to.
        """
        kwargs = {
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {"User-Agent": self.user_agent},
            "compress": 0,
        }

        return await self._session.ws_connect(url, **kwargs)

    async def close(self):
        """Closes the connection."""
        if self.__session and not self.__session.closed:
            await self._session.close()

    @staticmethod
    def _prepare_data(json: MissingOr[dict[str, Any]]):
        # TODO: Use aiohttp.FormData when files are included

        if json is not MISSING:
            return _PreparedData(json, MISSING)

        return _PreparedData(MISSING, MISSING)

    @staticmethod
    async def _text_or_json(resp: aiohttp.ClientResponse):
        text = await resp.text()

        if resp.content_type == "application/json":
            return json.loads(text)

        return text

    async def request(
        self, 
        method: str, 
        url: str, 
        url_format_params: Optional[dict[str, Any]] = None,
        *, 
        query_params: Optional[dict[str, Any]] = None,
        json_params: MissingOr[dict[str, Any]] = MISSING,
        reason: Optional[str] = None,
    ):
        url_format_params = url_format_params or {}
        url = url.format_map({k: _urlquote(v) for k, v in url_format_params.items()})

        query_params = query_params or {}
        max_tries = 5
        headers: dict[str, str] = {"Authorization": f"Bot {self.token}"}

        if reason:
            headers["X-Audit-Log-Reason"] = _urlquote(reason, safe="/ ")


        for tries in range(max_tries):
            data = self._prepare_data(json_params)
            kwargs: dict[str, Any] = {}

            if data.json is not MISSING:
                kwargs["json"] = data.json

            client_bucket = f"{method}:{url}"
            bucket = await self._ratelimiter.acquire_bucket(client_bucket)

            if self._ratelimiter._global_lock.is_set():
                await self._ratelimiter._global_lock.wait()

            async with bucket:
                response = await self._session.request(
                    method,
                    url,
                    params=query_params,
                    headers=headers,
                    **kwargs
                )

                reset_after = float(response.headers.get("X-RateLimit-Reset-After", 0))
                remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
                discord_bucket = str(response.headers.get("X-RateLimit-Bucket", client_bucket))

                if self._resolutor._bucket_strs.get(client_bucket) != discord_bucket:
                    self._resolutor.add_bucket_mapping(client_bucket, discord_bucket)

                # Everything is ok
                if 200 <= response.status < 300:
                    if remaining == 0:
                        await bucket.delay_unlock(reset_after)
                    return await self._text_or_json(response)

                # Ratelimited
                if response.status == 429:
                    if "Via" not in response.headers:
                        # something about Cloudflare and Google responding and adding something to the headers
                        # it means we're Cloudflare banned
                        raise HTTPException(response, await self._text_or_json(response))

                    response_json: dict[str, Any] = await response.json()
                    is_global = response_json.get("global", False)

                    if is_global:
                        await self._ratelimiter.set_global_lock(reset_after)
                    else:
                        await bucket.delay_unlock(reset_after)

                # Specific Server Errors, retry after some time
                if response.status in {500, 502, 504}:
                    await asyncio.sleep(1 + tries * 2)
                    continue

                # Client/Server errors
                if response.status >= 400:
                    raise HTTPException(response, await self._text_or_json(response))

        raise DisCatPyException(f"Tried sending request to \"{url}\" with method {method} {max_tries} times.")