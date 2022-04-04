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
from typing import Optional

from .internal.dispatcher import *
from .gateway import GatewayClient
from .http import HTTPClient
from .user import User

__all__ = (
    "Client",
    "set_global_client",
    "get_global_client",
)

class Client:
    """
    The main client that joins the developer's code and the Discord API together.

    Attributes
    ----------
    gateway: :type:`Optional[GatewayClient]`
        The gateway client that handles connections with the gateway
    http: :type:`HTTPClient`
        The http client that handles connections with the REST API
    me: :type:`User`
        The bot user
    running: :type:`bool`
        Whether or not the client is running
    intents: :type:`int`
        The intents for the gateway
    dispatcher: :type:`Dispatcher`
        The event dispatcher for Gateway events
    """
    def __init__(self, intents: int):
        self.gateway: Optional[GatewayClient] = None # initalized later
        self.http: HTTPClient = HTTPClient()
        self.me: Optional[User] = None
        self._gateway_reconnect = asyncio.Event()
        self.running: bool = False
        self.intents: int = intents
        self.dispatcher: Dispatcher = Dispatcher()
    
    @property
    def token(self):
        """
        The bot's token. 
        Shortcut for `Client.http.token`.
        """
        return self.http.token

    async def login(self, token: str):
        """
        Logs into the bot user and grabs its user object.

        Do not run this yourself. `run()` will take care of this for you.

        Parameters
        ----------
        token: :type:`str`
            The token for the bot user
        """
        user_dict = await self.http.login(token)
        self.me = User.from_dict(user_dict)
        # TODO: Support setting the initial presence
        self.me.presence = None

    async def gateway_run(self):
        """
        Runs the Gateway Client code and reconnects when prompted.

        Do not run this yourself. `run()` will take care of this for you.
        """
        gateway_url = await self.http.get_gateway_bot()
        gateway_url = gateway_url[1]
        self.gateway = GatewayClient(await self.http.ws_connect(gateway_url), self)
        self.running = True

        while self.running:
            try:
                await self.gateway.loop()

                # if we get here, then we probably have to reconnect
                if self._gateway_reconnect.is_set():
                    self.gateway.ws = await self.http.ws_connect(gateway_url)
                else:
                    # we cannot reconnect, so we must stop the program
                    self.running = False
            except KeyboardInterrupt:
                self.running = False

        await self.gateway.close(reconnect=False)

    async def _run(self, token: str):
        await self.login(token)
        await self.gateway_run()

    def run(self, token: str):
        """
        Logs into the bot user then starts the Gateway client.

        Parameters
        ----------
        token: :type:`str`
            The token for the bot user
        """
        asyncio.run(self._run(token))

global_client: Client = None

def set_global_client(client: Client) -> None:
    """
    Sets the global client used throughout the library.

    Parameters
    ----------
    client: :type:`Client`
        The client to set as the global client
    """
    global global_client

    if global_client is not None:
        raise RuntimeError("Global Client is already set")

    global_client = client

def get_global_client() -> Client:
    """
    Gets the global client used throughout the library.

    Returns
    -------
    :type:`Client`
        The global client
    """
    global global_client

    if global_client is None:
        raise RuntimeError("Global Client is not set")

    return global_client