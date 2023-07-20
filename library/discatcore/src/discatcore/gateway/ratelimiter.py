# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import logging
import typing as t

from ..utils.ratelimit import BaseRatelimiter

if t.TYPE_CHECKING:
    from .client import GatewayClient

__all__ = ("Ratelimiter",)

_log = logging.getLogger(__name__)


class Ratelimiter(BaseRatelimiter):
    """Represents a ratelimiter for a Gateway Client."""

    __slots__ = (
        "commands_used",
        "parent",
        "_task",
        "_lock",
        "limit",
        "reset_after",
    )

    def __init__(self, parent: GatewayClient, limit: int = 120, reset_after: float = 60.0) -> None:
        super().__init__()

        self.commands_used: int = 0
        self.limit: int = limit
        self.reset_after: float = reset_after
        self.parent: GatewayClient = parent
        self._task: t.Optional[asyncio.Task[t.Any]] = None

    async def ratelimit_loop(self) -> None:
        """Updates the amount of commands used per minute."""
        while not self.parent.is_closed:
            try:
                self._lock.clear()

                await asyncio.sleep(self.reset_after)

                self._lock.set()
                self.commands_used = 0
            except asyncio.CancelledError:
                break

    def start(self) -> None:
        """Starts the ratelimiter task which updates the commands used per minute."""
        if not self._task:
            self._task = asyncio.create_task(self.ratelimit_loop())
            _log.info("Started Gateway ratelimiting task.")

    async def stop(self) -> None:
        """Stops the ratelimiter task."""
        if self._task:
            self._task.cancel()
            await self._task
            _log.info("Stopped Gateway ratelimiting task.")

    def add_command_usage(self) -> None:
        self.commands_used += 1
        _log.debug("A Gateway command has been used.")

    def is_ratelimited(self) -> bool:
        return self.commands_used == self.limit - 1

    async def acquire(self) -> None:
        """Waits for the lock to be unlocked."""
        if not self.is_ratelimited():
            return

        return await super().acquire()
