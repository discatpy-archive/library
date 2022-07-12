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
import traceback
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Optional, overload

from .utils import MultipleValuesDict

_log = logging.getLogger(__name__)

__all__ = ("Dispatcher",)

CoroFunc = Callable[..., Coroutine[Any, Any, Any]]


def _find_value_in_multidict(d: MultipleValuesDict[Any, Any], k: Any, v: Any):
    values = d.get(k)

    if isinstance(values, list):
        for i, value in enumerate(values):
            if value is v:
                return i

    return -1


@dataclass
class _EventCallbackMetadata:
    one_shot: bool = False
    parent: Optional[Any] = None


class Dispatcher:
    """A class that helps manage events.

    Attributes
    ----------
    events: :type:`MultipleValuesDict[str, CoroFunc]`
        The event and its callbacks for this Dispatcher.
    """

    def __init__(self):
        self.events: MultipleValuesDict[str, CoroFunc] = MultipleValuesDict()

    async def error_handler(self, exception: Exception):
        """Basic error handler for dispatched events.

        Parameters
        ----------
        exception: :type:`Exception`
            The exception from the dispatched event.
        """
        traceback.print_exception(type(exception), exception, exception.__traceback__)

    async def run(self, coro: CoroFunc, parent: Optional[Any], *args: Any, **kwargs: Any):
        """Runs the given coroutine. Do not run this yourself, :meth:`.dispatch` takes care of that.

        If the coroutine returns anything, then the coroutine result is ignored.

        Parameters
        ----------
        coro: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The coroutine to run.
        parent: :type:`Optional[Any]`
            The parent for this coroutine.
        *args: :type:`Any`
            Arguments to pass into the coroutine.
        **kwargs: :type:`Any`
            Keyword arguments to pass into the coroutine.
        """
        try:
            if parent:
                await coro(parent, *args, **kwargs)
            else:
                await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            try:
                await self.error_handler(e)
            except asyncio.CancelledError:
                pass

    def dispatch(self, name: str, *args: Any, **kwargs: Any):
        """Dispatches a event. This will trigger the all of the event's
        callbacks.

        Parameters
        ----------
        name: :type:`str`
            The name of the event to dispatch.
        *args: :type:`Any`
            Arguments to pass into the event callback.
        **kwargs: :type:`Any`
            Keyword arguments to pass into the event callback.
        """
        _log.debug("Dispatching event %s", name)
        event = self.events.get(name)

        if event is not None:
            if isinstance(event, list):
                for i, callback in enumerate(event):
                    metadat = getattr(callback, "__event_metadata__", _EventCallbackMetadata())
                    asyncio.create_task(
                        self.run(callback, metadat.parent, *args, **kwargs),
                        name=f"DisCatPy Event:{name} Index:{i}",
                    )

                    if metadat.one_shot:
                        self.remove_event(
                            name, _find_value_in_multidict(self.events, name, callback)
                        )
            else:
                metadat = getattr(event, "__event_metadata__", _EventCallbackMetadata())
                asyncio.create_task(
                    self.run(event, metadat.parent, *args, **kwargs), name=f"DisCatPy Event:{name}"
                )

                if metadat.one_shot:
                    self.remove_event(name)

    @overload
    def add_event(self, func: CoroFunc, *, name: Optional[str] = None):
        ...

    @overload
    def add_event(self, func: CoroFunc, *, name: Optional[str] = None, one_shot: bool = False):
        ...

    @overload
    def add_event(
        self,
        func: CoroFunc,
        *,
        name: Optional[str] = None,
        one_shot: bool = False,
        parent: Optional[Any] = None,
    ):
        ...

    def add_event(
        self,
        func: CoroFunc,
        *,
        name: Optional[str] = None,
        one_shot: bool = False,
        parent: Optional[Any] = None,
    ):
        """Adds a new event or new event callback to this dispatcher.

        Parameters
        ----------
        func: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The callback for this event.
        name: :type:`Optional[str]` = `None`
            The name of this event. If not set, then it uses the name of
            the callback.
        one_shot: :type:`bool` = `False`
            Whether or not this callback should be deleted after running.
        parent: :type:`Optional[Any]` = `None`
            The parent of this callback, if any.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback provided is not a coroutine.")

        event_name = func.__name__ if not name else name

        if event_name in self.events:
            orig_event_callback = self.events.get_one(event_name, 0)
            orig_callback_metadata = getattr(
                orig_event_callback, "__event_metadata__", _EventCallbackMetadata()
            )

            orig_callback_sig = inspect.signature(orig_event_callback)
            # pop parent parameter (if it exists)
            if orig_callback_metadata.parent is not None:
                new_params = list(OrderedDict(orig_callback_sig.parameters).values())
                new_params.pop(0)
                orig_callback_sig = orig_callback_sig.replace(parameters=new_params)

            new_callback_sig = inspect.signature(func)
            # pop parent parameter (if it exists)
            if parent is not None:
                new_params = list(OrderedDict(new_callback_sig.parameters).values())
                new_params.pop(0)
                new_callback_sig = new_callback_sig.replace(parameters=new_params)

            if orig_callback_sig.parameters != new_callback_sig.parameters:
                raise TypeError(
                    "Overloaded function does not have the same parameters as original function."
                )

        metadat = _EventCallbackMetadata(one_shot, parent)
        setattr(func, "__event_metadata__", metadat)
        self.events[event_name] = func

        _log.debug("Registered new event callback under event %s", event_name)

    @overload
    def remove_event(self, name: str):
        ...

    @overload
    def remove_event(self, name: str, index: Optional[int] = None):
        ...

    def remove_event(self, name: str, index: Optional[int] = None):
        """Removes an event callback or the entire event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove.
        """
        if index is not None and isinstance(self.events[name], list):
            del self.events[name][index]
            _log.debug("Removed event callback under event %s", name)
        else:
            del self.events[name]
            _log.debug("Removed event %s", name)

    def has_event(self, name: str):
        """Check if this dispatcher already has a event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event to find.

        Returns
        -------
        :type:`bool`
            A bool correlating to if there is a event with that
            name or not.
        """
        return name in self.events

    def override_error_handler(self, func: CoroFunc):
        """Overrides a new error handler for dispatched events.

        Parameters
        ----------
        func: :type:`CoroFunc`
            The new error handler.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback provided is not a coroutine.")

        orig_handler_sig = inspect.signature(self.error_handler)
        new_handler_sig = inspect.signature(func)

        if orig_handler_sig.parameters != new_handler_sig.parameters:
            raise TypeError(
                "Overloaded error handler does not have the same parameters as original error handler."
            )

        setattr(self, "error_handler", func)
        _log.debug("Registered new error handler")
