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
from typing import Any, Callable, Coroutine, Optional

from .dispatcher import Dispatcher
from .flags import Intents
from .gateway import GatewayClient, GatewayEventProtos, GatewayEventHandler
from .http import HTTPClient

__all__ = ("Client",)


def get_loop():
    try:
        return asyncio.get_running_loop()
    except:
        return asyncio.new_event_loop()


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
        "intents",
        "dispatcher",
    )

    def __init__(self, token: str, *, intents: Intents, api_version: Optional[int] = None):
        self.gateway: Optional[GatewayClient] = None  # initalized later
        self.dispatcher: Dispatcher = Dispatcher()
        self._event_protos_handler_hooked: bool = False
        self.event_protos_handler: GatewayEventProtos = GatewayEventProtos(self) # TODO: maybe remove keeping a reference to this?
        self.event_handler: GatewayEventHandler = GatewayEventHandler(self)
        self.http: HTTPClient = HTTPClient(token, api_version=api_version)
        self._gateway_reconnect = asyncio.Event()
        self.running: bool = False
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

    # Events

    def event(self, name: Optional[str] = None):
        """A decorator that registers a function as an event callback.

        Parameters
        ----------
        name: :type:`Optional[str]` = `None`
            The name of this event. If none, then the function's name is used.
        """

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            event_name = self.dispatcher._get_event_name(func, name)

            if not self.dispatcher.has_event(event_name):
                self.dispatcher.set_event_proto(func, name=name)

            # TODO: parent
            self.dispatcher.add_event_callback(func, name=name)
            return func

        return decorator

    # Running logic

    async def login(self):
        """Logs into the bot user and grabs its user object."""
        # TODO: Readd?
        # user_dict = await self.http.login(token)
        # self.me = User(user_dict, self)
        # self.cache.add_user(self.me)

    async def _end_run(self):
        if self.gateway is not None:
            await self.gateway.close(reconnect=False)
        await self.http.close()

    async def gateway_run(self):
        """Runs the Gateway Client code and reconnects when prompted."""
        gateway_info = await self.http.get_gateway_bot()
        self.gateway = GatewayClient(await self.http.ws_connect(gateway_info.get("url")), self)
        self.running = True

        while self.running:
            try:
                await self.gateway.loop()

                # if we get here, then we probably have to reconnect
                if self._gateway_reconnect.is_set():
                    self.gateway.ws = await self.http.ws_connect(gateway_info.get("url"))
                    self._gateway_reconnect.clear()
                else:
                    # we cannot reconnect, so we must stop the program
                    self.running = False
            except Exception as e:
                await self.dispatcher.error_handler(e)

    def run(self):
        """Starts the Gateway client in a blocking, synchronous"""

        async def wrapped():
            await self.login()
            await self.gateway_run()

        loop = get_loop()
        try:
            loop.run_until_complete(wrapped())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self._end_run())
