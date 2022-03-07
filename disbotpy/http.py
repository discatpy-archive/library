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
from .types.snowflake import *
from .errors import DisBotPyException, HTTPException

__all__ = (
    "Route",
    "HTTPClient"
)

API_VERSION = 9

class Route:
    """
    The route for a request

    This tells the HTTPClient where you want to go and what
    method you want to connect with.

    Parameters
    ----------
    method: :type:`str`
        The method to use when connecting
    path: :type:`str`
        The path to connect to
    parameters :type:`Dict[str, Any]`
        Additional parameters to the path. Automatically formatted

    Attributes
    ----------
    url: :type:`str`
        Fully formatted url to connect to
    channel_id: :type:`Optional[Snowflake]`
        The channel id if it's specified in parameters
    guild_id: :type:`Optional[Snowflake]`
        The guild id if it's specified in parameters
    webhook_id: :type:`Optional[Snowflake]`
        The webhook id if it's specified in parameters
    webhook_token: :type:`Optional[str]`
        The webhook token if it's specified in parameters
    """

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        url: str = self.base + self.path
        if parameters:
            url = url.format_map({k: urlquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

        # some major parameters
        self.channel_id: Optional[Snowflake] = parameters.get("channel_id")
        self.guild_id: Optional[Snowflake] = parameters.get("guild_id")
        self.webhook_id: Optional[Snowflake] = parameters.get("webhook_id")
        self.webhook_token: Optional[str] = parameters.get("webhook_token")

    @property
    def base(self) -> str:
        return "https://discord.com/api/v{0}".format(API_VERSION)

    @property
    def bucket(self) -> str:
        """
        Returns the current ratelimit bucket for this Route.
        """
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
    """
    The HTTP client between your bot and Discord.

    This manages connections to the Discord API and allows you
    to make your own requests.

    Parameters
    ----------
    connector: :type:`Optional[aiohttp.BaseConnector]`
        The connector to use with the internal aiohttp session

    Attributes
    ----------
    loop: :type:`asyncio.AbstractEventLoop`
        The main event loop. Used for ratelimiting in request
    _session: :type:`Optional[aiohttp.ClientSession]`
        The internal aiohttp session. Initalized later by login
    token: :type:`Optional[str]`
        The bot's token. Initalized later by login
    user_agent: :type:`str`
        The user agent sent with all requests and the Gateway.
        Do not modify this
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, connector: Optional[aiohttp.BaseConnector] = None):
        self.loop: asyncio.AbstractEventLoop = loop
        self.connector = connector
        self._session: Optional[aiohttp.ClientSession] = None # initalized later by login
        self._global_ratelimit_over: asyncio.Event = asyncio.Event()
        self._global_ratelimit_over.set()
        self._bucket_locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.token: Optional[str] = None

        self.user_agent: str = _get_user_agent()

    def recreate_session(self):
        """
        Recreates the session if it's closed.
        """
        if self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=self.connector
            )

    async def ws_connect(self, url: str):
        """
        Starts a websocket connection. 
        
        This is only used for the Gateway.
        """
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
        """
        Sends a request to the Discord API.

        This function automatically handles ratelimiting.

        Parameters
        ----------
        route: :type:`Route`
            Where we should send a request to and the method to use
        json: :type:`Dict[str, Any]`
            Any content we should send along with the request
        """
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
                    if resp_code >= 400:
                        raise HTTPException(response, data)

            # exhausted retries
            if response is not None:
                raise HTTPException(response, data)

        raise RuntimeError("Got to unreachable section of HTTPClient.request")

    async def close(self):
        """
        Closes the internal session. 
        
        Required when the client is done in order to stop 
        aiohttp from complaining.
        """
        return await self._session.close()

    async def login(self, token: str):
        """
        Logs into the bot account by initalizing the aiohttp.ClientSession then
        grabbing info on the bot account.

        Parameters
        ----------
        token: :type:`str`
            The token to login with
        """
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

    async def leave_guild(self, guild_id: Snowflake):
        """
        Makes the bot leave a guild with the provided guild id.

        Parameters
        ----------
        guild_id: :type:`Snowflake`
            The id of the guild to leave
        """
        return await self.request(Route("DELETE", "/users/@me/guilds/{guild_id}", guild_id=guild_id))

    async def get_gateway_bot(self, *, encoding: str = "json", zlib: bool = True):
        """
        Grabs the Gateway URL along with the number of shards.

        Parameters
        ----------
        encoding: :type:`str`
            The encoding the Gateway should use. Set to "json" by default
        zlib: :type:`bool`
            If the Gateway should send compressed payloads or not. Set to True by default
        """
        try:
            data = await self.request(Route("GET", "/gateway/bot"))
        except HTTPException as e:
            raise DisBotPyException("Gateway not found") from e

        if zlib:
            fmt = "{0}?v={1}&encoding={2}&compress=zlib-stream"
        else:
            fmt = "{0}?v={1}&encoding={2}"

        return data["shards"], fmt.format(data["url"], API_VERSION, encoding)

    async def modify_current_user(self, username: str):
        # TODO: add the ability to modify the avatar
        json_req: Dict[str, Any] = {"username": username}
        return await self.request(Route("PATCH", "/users/@me"), json=json_req)

    async def get_user(self, user_id: Snowflake):
        """
        Grabs a user object from its id.

        Parameters
        ----------
        user_id: :type:`Snowflake`
            The id of the user to grab
        """
        return await self.request(Route("GET", "/users/{user_id}", user_id=user_id))

    async def modify_dm_channel(self, channel_id: Snowflake, new_channel: Dict[str, Any]):
        """
        Modifies a Group DM channel with the given channel (in Dict form).

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to modify
        new_channel: :type:`Dict[str, Any]`
            The updated channel. Outputted from `DMChannel.to_dict()`
        """
        name = new_channel.get("name")
        icon = new_channel.get("icon")
        return await self.request(
            Route("PATCH", "/channels/{channel_id}", channel_id=channel_id),
            json={
                "name": name,
                "icon": icon
            }
        )

    async def modify_guild_channel(self, channel_id: Snowflake, new_channel: Dict[str, Any]):
        """
        Modifies a guild channel with the given channel (in Dict form).

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to modify
        new_channel: :type:`Dict[str, Any]`
            The updated channel. Outputted from `GuildChannel.to_dict()`
        """
        return await self.request(Route("PATCH", "/channels/{channel_id}", channel_id=channel_id), json=new_channel)

    async def get_channel(self, channel_id: Snowflake):
        """
        Grabs a channel from its id.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to grab
        """
        return await self.request(Route("GET", "/channels/{channel_id}", channel_id=channel_id))

    async def delete_channel(self, channel_id: Snowflake):
        """
        Deletes/closes a channel.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to delete/close
        """
        return await self.request(Route("DELETE", "/channels/{channel_id}", channel_id=channel_id))

    async def get_messages(self, channel_id: Snowflake, around: Optional[Snowflake] = None, before: Optional[Snowflake] = None, after: Optional[Snowflake] = None, limit: int = 50):
        """
        Grabs all messages from a channel.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to grab the messages from
        around: :type:`Optional[Snowflake]`
            The id of the message to grab the messages around. Set to None by default
        before: :type:`Optional[Snowflake]`
            The id of the message to grab the messages before. Set to None by default
        after: :type:`Optional[Snowflake]`
            The id of the message to grab the messages after. Set to None by default
        limit: :type:`int`
            The amount of messages to grab. Set to 50 by default
        """
        if limit < 1:
            raise ValueError("Got a limit that's smaller than 1")
        elif limit > 100:
            raise ValueError("Got a limit that's larger than 100")

        json_req: Dict[str, Any] = {"limit": limit}
        if around:
            json_req["around"] = around
        if before:
            json_req["before"] = before
        if after:
            json_req["after"] = after

        return await self.request(Route("GET", "/channels/{channel_id}/messages", channel_id=channel_id), json=json_req)

    async def get_message(self, channel_id: Snowflake, message_id: Snowflake):
        """
        Grabs a message from its id.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel where the message is from
        message_id: :type:`Snowflake`
            The id of the message to grab
        """
        return await self.request(Route("GET", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=message_id))  
