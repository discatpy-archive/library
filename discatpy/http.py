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

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote as urlquote
import sys
import asyncio
import aiohttp
import json
import datetime
import logging

from . import __version__
from .types.channel import ChannelType
from .types.snowflake import *
from .types.message import MessageReference
from .embed import Embed
from .errors import DisCatPyException, HTTPException
from .utils import DataEvent

__all__ = (
    "Route",
    "HTTPClient"
)

_log = logging.getLogger(__name__)

VALID_API_VERSIONS: List[int] = [9, 10]

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
    """

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self._parameters = parameters

        # some major parameters
        self.channel_id: Optional[Snowflake] = parameters.get("channel_id")
        self.guild_id: Optional[Snowflake] = parameters.get("guild_id")

    @property
    def base(self) -> str:
        return "https://discord.com/api/v{0}"

    @property
    def endpoint(self) -> str:
        return "{0}:{1}".format(self.method, self.path)

    def get_bucket(self, shared_bucket_hash: str) -> str:
        return f"{self.guild_id}:{self.channel_id}:{self.path}" if shared_bucket_hash is None else f"{self.guild_id}:{self.channel_id}:{shared_bucket_hash}"

    def grab_url(self, api_version: str) -> str:
        url = self.base.format(api_version) + self.path
        if self._parameters:
            url = url.format_map({k: urlquote(v) if isinstance(v, str) else v for k, v in self._parameters.items()})

        return url

def _get_user_agent():
    user_agent = "DiscordBot (https://github.com/EmreTech/DisCatPy.git, {0}) Python/{1.major}.{1.minor}.{1.micro}"
    return user_agent.format(__version__, sys.version_info)

def _calculate_ratelimit_delta(reset_timestamp: float) -> float:
    now = datetime.datetime.now()
    reset = datetime.datetime.fromtimestamp(float(reset_timestamp))
    return (reset - now).total_seconds()

def _message_reference_to_dict(mr: MessageReference) -> Dict[str, Any]:
    ret_dict: Dict[str, Any] = {
        "message_id": mr.message_id,
        "fail_if_not_exists": mr.fail_if_not_exists,
    }

    if mr.channel_id:
        ret_dict["channel_id"] = mr.channel_id

    if mr.guild_id:
        ret_dict["guild_id"] = mr.guild_id

    return ret_dict

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
    _session: :type:`Optional[aiohttp.ClientSession]`
        The internal aiohttp session. Initalized later by login
    token: :type:`Optional[str]`
        The bot's token. Initalized later by login
    user_agent: :type:`str`
        The user agent sent with all requests and the Gateway.
        Do not modify this
    """

    def __init__(self, api_version: Optional[int] = None, connector: Optional[aiohttp.BaseConnector] = None):
        self.connector = connector
        self._session: Optional[aiohttp.ClientSession] = None # initalized later by login
        self._global_ratelimit: DataEvent = DataEvent()
        self._bucket_ratelimits: Dict[str, DataEvent] = {}
        self._buckets: Dict[str, str] = {}
        self.token: Optional[str] = None
        self.api_version: int = api_version if api_version is not None else 9
        if self.api_version not in VALID_API_VERSIONS:
            raise ValueError(f"API Version {self.api_version} is invalid!")

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
        headers: Dict[str, Any] = {
            "User-Agent": self.user_agent
        }

        if self.token is not None:
            headers["Authorization"] = f"Bot {self.token}"

        data = kwargs.get("json")
        if data is not None:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(data, separators=(",", ":"), ensure_ascii=True)
            kwargs.pop("json")

        # TODO: Manage Audit log reason

        kwargs["headers"] = headers

        method = route.method
        url = route.grab_url(self.api_version)
        bucket = route.get_bucket(self._buckets.get(route.endpoint))

        # first we do a global ratelimit as that affects all requests
        # then we do a bucket ratelimit

        if self._global_ratelimit.is_set():
            delta = _calculate_ratelimit_delta(self._global_ratelimit.data)
            _log.debug("We are being ratelimited globally. Trying again in %s seconds.", delta)

            if delta <= 0:
                _log.debug("Global ratelimit is over now. Skipping over this ratelimit.")
                pass

            await asyncio.sleep(delta)

        ratelimited = self._bucket_ratelimits.get(bucket)
        if ratelimited is None:
            # ratelimit for this bucket has not been initalized
            ratelimited = DataEvent()
            if bucket is not None:
                self._bucket_ratelimits[bucket] = ratelimited
        else:
            if ratelimited.is_set():
                delta = _calculate_ratelimit_delta(ratelimited.data)
                _log.debug("This bucket is being ratelimited. Trying again in %s seconds.", delta)

                if delta <= 0:
                    _log.debug("Bucket ratelimit is over now. Skipping over this ratelimit.")
                    pass

                await asyncio.sleep(delta)

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        for tries in range(5):
            async with self._session.request(method, url, **kwargs) as response:
                resp_code = response.status
                data = None
                
                if not resp_code == 204: # 204 means empty content, aiohttp throws an error when trying to parse empty context as json
                    data = await response.json(encoding="utf-8")

                _bucket = response.headers.get("X-RateLimit-Bucket")
                remaining_req = response.headers.get("X-RateLimit-Remaining")
                reset_timestamp = response.headers.get("X-RateLimit-Reset")

                if _bucket is not None:
                    self._buckets[route.endpoint] = _bucket

                if remaining_req == "0" and resp_code != 429:
                    # this means that the current ratelimit bucket has been exhausted

                    if not ratelimited.is_set():
                        # we are the first request with this bucket to hit a ratelimit
                        delta = _calculate_ratelimit_delta(reset_timestamp)
                        _log.debug("Ratelimit bucket exhausted, trying again in %s seconds.", delta)

                        if delta > 0:
                            ratelimited.set(reset_timestamp)

                            async def unlock():
                                await asyncio.sleep(delta)
                                ratelimited.clear()

                            ratelimit_task = asyncio.create_task(unlock())
                            await ratelimit_task
                        else:
                            _log.debug("Ratelimit bucket is already good to go. Skipping.")
                    else:
                        # we are not the first request with this bucket to hit a ratelimit
                        delta = _calculate_ratelimit_delta(ratelimited.data)
                        _log.debug("Ratelimit bucket exhausted, trying again in %s seconds.", delta)

                        if delta > 0:
                            await asyncio.sleep(_calculate_ratelimit_delta(ratelimited.data))
                        else:
                            _log.debug("Ratelimit bucket is already good to go. Skipping.")

                if resp_code >= 200 and resp_code < 300:
                    _log.debug("Connection to \"%s\" succeeded!", url)
                    return data

                # we are being ratelimited
                if resp_code == 429:
                    _log.debug("We are being ratelimited!")

                    if response.headers.get("Via") or isinstance(data, str):
                        # probably banned by CloudFlare
                        raise HTTPException(response, data)

                    retry_after = data["retry_after"]
                    is_global = data.get("global", False)
                    _log.debug("Global Ratelimit: %s", is_global)

                    if is_global:
                        self._global_ratelimit.set(reset_timestamp)

                    # wait then try again
                    await asyncio.sleep(retry_after)

                    if is_global:
                        self._global_ratelimit.clear()

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

    # Misc HTTP functions

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
            me = await self.get_current_user()
        except HTTPException as e:
            self.token = old_token
            if e.status == 401:
                raise DisCatPyException("LoginFailure: Improper token has been passed.") from e
            raise

        return me

    async def close(self):
        """
        Closes the internal session. 
        
        Required when the client is done in order to stop 
        aiohttp from complaining.
        """
        return await self._session.close()

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
            raise DisCatPyException("Gateway not found") from e

        if zlib:
            fmt = "{0}?v={1}&encoding={2}&compress=zlib-stream"
        else:
            fmt = "{0}?v={1}&encoding={2}"

        return data["shards"], fmt.format(data["url"], self.api_version, encoding)

    async def get_from_cdn(self, url: str) -> bytes:
        async with self._session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            
            raise HTTPException(resp, f"failed to grab Asset with url {url}")

    # User HTTP functions

    async def get_user(self, user_id: Snowflake):
        """
        Grabs a user object from its id.

        Parameters
        ----------
        user_id: :type:`Snowflake`
            The id of the user to grab
        """
        return await self.request(Route("GET", "/users/{user_id}", user_id=user_id))

    async def get_current_user(self):
        """
        Grabs the current user object.
        """
        return await self.request(Route("GET", "/users/@me"))

    async def create_user_dm(self, recipient_id: Snowflake):
        """
        Creates a new DM with another user.

        Parameters
        ----------
        recipient_id: :type:`Snowflake`
            The recipient of this DM.
        """
        return await self.request(Route("POST", "/users/@me/channels"), json={"recipient_id":recipient_id})

    async def modify_current_user(self, username: str):
        """
        Modifies the current bot's user account.

        Parameters
        ----------
        username: :type:`str`
            The new username for the bot.
        """
        # TODO: add the ability to modify the avatar
        return await self.request(Route("PATCH", "/users/@me"), json={"username":username})

    # Guild HTTP functions

    async def get_guild(self, guild_id: Snowflake, with_counts: bool = False):
        return await self.request(Route("GET", "/guilds/{guild_id}", guild_id=guild_id), json={"with_counts":with_counts})

    async def get_guild_preview(self, guild_id: Snowflake):
        return await self.request(Route("GET", "/guilds/{guild_id}/preview", guild_id=guild_id))

    async def create_guild(
        self, 
        name: str,
        icon: Optional[str] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        roles: Optional[List[Dict[str, Any]]] = None,
        channels: Optional[List[Dict[str, Any]]] = None,
        afk_channel_id: Optional[Snowflake] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[Snowflake] = None,
        system_channel_flags: Optional[int] = None
    ):
        json_req: Dict[str, Any] = {"name": name}

        if icon:
            json_req["icon"] = f"data:image/jpeg;base64,{icon}"

        if verification_level:
            json_req["verification_level"] = verification_level

        if default_message_notifications:
            json_req["default_message_notifications"] = default_message_notifications

        if explicit_content_filter:
            json_req["explicit_content_filter"] = explicit_content_filter

        if roles:
            json_req["roles"] = roles

        if channels:
            json_req["channels"] = channels

        if afk_channel_id:
            json_req["afk_channel_id"] = afk_channel_id

        if afk_timeout:
            json_req["afk_timeout"] = afk_timeout

        if system_channel_id:
            json_req["system_channel_id"] = system_channel_id

        if system_channel_flags:
            json_req["system_channel_flags"] = system_channel_flags

        return await self.request(Route("POST", "/guilds"), json=json_req)

    async def modify_guild(self, guild_id: Snowflake, new_guild: Dict[str, Any]):
        return await self.request(Route("PATCH", "/guilds/{guild_id}", guild_id=guild_id), json=new_guild)
    
    async def leave_guild(self, guild_id: Snowflake):
        """
        Makes the bot leave a guild with the provided guild id.

        Parameters
        ----------
        guild_id: :type:`Snowflake`
            The id of the guild to leave
        """
        return await self.request(Route("DELETE", "/users/@me/guilds/{guild_id}", guild_id=guild_id))

    # Channel HTTP functions

    async def get_channel(self, channel_id: Snowflake):
        """
        Grabs a channel from its id.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to grab
        """
        return await self.request(Route("GET", "/channels/{channel_id}", channel_id=channel_id))

    async def get_channels(self, guild_id: Snowflake):
        return await self.request(Route("GET", "/guilds/{guild_id}/channels", guild_id=guild_id))

    async def get_active_threads(self, guild_id: Snowflake):
        return await self.request(Route("GET", "/guilds/{guild_id}/threads/active", guild_id=guild_id))

    async def create_channel(self, guild_id: Snowflake, new_channel: Dict[str, Any]):
        return await self.request(Route("POST", "/guilds/{guild_id}/channels", guild_id=guild_id), json=new_channel)

    async def modify_channel(self, channel_id: Snowflake, new_channel: Dict[str, Any]):
        """
        Modifies a channel with the given channel (in Dict form).

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to modify
        new_channel: :type:`Dict[str, Any]`
            The updated channel. Outputted from `GuildChannel.to_dict()`
        """
        return await self.request(Route("PATCH", "/channels/{channel_id}", channel_id=channel_id), json=new_channel)

    async def modify_channel_positions(self, guild_id: Snowflake, channel_id: Snowflake, /, position: Optional[int] = None, lock_permissions: Optional[bool] = None, parent_id: Optional[Snowflake] = None):
        json_req: Dict[str, Any] = {
            "id": channel_id
        }

        if position is not None:
            json_req["position"] = position

        if lock_permissions is not None:
            json_req["lock_permissions"] = lock_permissions

        if parent_id:
            json_req["parent_id"] = parent_id

        return await self.request(Route("PATCH", "/guilds/{guild_id}/channels", guild_id=guild_id), json=json_req)

    async def delete_channel(self, channel_id: Snowflake):
        """
        Deletes/closes a channel.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to delete/close
        """
        return await self.request(Route("DELETE", "/channels/{channel_id}", channel_id=channel_id))

    async def start_thread_from_message(
        self, 
        channel_id: Snowflake, 
        msg_id: Snowflake, 
        name: str, 
        auto_archive_duration: Optional[int] = None, 
        cooldown: int = 0
    ):
        """
        Starts a thread with a provided message id.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel where the thread should be made
        msg_id: :type:`Snowflake`
            The id of the message to create the thread from
        name: :type:`str`
            The name of this thread
        auto_archive_duration: :type:`Optional[int]`
            The duration until this thread will be auto archived
        cooldown: :type:`int`
            The cooldown (rate limit per user) of this thread
        """
        json_req: Dict[str, Any] = {"name":name}

        if auto_archive_duration:
            json_req["auto_archive_duration"] = auto_archive_duration
        
        if cooldown:
            json_req["rate_limit_per_user"] = cooldown

        return await self.request(
            Route("POST", "/channels/{channel_id}/messages/{message_id}/threads", channel_id=channel_id, message_id=msg_id),
            json=json_req
        )

    async def start_thread_without_message(
        self, 
        channel_id: Snowflake, 
        name: str, 
        auto_archive_duration: Optional[int] = None, 
        type: int = ChannelType.GUILD_PRIVATE_THREAD,
        invitable: bool = True,
        cooldown: int = 0
    ):
        """
        Starts a thread without a provided message id.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel where the thread should be made
        name: :type:`str`
            The name of this thread
        auto_archive_duration: :type:`Optional[int]`
            The duration until this thread will be auto archived
        type: :type:`int`
            The type of this thread. The only valid values is `GUILD_NEWS_THREAD`,
            `GUILD_PUBLIC_THREAD`, and `GUILD_PRIVATE_THREAD`.
        invitable: :type:`bool`
            Whether or not non-moderators can add other non-moderators to a thread
        cooldown: :type:`int`
            The cooldown (rate limit per user) of this thread
        """
        json_req: Dict[str, Any] = {"name":name, "rate_limit_per_user":cooldown, "type":type}

        if type == ChannelType.GUILD_PRIVATE_THREAD:
            json_req["invitable"] = invitable

        if auto_archive_duration:
            json_req["auto_archive_duration"] = auto_archive_duration

        return await self.request(
            Route("POST", "/channels/{channel_id}/threads", channel_id=channel_id),
            json=json_req
        )

    # Guild Member HTTP functions

    async def get_guild_member(self, guild_id: Snowflake, user_id: Snowflake):
        return await self.request(Route("GET", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id))

    async def get_guild_members(self, guild_id: Snowflake, limit: int = 1, after: Snowflake = 0):
        json_req: Dict[str, Any] = {"limit":limit, "after":after}
        return await self.request(Route("GET", "/guilds/{guild_id}/members", guild_id=guild_id), json=json_req)

    async def find_guild_members(self, guild_id: Snowflake, query: str, limit: int = 1):
        json_req: Dict[str, Any] = {"query":query, "limit":limit}
        return await self.request(Route("GET", "/guilds/{guild_id}/members/search", guild_id=guild_id), json=json_req)

    async def modify_guild_member(self, guild_id: Snowflake, user_id: Snowflake, new_guild_member: Dict[str, Any]):
        return await self.request(Route("PATCH", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id), json=new_guild_member)

    async def modify_current_guild_member(self, guild_id: Snowflake, nick: str):
        return await self.request(Route("PATCH", "/guilds/{guild_id}/members/@me", guild_id=guild_id), json={"nick":nick})

    async def remove_guild_member(self, guild_id: Snowflake, user_id: Snowflake):
        return await self.request(Route("DELETE", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id))

    async def add_guild_member_role(self, guild_id: Snowflake, user_id: Snowflake, role_id: Snowflake):
        return await self.request(Route("PUT", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}", guild_id=guild_id, user_id=user_id, role_id=role_id))

    async def remove_guild_member_role(self, guild_id: Snowflake, user_id: Snowflake, role_id: Snowflake):
        return await self.request(Route("DELETE", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}", guild_id=guild_id, user_id=user_id, role_id=role_id))

    # Message HTTP functions

    async def get_messages(self, channel_id: Snowflake, /, limit: int = 50, around: Optional[Snowflake] = None, before: Optional[Snowflake] = None, after: Optional[Snowflake] = None):
        """Grabs all messages from a channel.
        Only one of the around, before, and after parameters can be set.

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
            The amount of messages to grab. The maximum is 100. Set to 50 by default
        """
        if limit < 1:
            raise ValueError("Got a limit that's smaller than 1")
        elif limit > 100:
            raise ValueError("Got a limit that's larger than 100")

        if (before and after and around) or (before and after) or (after and around) or (before and around):
            raise ValueError("Only one of before, around, and after can be set.") 

        url_link = "/channels/{channel_id}/messages?limit=" + str(limit)
        if around:
            url_link += "?around=" + str(around)
        if before:
            url_link += "?before=" + str(before)
        if after:
            url_link += "?after=" + str(after)

        return await self.request(Route("GET", url_link, channel_id=channel_id))

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
        return await self.request(
            Route("GET", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=message_id)
        )  

    async def get_pinned_messages(self, channel_id: Snowflake):
        """
        Gets all pinned messages from a channel.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to grab the pinned messages from.
        """
        return await self.request(Route("GET", "/channels/{channel_id}/pins", channel_id=channel_id))

    async def send_message(
        self, 
        channel_id: Snowflake, 
        /,
        content: str, 
        embed: Optional[Embed] = None, 
        embeds: Optional[List[Embed]] = None,
        msg_reference: Optional[MessageReference] = None,
        tts: bool = False
    ):
        """
        Sends a message to a channel.

        Parameters
        ----------
        channel_id: :type:`Snowflake`
            The id of the channel to send the message to
        content: :type:`str`
            The content of the message to send
        embed: :type:`Optional[Embed]`
            The embed to send. Set to None by default
        embeds: :type:`Optional[List[Embed]]`
            The embeds to send. Set to None by default
        msg_reference: :type:`Optional[MessageReference]`
            The message reference to send. Set to None by default
        tts: :type:`bool`
            Whether the message should be sent in text-to-speech. Set to False by default
        """
        json_data: Dict[str, Any] = {"content": content, "tts": tts}

        if embed and embeds:
            raise ValueError("Cannot send both embed and embeds")

        if embed:
            json_data["embeds"] = [embed.to_dict()]

        if embeds:
            json_data["embeds"] = [e.to_dict() for e in embeds]

        if msg_reference:
            json_data["message_reference"] = _message_reference_to_dict(msg_reference)

        return await self.request(Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id), json=json_data)

    async def crosspost_message(self, channel_id: Snowflake, message_id: Snowflake):
        return await self.request(Route("POST", "/channels/{channel_id}/messages/{message_id}/crosspost", channel_id=channel_id, message_id=message_id))

    async def edit_message(
        self,
        msg_id: Snowflake,
        channel_id: Snowflake,
        /,
        content: str,
        embed: Optional[Embed] = None, 
        embeds: Optional[List[Embed]] = None
    ):
        """
        Edits an existing message.

        Parameters
        ----------
        msg_id: :type:`Snowflake`
            The id of the message to edit
        channel_id: :type:`Snowflake`
            The id of the channel where the message is from
        content: :type:`str`
            The new content of the message to edit
        embed: :type:`Optional[Embed]`
            The new embed of the message to edit. Set to None by default
        embeds: :type:`Optional[List[Embed]]`
            The new embeds of the message to edit. Set to None by default
        """
        json_data: Dict[str, Any] = {"content": content}

        if embed and embeds:
            raise ValueError("Cannot send both embed and embeds")

        if embed:
            json_data["embeds"] = [embed.to_dict()]

        if embeds:
            json_data["embeds"] = [e.to_dict() for e in embeds]

        return await self.request(
            Route("PATCH", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=msg_id), 
            json=json_data
        )

    async def delete_message(self, msg_id: Snowflake, channel_id: Snowflake):
        """
        Deletes an existing message from a channel.

        Parameters
        ----------
        msg_id: :type:`Snowflake`
            The id of the message to delete
        channel_id: :type:`Snowflake`
            The id of the channel where the message is from
        """
        return await self.request(Route("DELETE", "/channels/{channel_id}/messages/{message_id}", channel_id=channel_id, message_id=msg_id))

    async def bulk_delete_messages(self, messages: List[Snowflake], channel_id: Snowflake):
        """
        Bulk deletes messages from a channel.

        Parameters
        ----------
        messages: :type:`List[Snowflake]`
            A list of the id of the messages to delete
        channel_id: :type:`Snowflake`
            The id of the channel where the messages are from
        """
        return await self.request(
            Route("POST", "/channels/{channel_id}/messages/bulk-delete", channel_id=channel_id),
            json={"messages":messages}
        )

    async def pin_message(self, msg_id: Snowflake, channel_id: Snowflake):
        """
        Pins a new message to the provided channel id.

        Parameters
        ----------
        msg_id: :type:`Snowflake`
            The id of the message to pin
        channel_id: :type:`Snowflake`
            The id of the channel to pin the message to
        """
        return await self.request(Route("PUT", "/channels/{channel_id}/pins/{message_id}", channel_id=channel_id, message_id=msg_id))

    async def unpin_message(self, msg_id: Snowflake, channel_id: Snowflake):
        """
        Unpins a message to the provided channel id.

        Parameters
        ----------
        msg_id: :type:`Snowflake`
            The id of the message to unpin
        channel_id: :type:`Snowflake`
            The id of the channel to unpin the message from
        """
        return await self.request(Route("DELETE", "/channels/{channel_id}/pins/{message_id}", channel_id=channel_id, message_id=msg_id))