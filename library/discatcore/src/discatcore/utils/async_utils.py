# SPDX-License-Identifier: MIT

import asyncio
import typing as t

from typing_extensions import ParamSpec

__all__ = (
    "maybecoro",
    "completed_future",
)

T = t.TypeVar("T")
P = ParamSpec("P")

Coro = t.Coroutine[t.Any, t.Any, T]
MaybeCoro = t.Union[Coro[T], T]


async def maybecoro(func: t.Callable[P, MaybeCoro[T]], *args: P.args, **kwargs: P.kwargs) -> T:
    ret = func(*args, **kwargs)

    if asyncio.iscoroutine(ret):
        return await ret
    else:
        # pyright doesn't seem to narrow down the type correctly
        # it thinks it can still be MaybeCoro at this point
        if t.TYPE_CHECKING:
            ret = t.cast(T, ret)

        return ret


def completed_future() -> asyncio.Future[None]:
    future = asyncio.get_running_loop().create_future()
    future.set_result(None)
    return future
