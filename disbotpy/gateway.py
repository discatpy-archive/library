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
from typing import Any, Dict, Optional

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
    """The Gateway Client between your Bot and Discord
    
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
        self.recent_gp: GatewayPayload = GatewayPayload()
        self.keep_alive_thread: Optional[threading.Thread] = None
        self._first_heartbeat: bool = True
        self._last_heartbeat_ack: Optional[datetime.datetime] = None
        self.heartbeat_timeout: float = heartbeat_timeout
        self._gateway_resumable: bool = False

    def identify_payload(self):
        """
        Returns the identifcation payload. 
        For internal use only.
        """
        identify_dict = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.client.token,
                "intents": self.client.intents,
                "properties": _identify_connection_properties,
                "large_threshold": 250,
            }
        }

        if self.client.user.presence is not None:
            identify_dict["d"]["presence"] = self.client.user.presence.to_dict()

        return identify_dict

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
            if (datetime.datetime.now() - self._last_heartbeat_ack).total_seconds() > self.heartbeat_timeout:
                self.ws.close(code=1008)
                await self.client._gateway_reconnect.set()

            msg = await self.ws.receive()

            # we should be able to say that the type of the message is binary and its compressed
            inflated_msg = decompress_msg(self.inflator, msg)
            inflated_msg = json.loads(inflated_msg)
            self.recent_gp = _map_dict_to_gateway_payload(inflated_msg)

            await self.poll_event()

    async def poll_event(self):
        """
        Polls the latest message from the server. 
        For internal use only.
        """
        if self.recent_gp.op == GatewayOpcode.DISPATCH:
            # TODO: Tell the client that there is a new event
            print("Unimplemented.")

        if self.recent_gp.op == GatewayOpcode.RECONNECT:
            self.ws.close(code=1012)
            await self.client._gateway_reconnect.set()
        
        if self.recent_gp.op == GatewayOpcode.INVALID_SESSION:
            resumable: bool = self.recent_gp.d if isinstance(self.recent_gp.d, bool) else False
            self._gateway_resumable = resumable
            self.ws.close(code=1012)
            await self.client._gateway_reconnect.set()

        if self.recent_gp.op == GatewayOpcode.HELLO:
            self.heartbeat_interval = self.recent_gp.d["heartbeat_interval"] / 1000
            await self.ws.send_json(self.identify_payload())
            self.keep_alive_thread = threading.Thread(target=self.keep_alive_run)
        
        # TODO: Maybe move to the keep alive thread?
        if self.recent_gp.op == GatewayOpcode.HEARTBEAT_ACK:
            self._last_heartbeat_ack = datetime.datetime.now()

    async def keep_alive_loop(self):
        """
        Executes the keep alive loop, which is the following:
        - sends a heartbeat payload with the sequence number
        - wait for the set heartbeat_interval time defined by the server
            - if this is the first heartbeat, then we multiply that time with a jitter (value between 0 and 1)
        Do not run this yourself. Instead, use keep_alive_run.
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
        loop.run_until_complete(self.keep_alive_loop())
