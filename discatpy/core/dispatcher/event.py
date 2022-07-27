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
import inspect
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Coroutine, List, Optional, TypeVar

if TYPE_CHECKING:
    from . import Dispatcher

_log = logging.getLogger(__name__)

__all__ = ("Event",)

T = TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[Any, Any, Any]]


@dataclass
class _EventCallbackMetadata:
    one_shot: bool = False
    parent: bool = False


class Event:
    def __init__(self, name: str, parent: Dispatcher):
        self.name = name
        self.parent = parent
        self.callbacks: List[CoroFunc] = []
        self._proto: Optional[inspect.Signature] = None
        self._error_handler: CoroFunc = self.parent.error_handler

    # setters/decorators

    def set_proto(self, proto_func: Func[Any], *, parent: bool = False):
        is_static = isinstance(proto_func, staticmethod)
        if is_static:
            proto_func = proto_func.__func__

        if not self._proto:
            sig = inspect.signature(proto_func)
            if parent and not is_static:
                new_params = list(sig.parameters.values())
                new_params.pop(0)
                sig = sig.replace(parameters=new_params)
            self._proto = sig

            _log.debug("Registered new event prototype under event %s", self.name)
        else:
            raise ValueError(f"Event prototype for event {self.name} has already been set!")

    def proto(self, func: Optional[Func[Any]] = None, *, parent: bool = False):
        def wrapper(func: Func[Any]):
            self.set_proto(func, parent=parent)
            return self

        if func:
            return wrapper(func)
        return wrapper

    def set_error_handler(self, func: CoroFunc):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback provided is not a coroutine.")

        orig_handler_sig = inspect.signature(self._error_handler)
        new_handler_sig = inspect.signature(func)

        if len(orig_handler_sig.parameters) != len(new_handler_sig.parameters):
            raise TypeError(
                "Overloaded error handler does not have the same parameters as original error handler."
            )

        self._error_handler = func
        _log.debug("Registered new error handler under event %s", self.name)

    def error_handler(self):
        def wrapper(func: CoroFunc):
            self.set_error_handler(func)
            return self

        return wrapper

    def add_callback(self, func: CoroFunc, *, one_shot: bool = False, parent: bool = False):
        if not self._proto:
            raise ValueError(f"Event prototype for event {self.name} has not been defined.")

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback provided is not a coroutine.")

        callback_sig = inspect.signature(func)
        if parent:
            new_params = list(callback_sig.parameters.values())
            new_params.pop(0)
            callback_sig = callback_sig.replace(parameters=new_params)

        if len(self._proto.parameters) != len(callback_sig.parameters):
            raise TypeError(
                "Event callback parameters do not match up with the event prototype parameters."
            )

        metadat = _EventCallbackMetadata(one_shot)
        setattr(func, "__callback_metadata__", metadat)
        self.callbacks.append(func)

        _log.debug("Registered new event callback under event %s", self.name)

    def remove_callback(self, index: int):
        if len(self.callbacks) - 1 < index:
            raise ValueError(f"Event {self.name} has less callbacks than the index provided!")

        del self.callbacks[index]
        _log.debug("Removed event callback with index %d under event %s", index, self.name)

    def callback(
        self, func: Optional[CoroFunc] = None, *, one_shot: bool = False, parent: bool = False
    ):
        def wrapper(func: CoroFunc):
            self.add_callback(func, one_shot=one_shot, parent=parent)
            return self

        if func:
            return wrapper(func)
        return wrapper

    # dispatch

    async def _run(self, coro: CoroFunc, *args: Any, **kwargs: Any):
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            try:
                await self._error_handler(e)
            except asyncio.CancelledError:
                pass

    def _schedule_task(
        self,
        coro: CoroFunc,
        index: Optional[int],
        *args: Any,
        **kwargs: Any,
    ):
        task_name = f"DisCatPy Event:{self.name} "
        if index:
            task_name += f"Index:{index}"
        task_name = task_name.rstrip()

        wrapped = self._run(coro, *args, **kwargs)
        return asyncio.create_task(wrapped, name=task_name)

    def dispatch(self, *args: Any, **kwargs: Any):
        for i, callback in enumerate(self.callbacks):
            metadata = getattr(callback, "__callback_metadata__", _EventCallbackMetadata())
            _log.debug("Running event callback under event %s with index %s", self.name, i)

            self._schedule_task(callback, i, *args, **kwargs)

            if metadata.one_shot:
                _log.debug("Removing event callback under event %s with index %s", self.name, i)
                self.remove_callback(i)
