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
from typing import Type

__all__ = (
    "BucketResolutor",
    "Bucket",
    "Ratelimiter",
)

class BucketResolutor:
    """Converts a given client bucket (method + path) into a bucket from Discord.

    This works by having requests pair their client buckets with the bucket from Discord.
    Then when another request with the same client bucket wants its bucket from Discord, it fetches from here.

    Attributes
    ----------
    _bucket_strs: dict[:class:`str`, :class:`str`]
        The internal bucket mapping.    
    """
    __slots__ = ("_bucket_strs",)

    def __init__(self):
        self._bucket_strs: dict[str, str] = {}

    def resolve_bucket(self, bucket: str):
        """Resolves the Discord bucket via the given client bucket.
        
        Parameters
        ----------
        bucket: :class:`str`
            The client bucket to resolve.

        Returns
        -------
        :class:`str`
            The Discord bucket, if found. If not found, then the client bucket is returned.
        """
        return self._bucket_strs.get(bucket, bucket)

    def add_bucket_mapping(self, client_bucket: str, discord_bucket: str):
        """Adds a new client bucket to discord bucket mapping.
        
        Parameters
        ----------
        client_bucket: :class:`str`
            The client bucket to map for.
        discord_bucket: :class:`str`
            The discord bucket to map to the client bucket.
        """
        if client_bucket not in self._bucket_strs:
            self._bucket_strs[client_bucket] = discord_bucket

    def has_bucket_mapping(self, client_bucket: str):
        """Checks whether or not a mapping for a client bucket exists.
        
        Parameters
        ----------
        client_bucket: :class:`str`
            The client bucket to check for.

        Returns
        -------
        :class:`bool`
            Whether or not the client bucket mapping exists.
        """
        return client_bucket in self._bucket_strs

class Bucket:
    """Represents a ratelimiting bucket."""

    __slots__ = ("_lock", "_delayed")

    def __init__(self):
        self._lock = asyncio.Lock()
        self._delayed = False

    async def __aenter__(self) -> "Bucket":
        await self._lock.acquire()
        return self

    async def __aexit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: BaseException) -> None:
        if self._delayed:
            self._lock.release()

    async def _unlock(self, delay: float):
        await asyncio.sleep(delay)

        self._lock.release()
        self._delayed = False

    async def delay_unlock(self, delay: float):
        """Delays unlocking this bucket.
        
        Parameters
        ----------
        delay: :class:`float`
            The delay for when the bucket will be unlocked.
        """
        self._delayed = True
        asyncio.create_task(self._unlock(delay))

class Ratelimiter:
    """Represents the global ratelimiter."""

    __slots__ = ("_resolutor", "_buckets", "_global_lock")

    def __init__(self, resolutor: BucketResolutor):
        self._resolutor = resolutor
        self._buckets: dict[str, Bucket] = {}
        self._global_lock = asyncio.Event()

    async def acquire_bucket(self, bucket_str: str) -> Bucket:
        """Acquires a bucket with the given bucket str. 
        This bucket str will be resolved before acquiring the bucket.
        
        Parameters
        ----------
        bucket_str: :class:`str`
            The string representing the bucket.
        """
        resolved_bucket_str = self._resolutor.resolve_bucket(bucket_str)

        if resolved_bucket_str not in self._buckets:
            self._buckets[resolved_bucket_str] = Bucket()

        return self._buckets[resolved_bucket_str]

    async def _unlock_global(self, after: float):
        await asyncio.sleep(after)
        self._global_lock.clear()

    async def set_global_lock(self, unlock_after: float):
        """Sets the global lock then unsets it after some time.

        Parameters
        ----------
        unlock_after: :class:`float`
            The delay of when to unlock the global lock.

        Raises
        ------
        RuntimeError:
            The global lock is already locked.
        """
        if self._global_lock.is_set():
            raise RuntimeError("Global Lock is already locked.")

        self._global_lock.set()
        asyncio.create_task(self._unlock_global(unlock_after))