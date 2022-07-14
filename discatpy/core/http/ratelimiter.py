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
import logging
from typing import List

from .route import Route

_log = logging.getLogger(__name__)

__all__ = (
    "Bucket",
    "Ratelimiter",
)


class Bucket:
    """Represents a ratelimiting bucket."""

    __slots__ = ("route", "_lock")

    def __init__(self, route: Route):
        self.route = route
        self._lock = asyncio.Event()
        self._lock.set()

    async def wait(self):
        """Waits for the bucket to be available."""
        await self._lock.wait()

    async def _unlock(self, delay: float):
        await asyncio.sleep(delay)
        self._lock.set()
        _log.debug("Ratelimit bucket with parameters %s has been unlocked.", self.route.bucket)

    def lock_for(self, delay: float):
        self._lock.clear()
        _log.debug(
            "Ratelimit bucket with parameters %s has been locked. This will be unlocked after %f seconds.",
            self.route.bucket,
            delay,
        )
        asyncio.create_task(self._unlock(delay))

    def is_locked(self):
        return not self._lock.is_set()


class Ratelimiter:
    """Represents the global ratelimiter."""

    __slots__ = ("_buckets", "global_bucket")

    def __init__(self):
        self._buckets: List[Bucket] = []
        self.global_bucket = Bucket(Route("/"))

    async def acquire_buckets(self, route: Route):
        """Acquires (a) bucket(s) with the given route.
        This will automatically wait for each bucket that matches the provided route.

        Parameters
        ----------
        route: :class:`Route`
            The route representing the bucket(s).
        """
        for bucket in self._buckets:
            if (
                bucket.route.channel_id == route.channel_id
                or bucket.route.guild_id == route.guild_id
                or bucket.route.webhook_id == route.webhook_id
                or bucket.route.webhook_token == route.webhook_token
                or bucket.route.endpoint == route.endpoint
            ):
                await bucket.wait()
                break

    async def create_temporary_bucket_for(self, route: Route, delay: float):
        new_bucket = Bucket(route)
        self._buckets.append(new_bucket)

        new_bucket.lock_for(delay)
        await new_bucket.wait()

        for i, bucket in enumerate(self._buckets):
            if bucket == new_bucket:
                del self._buckets[i]
