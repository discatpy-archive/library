# SPDX-License-Identifier: MIT

import typing as t
from datetime import datetime, timezone

from aiohttp import ClientResponse

from ..utils.ratelimit import BurstRatelimiter, ManualRatelimiter

__all__ = (
    "Bucket",
    "Ratelimiter",
)


class Bucket(BurstRatelimiter):
    """Represents a bucket in the Discord API.

    Attributes:
        reset (t.Optional[datetime.datetime]): The raw timestamp (processed into a datetime) when the bucket will reset.
            Defaults to None.
        bucket (t.Optional[str]): The hash denoting this bucket. This value is straight from the Discord API.
            Defaults to None.
    """

    __slots__ = (
        "reset",
        "bucket",
        "_first_update",
    )

    def __init__(self) -> None:
        BurstRatelimiter.__init__(self)

        self.reset: t.Optional[datetime] = None
        self.bucket: t.Optional[str] = None
        self._first_update: bool = True

    def update_info(self, response: ClientResponse) -> None:
        """Updates the bucket's underlying information via the new headers.

        Args:
            response (aiohttp.ClientResponse): The response to update the bucket information with.
        """
        self.limit = int(response.headers.get("X-RateLimit-Limit", 1))
        raw_remaining = response.headers.get("X-RateLimit-Remaining")

        if response.status == 429:
            self.remaining = 0
        elif raw_remaining is None:
            self.remaining = 1
        else:
            converted_remaining = int(raw_remaining)

            if self._first_update:
                self.remaining = converted_remaining
            elif self.remaining is not None:
                self.remaining = (
                    converted_remaining if converted_remaining < self.remaining else self.remaining
                )

        raw_reset = response.headers.get("X-RateLimit-Reset")
        if raw_reset is not None:
            self.reset = datetime.fromtimestamp(float(raw_reset), timezone.utc)

        raw_reset_after = response.headers.get("X-RateLimit-Reset-After")
        if raw_reset_after is not None:
            raw_reset_after = float(raw_reset_after)

            if self.reset_after is None:
                self.reset_after = raw_reset_after
            else:
                self.reset_after = (
                    raw_reset_after if self.reset_after < raw_reset_after else self.reset_after
                )

        raw_bucket = response.headers.get("X-RateLimit-Bucket")
        self.bucket = raw_bucket

        if self._first_update:
            self._first_update = False


class Ratelimiter:
    """Represents the global ratelimiter.

    Attributes:
        buckets: A mapping of route urls and bucket hashes to buckets.
        global_bucket: The global bucket. Used for requests that involve global 429s.
    """

    __slots__ = ("buckets", "global_bucket")

    def __init__(self) -> None:
        self.buckets: dict[tuple[str, t.Optional[str]], Bucket] = {}
        self.global_bucket = ManualRatelimiter()

    def get_bucket(self, key: tuple[str, t.Optional[str]]) -> Bucket:
        """Gets a bucket object with the provided key.

        Args:
            key: The key to grab the bucket with. This key is in the format (route_url, bucket_hash).
        """
        if key not in self.buckets:
            new_bucket = Bucket()
            self.buckets[key] = new_bucket
            new_bucket.bucket = key[1]

        return self.buckets[key]
