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
import zlib
from typing import Any, Dict, Generic, TypeVar, Union

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

class HeartbeatHandler:
    def __init__(self, gw) -> None:
        self.gw = gw
        self.s = None

    async def loop(self):
        heartbeat_payload = {
            "op": GatewayOpcode.HEARTBEAT,
            "d": self.s
        }
        await self.gw.send_json(heartbeat_payload)

        msg = await self.gw.ws.receive()
        # let's assume the type of msg is text
        msg_json = json.loads(msg.data)
        gp = _map_dict_to_gateway_payload(msg_json)

        # TODO: Break connection if HEARTBEAT_ACK wasn't received

class GatewayClient:
    def __init__(self, ws: aiohttp.ClientWebSocketResponse, client):
        self.ws = ws
        self.inflator = zlib.decompressobj()
        self.client = client
        self.heartbeat_interval = 0
        self.recent_gp = GatewayPayload()
        self.heartbeat_handler = HeartbeatHandler(self)
    
    def decompress_msg(self, msg: bytes):
        out_str: str = ""

        # Message should be compressed
        if len(msg) < 4 or msg[-4:] != ZLIB_SUFFIX:
            return out_str

        buff = self.inflator.decompress(msg)
        out_str = buff.decode("utf-8")
        return out_str

    async def get_request(self):
        msg = await self.ws.receive()
        if msg.type == aiohttp.WSMsgType.BINARY:
            decompressed_msg = self.decompress_msg(msg.data)
            decompressed_msg = json.loads(decompressed_msg)
            self.recent_gp = _map_dict_to_gateway_payload(decompressed_msg)
            # TODO: Poll event
            
        elif msg.type == aiohttp.WSMsgType.TEXT:
            msg_json = json.loads(msg.data)
            self.recent_gp = _map_dict_to_gateway_payload(msg_json)
            # TODO: Poll event

    async def send_json(self, d: Dict[str, Any]):
        json_str = json.dumps(d)
        await self.ws.send_str(json_str)

    async def poll_event(self, gp: GatewayPayload):
        if gp.op == 10:
            send_gp = {
                "op": GatewayOpcode.IDENTIFY,
                "d": {
                    "token": self.client.token,
                    "properties": _identify_connection_properties,
                    "large_threshold": self.client.large_threshold,
                    "presence": self.client.user.presence,
                    "intents": self.client.raw_intents,
                }
            }
            await self.send_json(send_gp)
            self.heartbeat_interval = gp.d.get("heartbeat_interval")
            # TODO: Start heartbeat loop
