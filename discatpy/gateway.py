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
from __future__ import annotations

import asyncio
import datetime
import json
import platform
import random
import zlib
from typing import TYPE_CHECKING, Any, List, Optional, Union

import aiohttp
from typing_extensions import TypedDict

from .enums.gateway import GatewayOpcode
from .types.snowflake import *

if TYPE_CHECKING:
    from .client import Client

__all__ = (
    "GatewayPayload",
    "GatewayClient",
)


class GatewayPayload(TypedDict):
    op: int
    d: Optional[Any]
    s: Optional[int]
    t: Optional[str]


ZLIB_SUFFIX = b"\x00\x00\xff\xff"

_identify_connection_properties = {
    "os": platform.uname().system,
    "browser": "discatpy",
    "device": "discatpy",
}


def decompress_msg(inflator: zlib._Decompress, msg: bytes):
    """
    Decompresses the message with the provided object from
    zlib.decompressobj().

    Parameters
    ----------
    inflator:
        The object returned from zlib.decompressobj()
    msg: :type:`bytes`
        The compressed message
    """
    out_str: str = ""

    # Message should be compressed
    if len(msg) < 4 or msg[-4:] != ZLIB_SUFFIX:
        return out_str

    buff = inflator.decompress(msg)
    out_str = buff.decode("utf-8")
    return out_str


class GatewayClient:
    """
    The Gateway Client between your Bot and Discord

    Parameters
    ----------
    ws: :class:`aiohttp.ClientWebSocketResponse`
        The websockets response
    client: :class:`Client`
        The Client
    heartbeat_timeout: :class:`int`
        The amount of time (in seconds) to wait for a heartbeat ack
        to come in.

    Attributes
    ----------
    inflator: :class:`zlib.decompressobj`
        The Gateways inflator
    heartbeat_interval: :class:`float`
        The interval to heartbeat given by Discord
    seq_num: :class:`int`
        The current sequence number
    session_id: :class:`str`
        The session id of this Gateway connection
    recent_gp: :class:`GatewayPayload`
        The newest Gateway Payload
    keep_alive_task: :class:`Optional[asyncio.Task]`
        The task used to keep the connection alive
    """

    def __init__(
        self,
        ws: aiohttp.ClientWebSocketResponse,
        client: Client,
        heartbeat_timeout: float = 30.0,
    ):
        self.ws: aiohttp.ClientWebSocketResponse = ws
        self.inflator = zlib.decompressobj()
        self.client: Client = client
        self.heartbeat_interval: float = 0.0
        self.seq_num: Optional[int] = None
        self.session_id: str = ""
        self.recent_gp: GatewayPayload = GatewayPayload()
        self.keep_alive_task: Optional[asyncio.Task] = None
        self._first_heartbeat: bool = True
        self._last_heartbeat_ack: datetime.datetime = datetime.datetime.now()
        self.heartbeat_timeout: float = heartbeat_timeout
        self._gateway_resume: bool = False

    def identify_payload(self):
        """
        Returns the identifcation payload.

        For internal use only.
        """
        identify_dict = {
            "op": GatewayOpcode.IDENTIFY.value,
            "d": {
                "token": self.client.token,
                "intents": self.client.intents.value,
                "properties": _identify_connection_properties,
                "large_threshold": 250,
            },
        }

        # TODO: Presence support

        return identify_dict

    async def close(self, code: int = 1000, reconnect: bool = True):
        """
        Closes the connection with the gateway.

        For internal use only.

        Parameters
        ----------
        code: :type:`int`
            The websocket code to close with. Set to 1000 by default
        reconnect: :type:`bool`
            If we should reconnect or not. Set to True by default
        """
        await self.ws.close(code=code)
        await self.keep_alive_task

        if reconnect:
            await self.client._gateway_reconnect.set()

    async def loop(self):
        """
        Executes the main Gateway loop, which is the following:

        - compare the last time the heartbeat ack was sent from the server to current time
            - if that comparison is greater than the heartbeat timeout, then we reconnect
        - receive the latest message from the server
        - decompress and convert this message to the GatewayPayload format
        - poll the latest message to see what to do

        """
        while not self.ws.closed:
            if self._gateway_resume:
                resume_dict = {
                    "op": GatewayOpcode.RESUME.value,
                    "d": {
                        "token": self.client.token,
                        "session_id": self.session_id,
                        "seq": self.seq_num,
                    },
                }
                await self.ws.send_json(resume_dict)
                self._gateway_resume = False

            if (
                datetime.datetime.now() - self._last_heartbeat_ack
            ).total_seconds() > self.heartbeat_timeout:
                await self.close(code=1008)

            try:
                msg = await self.ws.receive()
            except asyncio.TimeoutError:
                # try to re-establish the connection with the Gateway
                await self.close(code=1012)

            if msg.type == aiohttp.WSMsgType.BINARY or msg.type == aiohttp.WSMsgType.TEXT:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    inflated_msg = decompress_msg(self.inflator, msg.data)
                else:
                    inflated_msg = msg.data

                inflated_msg = json.loads(inflated_msg)
                self.recent_gp = GatewayPayload(inflated_msg)

                self.seq_num = self.recent_gp["s"]
                await self.poll_event()
            elif msg.type in (
                aiohttp.WSMsgType.CLOSE,
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.CLOSING,
            ):
                # we got a close code
                await self.close(reconnect=False)

    async def poll_event(self):
        """
        Polls the latest message from the server.

        For internal use only.
        """
        # Manages all event dispatches
        if self.recent_gp["op"] == GatewayOpcode.DISPATCH.value:
            await self.poll_dispatched_event()

        # Attempts to reconnect to the Gateway when prompted
        if self.recent_gp["op"] == GatewayOpcode.RECONNECT.value:
            await self.close(code=1012)

        # This connection session is invalid: if we can resume, then resume. Otherwise, reconnect.
        if self.recent_gp["op"] == GatewayOpcode.INVALID_SESSION.value:
            resumable: bool = (
                self.recent_gp["d"] if isinstance(self.recent_gp["d"], bool) else False
            )
            self._gateway_resume = resumable
            await self.close(code=1012)

        # Handles the hello message (means we successfully connected) with the identify payload and keep alive loop
        if self.recent_gp["op"] == GatewayOpcode.HELLO.value:
            self.heartbeat_interval = self.recent_gp["d"]["heartbeat_interval"] / 1000
            await self.ws.send_json(self.identify_payload())
            self.keep_alive_task = asyncio.create_task(self.keep_alive_loop())

        # Handles a heartbeat acknowledge to prevent our system from thinking the connection is "zombied"
        if self.recent_gp["op"] == GatewayOpcode.HEARTBEAT_ACK.value:
            self._last_heartbeat_ack = datetime.datetime.now()

    async def poll_dispatched_event(self):
        """
        Polls the latest dispatched event from the server.

        For internal use only.
        """
        args: List[Any] = ()

        # TODO: Parse event data into arguments
        if self.recent_gp["t"] == "READY":
            self.session_id = self.recent_gp["d"]["session_id"]
            # TODO: Add (unavailable) guilds to the client cache

        name = "on_" + self.recent_gp["t"].lower()
        await self.client.dispatcher.dispatch(name, *args)

    async def request_guild_members(
        self,
        guild_id: Snowflake,
        user_ids: Optional[Union[Snowflake, List[Snowflake]]] = None,
        limit: int = 0,
        query: str = "",
        presences: bool = False,
    ):
        """
        Sends a command to the Gateway requesting members from a certain guild.

        When the chucks of the members are received, they will be automatically
        inserted into the client's cache.

        Parameters
        ----------
        guild_id: :type:`int`
            The guild ID we are requesting members from
        user_ids: :type:`Optional[Union[int, List[int]]]`
            The user id(s) to request. Set to nothing by default
        limit: :type:`int`
            The maximum amount of members to grab. Set to 0 by default
        query: :type:`str`
            The string the username starts with. Set to "" by default
        presences: :type:`bool`
            If we want to grab the presences of the members. Set to False by default
        """
        guild_mems_req = {
            "op": GatewayOpcode.REQUEST_GUILD_MEMBERS.value,
            "d": {
                "guild_id": str(guild_id),
                "query": query,
                "limit": limit,
                "presences": presences,
            },
        }

        if user_ids is not None:
            guild_mems_req["d"]["user_ids"] = user_ids

        await self.ws.send_json(guild_mems_req)

    async def update_presence(self, since: int, status: str, afk: bool):
        """
        Sends a presence update to the Gateway.

        Parameters
        ----------
        since: :type:`int`
            When the bot went AFK
        activities: :type:`List[Activity]`
            The current activities
        status: :type:`str`
            The current status of the bot now
        afk: :type:`bool`
            If the bot is AFK or not
        """
        new_presence_dict = {
            "op": GatewayOpcode.PRESENCE_UPDATE.value,
            "d": {
                "since": since,
                "activities": [],
                "status": status,
                "afk": afk,
            },
        }

        # TODO: Activities

        await self.ws.send_json(new_presence_dict)

    async def keep_alive_loop(self):
        """
        Executes the keep alive loop, which is the following:

        - sends a heartbeat payload with the sequence number
        - wait for the set heartbeat_interval time defined by the server
            - if this is the first heartbeat, then we multiply that time with a jitter (value between 0 and 1)

        Do not run this yourself. The Gateway will automatically start an `asyncio.Task` to run this.
        """
        while not self.ws.closed:
            heartbeat_payload = {"op": GatewayOpcode.HEARTBEAT.value, "d": self.seq_num}
            await self.ws.send_json(heartbeat_payload)

            delta = self.heartbeat_interval
            if self._first_heartbeat:
                delta *= random.uniform(0.0, 1.0)
                self._first_heartbeat = False

            try:
                await asyncio.sleep(delta)
            except asyncio.CancelledError:
                break
