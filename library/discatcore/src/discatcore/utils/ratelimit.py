# SPDX-License-Identifier: MIT

import asyncio
import logging
import typing as t

__all__ = (
    "BaseRatelimiter",
    "ManualRatelimiter",
    "BurstRatelimiter",
)

_log = logging.getLogger(__name__)


class BaseRatelimiter:
    """The base class for all ratelimiters. Locking algorithms are up to the subclassed Ratelimiter."""

    __slots__ = ("_lock",)

    def __init__(self) -> None:
        self._lock: asyncio.Event = asyncio.Event()
        self._lock.set()

    async def acquire(self) -> None:
        await self._lock.wait()

    def is_locked(self) -> bool:
        """Returns whether the bucket is locked or not."""
        return not self._lock.is_set()

    async def __aenter__(self) -> None:
        await self.acquire()
        return None

    async def __aexit__(self, *args: t.Any) -> None:
        pass


class ManualRatelimiter(BaseRatelimiter):
    """A simple ratelimiter that simply locks at the command of anything."""

    async def _unlock(self, delay: float) -> None:
        await asyncio.sleep(delay)
        self._lock.set()

    def lock_for(self, delay: float) -> None:
        """Locks the bucket for a given amount of time.

        Args:
            delay (float): How long the bucket should be locked for.
        """
        if self.is_locked():
            return

        self._lock.clear()
        asyncio.create_task(self._unlock(delay))


class BurstRatelimiter(ManualRatelimiter):
    """A ratelimiter that automatically locks when acquired based on its information.

    Attributes:
        limit (t.Optional[int]): The amount of times this ratelimiter can be acquired before being locked.
        remaining (t.Optional[int]): The remaining amount of times this ratelimiter can be acquired before locking.
        reset_after (t.Optional[float]): How long the ratelimiter has to wait before it has been renewed.
    """

    __slots__ = ("limit", "remaining", "reset_after")

    def __init__(self) -> None:
        BaseRatelimiter.__init__(self)

        self.limit: t.Optional[int] = None
        self.remaining: t.Optional[int] = None
        self.reset_after: t.Optional[float] = None

    async def acquire(self) -> None:
        if (
            self.reset_after is not None
            and self.remaining == 0
            and not self.is_locked()
        ):
            _log.info("Auto-locking for %f seconds.", self.reset_after)
            self.lock_for(self.reset_after)

        return await super().acquire()
