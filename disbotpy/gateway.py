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
import aiohttp
import platform
import threading
import zlib
from typing import Any, Dict, Generic, TypeVar, Union, Optional

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

def decompress_msg(inflator: zlib._Decompress, msg: bytes):
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
    def __init__(self, ws: aiohttp.ClientWebSocketResponse, client):
        self.ws: aiohttp.ClientWebSocketResponse = ws
        self.inflator = zlib.decompressobj()
        self.client = client
        self.heartbeat_interval: float = 0.0
        self.seq_num: Optional[int] = None
        self.recent_gp: GatewayPayload = GatewayPayload()
        self.keep_alive_thread: Optional[threading.Thread] = None

    def identify_payload(self):
        identify_dict = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.client.token,
                "intents": self.client.intents,
                "properties": _identify_connection_properties,
                "large_threshold": 250,
            }
        }

        if self.client.intents is not None:
            identify_dict["d"]["intents"] = self.client.intents.raw
        if self.client.user.presence is not None:
            identify_dict["d"]["presence"] = self.client.user.presence.to_dict()

        return identify_dict

    async def loop(self):
        while True:
            if self.ws.closed:
                break

            msg = await self.ws.receive()

            # we should be able to say that the type of the message is binary and its compressed
            inflated_msg = decompress_msg(self.inflator, msg)
            inflated_msg = json.loads(inflated_msg)
            self.recent_gp = _map_dict_to_gateway_payload(inflated_msg)

            await self.poll_event()

    async def poll_event(self):
        if self.recent_gp.op == GatewayOpcode.HELLO:
            self.heartbeat_interval = self.recent_gp.d["heartbeat_interval"] / 1000
            await self.ws.send_json(self.identify_payload())
            self.keep_alive_thread = threading.Thread(target=self.keep_alive_run)

    async def keep_alive_loop(self):
        while True:
            if self.ws.closed:
                break

            heartbeat_payload = {
                "op": GatewayOpcode.HEARTBEAT,
                "d": self.seq_num
            }
            await self.ws.send_json(heartbeat_payload)

            msg = await self.ws.receive_json()

            # we should be able to say that the type of the message is binary and its compressed
            inflated_msg = decompress_msg(self.inflator, msg)
            inflated_msg = json.loads(inflated_msg)
            gp = _map_dict_to_gateway_payload(inflated_msg)

            asyncio.sleep(self.heartbeat_interval)

    def keep_alive_run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.keep_alive_loop())
