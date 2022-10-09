# SPDX-License-Identifier: MIT

import asyncio
from typing import Optional

from discatcore import Dispatcher, GatewayReconnect
from discatcore.gateway import GatewayClient
from discatcore.http import HTTPClient

from .event.protos import RawGatewayEvents, apply_events

__all__ = ("Bot",)


class Bot(Dispatcher):
    __slots__ = (
        "_raw_dispatcher",
        "http",
        "gateway",
        "running",
        "loop",
    )

    def __init__(self, *, token: str, api_version: Optional[int] = None, intents: int) -> None:
        self._raw_dispatcher: Dispatcher = Dispatcher()
        apply_events(source=RawGatewayEvents, dest=self._raw_dispatcher)
        self.http: HTTPClient = HTTPClient(token, api_version=api_version)
        self.gateway: GatewayClient = GatewayClient(
            self.http, self._raw_dispatcher, intents=intents
        )
        self.running: bool = False
        self.loop = asyncio.new_event_loop()

    @property
    def api_version(self) -> int:
        return self.http.api_version

    @property
    def intents(self) -> int:
        return self.gateway.intents

    @property
    def token(self) -> str:
        return self.http.token

    @property
    def raw_dispatcher(self) -> Dispatcher:
        return self._raw_dispatcher

    async def start(self) -> None:
        gateway_url: Optional[str] = None
        self.running = True

        while self.running:
            try:
                await self.gateway.connect(gateway_url)
            except GatewayReconnect as gr:
                gateway_url = gr.url

    async def stop(self) -> None:
        self.running = False
        await self.gateway.close(reconnect=False)
        await self.http.close()

    def run(self) -> None:
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(self.stop())
            self.loop.close()
