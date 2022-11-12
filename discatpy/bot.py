# SPDX-License-Identifier: MIT

import asyncio
import typing as t

from discatcore import Dispatcher, GatewayReconnect
from discatcore.gateway import GatewayClient
from discatcore.http import HTTPClient
from typing_extensions import Self

from .event.protos import RawGatewayEvents, apply_events
from .flags import Flag, flag

__all__ = ("Intents", "Bot")


class Intents(Flag):
    if t.TYPE_CHECKING:

        def __init__(
            self,
            *,
            guilds: bool = ...,
            guild_members: bool = ...,
            guild_bans: bool = ...,
            guild_emojis_and_stickers: bool = ...,
            guild_integrations: bool = ...,
            guild_webhooks: bool = ...,
            guild_invites: bool = ...,
            guild_voice_states: bool = ...,
            guild_presences: bool = ...,
            guild_messages: bool = ...,
            guild_message_reactions: bool = ...,
            guild_message_typing: bool = ...,
            direct_messages: bool = ...,
            direct_message_reactions: bool = ...,
            direct_message_typing: bool = ...,
            message_content: bool = ...,
            guild_scheduled_events: bool = ...,
            auto_moderation_configuration: bool = ...,
            automod_execution: bool = ...,
        ) -> None:
            ...

    @flag
    def GUILDS():
        return 1 << 0

    @flag
    def GUILD_MEMBERS():
        return 1 << 1

    @flag
    def GUILD_BANS():
        return 1 << 2

    @flag
    def GUILD_EMOJIS_AND_STICKERS():
        return 1 << 3

    @flag
    def GUILD_INTEGRATIONS():
        return 1 << 4

    @flag
    def GUILD_WEBHOOKS():
        return 1 << 5

    @flag
    def GUILD_INVITES():
        return 1 << 6

    @flag
    def GUILD_VOICE_STATES():
        return 1 << 7

    @flag
    def GUILD_PRESENCES():
        return 1 << 8

    @flag
    def GUILD_MESSAGES():
        return 1 << 9

    @flag
    def GUILD_MESSAGE_REACTIONS():
        return 1 << 10

    @flag
    def GUILD_MESSAGE_TYPING():
        return 1 << 11

    @flag
    def DIRECT_MESSAGES():
        return 1 << 12

    @flag
    def DIRECT_MESSAGE_REACTIONS():
        return 1 << 13

    @flag
    def DIRECT_MESSAGE_TYPING():
        return 1 << 14

    @flag
    def MESSAGE_CONTENT():
        return 1 << 15

    @flag
    def GUILD_SCHEDULED_EVENTS():
        return 1 << 16

    @flag
    def AUTO_MODERATION_CONFIGURATION():
        return 1 << 20

    @flag
    def AUTO_MODERATION_EXECUTION():
        return 1 << 21

    @classmethod
    def default(cls: type[Self]) -> Self:
        self = cls.all()
        self.GUILD_MEMBERS = False
        self.GUILD_PRESENCES = False
        self.MESSAGE_CONTENT = False
        return self


class Bot(Dispatcher):
    __slots__ = (
        "_raw_dispatcher",
        "http",
        "gateway",
        "running",
        "loop",
    )

    def __init__(
        self,
        *,
        token: str,
        api_version: t.Optional[int] = None,
        intents: Intents,
        heartbeat_timeout: float = 30.0,
    ) -> None:
        self._raw_dispatcher: Dispatcher = Dispatcher()
        apply_events(source=RawGatewayEvents, dest=self._raw_dispatcher)
        self.http: HTTPClient = HTTPClient(token, api_version=api_version)
        self.gateway: GatewayClient = GatewayClient(
            self.http,
            self._raw_dispatcher,
            intents=intents.value,
            heartbeat_timeout=heartbeat_timeout,
        )
        self.running: bool = False
        self.loop = asyncio.new_event_loop()

    @property
    def api_version(self) -> int:
        return self.http.api_version

    @property
    def intents(self) -> Intents:
        return Intents.from_value(self.gateway.intents)

    @property
    def token(self) -> str:
        return self.http.token

    @property
    def heartbeat_timeout(self) -> float:
        return self.gateway.heartbeat_timeout

    @property
    def raw_dispatcher(self) -> Dispatcher:
        return self._raw_dispatcher

    async def start(self) -> None:
        gateway_url: t.Optional[str] = None
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
