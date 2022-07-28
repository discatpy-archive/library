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
import logging
from typing import Callable, Optional

from .dispatcher import Dispatcher, Event
from .flags import Intents
from .gateway import GatewayClient, GatewayEventHandler, GatewayEventProtos
from .http import HTTPClient

__all__ = ("Client",)

_log = logging.getLogger(__name__)


def get_loop():
    try:
        return asyncio.get_running_loop()
    except:
        return asyncio.new_event_loop()


# Taken from discord.py
def _cancel_all_tasks():
    loop = get_loop()
    tasks = {t for t in asyncio.all_tasks(loop) if not t.done()}

    if not tasks:
        return

    _log.info("Cleaning up %d tasks found in event loop.", len(tasks))
    for t in tasks:
        t.cancel()

    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    _log.info("Finish cancelling all tasks.")

    for t in tasks:
        if t.cancelled():
            continue

        if t.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "Unhandled exception during Client.run shutdown.",
                    "exception": t.exception(),
                    "task": t,
                }
            )


# Taken from discord.py
def _cleanup_loop():
    loop = get_loop()
    try:
        _cancel_all_tasks()
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        _log.info("Closing the event loop.")
        loop.close()


class Client:
    """
    The main client that joins the developer's code and the Discord API together.

    Parameters
    ----------
    token: :type:`str`
        The token for this client.
    intents: :type:`Intents`
        The intents for the gateway.
    api_version: :type:`Optional[int]`
        The api version of the HTTP Client.
        This is automatically set to `None`, which will be set to `9`.

    Attributes
    ----------
    gateway: :type:`Optional[GatewayClient]`
        The gateway client that handles connections with the gateway.
    http: :type:`HTTPClient`
        The http client that handles connections with the REST API.
    running: :type:`bool`
        Whether or not the client is running.
    intents: :type:`Intents`
        The intents for the gateway.
    dispatcher: :type:`Dispatcher`
        The event dispatcher for Gateway events.
    """

    __slots__ = (
        "gateway",
        "event_protos_handler",
        "_event_protos_handler_hooked",
        "_event_handler_hooked",
        "event_handler",
        "http",
        "_gateway_reconnect",
        "running",
        "closed",
        "intents",
        "dispatcher",
    )

    def __init__(
        self, token: str, *, intents: Intents = Intents.DEFAULT(), api_version: Optional[int] = None
    ):
        self.gateway: Optional[GatewayClient] = None  # initalized later
        self.dispatcher: Dispatcher = Dispatcher(self)
        # pyright thinks that this is a dynamic instance attribute and not a class attribute (see below)
        self.event = self.dispatcher.event  # type: ignore
        self._event_protos_handler_hooked: bool = False
        self.event_protos_handler: GatewayEventProtos = GatewayEventProtos(
            self
        )  # TODO: maybe remove keeping a reference to this?
        self.event_handler: GatewayEventHandler = GatewayEventHandler(self)
        self.http: HTTPClient = HTTPClient(token, api_version=api_version)
        self._gateway_reconnect = asyncio.Event()
        self.running: bool = False
        self.closed: bool = False
        self.intents: Intents = intents

    # Properties

    @property
    def token(self):
        """:class:`str` The bot's token. Shortcut for :attr:`Client.http.token`."""
        return self.http.token

    @property
    def api_version(self):
        """:class:`int` The api version the HTTP Client is using. Shortcut for :attr:`Client.http._api_version`."""
        return self.http._api_version

    @property
    def loop(self):
        """:class:`asyncio.AbstractEventLoop` The main event loop. This is either a new loop or the current running loop."""
        return get_loop()

    # Events

    def event(
        self,
        *,
        proto: Optional[bool] = None,
        callback: Optional[bool] = None,
        name: Optional[str] = None,
        parent: bool = False,
        one_shot: bool = False,
    ) -> Callable[..., Event]:
        raise NotImplementedError

    # Running logic

    async def login(self):
        """Logs into the bot user and grabs its user object."""
        # Implemented in the wrapper's bot
        pass

    async def close(self):
        if self.closed:
            return

        self.closed = True

        if self.gateway is not None:
            await self.gateway.close(reconnect=False)
        await self.http.close()

    async def connect(self):
        """Runs the Gateway Client and reconnects when prompted."""
        gateway_info = await self.http.get_gateway_bot()
        ws = await self.http.ws_connect(gateway_info["url"])
        self.gateway = GatewayClient(ws, self)
        self.running = True

        while self.running:
            try:
                await self.gateway.loop()

                # if we get here, then we probably have to reconnect
                if self._gateway_reconnect.is_set():
                    self.gateway.ws = await self.http.ws_connect(gateway_info["url"])
                    self._gateway_reconnect.clear()
                else:
                    # we cannot reconnect, so we must stop the program
                    self.running = False
            except Exception as e:
                await self.dispatcher.error_handler(e)

    async def start(self):
        """An asynchronous function that calls :meth:`~.login` and :meth:`~.connect`."""
        await self.login()
        await self.connect()

    def run(self):
        """Starts the Gateway client in a blocking, synchronous way.

        If you need to run another asynchronous function before the client starts, then use :meth:`~.start`.
        """
        loop = self.loop

        try:
            loop.run_until_complete(self.start())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self.close())
            _log.info("Cleaning up unfinished tasks.")
            _cleanup_loop()
