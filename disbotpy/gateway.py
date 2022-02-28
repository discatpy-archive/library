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

import asyncio
import json
import random
import aiohttp
import platform
import threading
import datetime
import zlib
from typing import Any, Dict, List, Union, Optional

from .types.activities import Activity
from .types.gateway import GatewayPayload, GatewayOpcode

__all__ = (
    "GatewayClient",
)

ZLIB_SUFFIX = b'\x00\x00\xff\xff'

_identify_connection_properties = {
    "$os": platform.uname().system,
    "$browser": "disbotpy",
    "$device": "disbotpy",
}

def _map_dict_to_gateway_payload(d: Dict[str, Any]):
    output: GatewayPayload = GatewayPayload()
    output.op = d.get("op", -1)
    output.d = d.get("d")
    output.s = d.get("s")
    output.t = d.get("t")
    return output

def decompress_msg(inflator, msg: bytes):
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
    client
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
    keep_alive_thread: :class:`threading.Thread`
        The thread used to keep the connection alive
    """
    def __init__(self, ws: aiohttp.ClientWebSocketResponse, client, heartbeat_timeout: float = 30.0):
        self.ws: aiohttp.ClientWebSocketResponse = ws
        self.inflator = zlib.decompressobj()
        self.client = client
        self.heartbeat_interval: float = 0.0
        self.seq_num: Optional[int] = None
        self.session_id: str = ""
        self.recent_gp: GatewayPayload = GatewayPayload()
        self.keep_alive_thread: Optional[threading.Thread] = None
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
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.client.http.token,
                "intents": self.client.intents,
                "properties": _identify_connection_properties,
                "large_threshold": 250,
            }
        }

        if self.client.me.presence is not None:
            identify_dict["d"]["presence"] = self.client.user.presence.to_dict()

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
        self.keep_alive_thread.join()
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
                    "op": GatewayOpcode.RESUME,
                    "d": {
                        "token": self.client.token,
                        "session_id": self.session_id,
                        "seq": self.seq_num,
                    }
                }
                await self.ws.send_json(resume_dict)
                self._gateway_resume = False

            if (datetime.datetime.now() - self._last_heartbeat_ack).total_seconds() > self.heartbeat_timeout:
                await self.close(code=1008)

            try:
                # maybe re-add timeout?
                msg = await self.ws.receive()
            except asyncio.TimeoutError:
                # try to re-establish the connection with the Gateway
                await self.close(code=1012)

            if msg.type == aiohttp.WSMsgType.BINARY:
                # we should be able to say that the type of the message is binary and its compressed
                inflated_msg = decompress_msg(self.inflator, msg.data)
                inflated_msg = json.loads(inflated_msg)
                self.recent_gp = _map_dict_to_gateway_payload(inflated_msg)

                self.seq_num = self.recent_gp.s
                await self.poll_event()
            elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING):
                # we got a close code
                await self.close(reconnect=False)

    async def poll_event(self):
        """
        Polls the latest message from the server.

        For internal use only.
        """
        if self.recent_gp.op == GatewayOpcode.DISPATCH:
            if self.recent_gp.t == "READY":
                self.session_id = self.recent_gp.d["session_id"]
                # TODO: Add (unavailable) guilds to the client cache
            else:
                await self.poll_dispatched_event()

        if self.recent_gp.op == GatewayOpcode.RECONNECT:
            await self.close(code=1012)
        
        if self.recent_gp.op == GatewayOpcode.INVALID_SESSION:
            resumable: bool = self.recent_gp.d if isinstance(self.recent_gp.d, bool) else False
            self._gateway_resume = resumable
            await self.close(code=1012)
            await self.client._gateway_reconnect.set()

        if self.recent_gp.op == GatewayOpcode.HELLO:
            self.heartbeat_interval = self.recent_gp.d["heartbeat_interval"] / 1000
            await self.ws.send_json(self.identify_payload())
            self.keep_alive_thread = threading.Thread(target=self.keep_alive_run)
            self.keep_alive_thread.start()
        
        if self.recent_gp.op == GatewayOpcode.HEARTBEAT_ACK:
            self._last_heartbeat_ack = datetime.datetime.now()

    async def poll_dispatched_event(self):
        """
        Polls the latest dispatched event from the server.

        For internal use only.
        """
        # TODO: Implement events
        print("Unimplemented.")
        
    async def request_guild_members(self, guild_id: int, user_ids: Optional[Union[int, List[int]]], limit: int = 0, query: str = "", presences: bool = False):
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
            "op": GatewayOpcode.REQUEST_GUILD_MEMBERS,
            "d": {
                "guild_id": str(guild_id),
                "query": query,
                "limit": limit,
                "presences": presences,
            }
        }

        if user_ids is not None:
            guild_mems_req["d"]["user_ids"] = user_ids

        await self.ws.send_json(guild_mems_req)

    async def update_presence(self, since: int, activities: List[Activity], status: str, afk: bool):
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
            "op": GatewayOpcode.PRESENCE_UPDATE,
            "d": {
                "since": since,
                "activities": [],
                "status": status,
                "afk": afk,
            }
        }

        # TODO: Move this script to a to_dict function for Activities
        for i in activities:
            new_presence_dict["d"]["activities"].append({
                "name": i.name,
                "type": i.type,
                "url": i.url,
            })

        await self.ws.send_json(new_presence_dict)

    async def keep_alive_loop(self):
        """
        Executes the keep alive loop, which is the following:

        - sends a heartbeat payload with the sequence number
        - wait for the set heartbeat_interval time defined by the server
            - if this is the first heartbeat, then we multiply that time with a jitter (value between 0 and 1)
        
        Do not run this yourself. keep_alive_run will start this for you.
        """
        while not self.ws.closed:
            heartbeat_payload = {
                "op": GatewayOpcode.HEARTBEAT,
                "d": self.seq_num
            }
            await self.ws.send_json(heartbeat_payload)

            delta = self.heartbeat_interval
            if self._first_heartbeat:
                delta *= random.uniform(0.0, 1.0)
                self._first_heartbeat = False
            await asyncio.sleep(delta)

    def keep_alive_run(self):
        """
        Runs the keep_alive_loop until it is complete.

        Do not run this yourself. poll_event will start this for you in a new thread 
        when it receives opcode 10 (Hello payload).
        """
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self.keep_alive_loop())
        except asyncio.CancelledError or asyncio.TimeoutError:
            pass
