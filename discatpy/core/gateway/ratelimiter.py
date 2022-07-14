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
from datetime import datetime
import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import GatewayClient

__all__ = ("Ratelimiter",)

_log = logging.getLogger(__name__)


class Ratelimiter:
    """Represents a ratelimiter for a Gateway Client."""

    __slots__ = (
        "commands_used",
        "parent",
        "_task",
        "_ratelimit_done",
        "_lock",
        "cmds_per_time_frame",
        "time_frame",
    )

    def __init__(self, parent: GatewayClient, cmds_per_time_frame: int = 120, time_frame: int = 60):
        self.commands_used = 0
        self.cmds_per_time_frame = cmds_per_time_frame
        self.time_frame = time_frame
        self.parent = parent
        self._task: Optional[asyncio.Task] = None
        self._ratelimit_done = asyncio.Event()
        self._lock = asyncio.Event()

    async def ratelimit_loop(self):
        """Updates the amount of commands used per minute."""
        while not self.parent.ws.closed:
            try:
                self._ratelimit_done.clear()

                await asyncio.sleep(self.time_frame)

                self._ratelimit_done.set()
                self.commands_used = 0
            except asyncio.CancelledError:
                break

    def start(self):
        """Starts the ratelimiter task which updates the commands used per minute."""
        if not self._task:
            self._task = asyncio.create_task(self.ratelimit_loop())
            _log.info("Started Gateway ratelimiting task.")

    async def stop(self):
        """Stops the ratelimiter task."""
        if self._task:
            self._task.cancel()
            await self._task
            _log.info("Stopped Gateway ratelimiting task.")

    def add_command_usage(self):
        self.commands_used += 1
        _log.debug("A Gateway command has been used.")

    def is_ratelimited(self):
        return self.commands_used == self.cmds_per_time_frame - 1

    async def set(self):
        """Sets the lock until the ratelimit is finished."""
        start_time = datetime.now()
        _log.info("Starting Gateway ratelimiting.")

        self._lock.clear()
        await self._ratelimit_done.wait()
        self._lock.set()

        end_time = datetime.now()
        _log.info("Gateway ratelimiting has finished. It took %f seconds.", (end_time - start_time).total_seconds())

    async def wait(self):
        """Waits for the lock to be unlocked."""
        if not self._lock.is_set():
            start_time = datetime.now()
            _log.info("Waiting for Gateway ratelimit lock.")

            await self._lock.wait()

            end_time = datetime.now()
            _log.info("Done waiting for the Gateway ratelimit lock. It took %f seconds.", (end_time - start_time).total_seconds())
