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
import traceback
from typing import Any, Callable, Coroutine, Dict, Optional

from ..utils import MultipleValuesDict

__all__ = ("Dispatcher",)

CoroFunc = Callable[..., Coroutine[Any, Any, Any]]


def _find_value_in_multidict(d: MultipleValuesDict[str, Any], k: str, v: Any):
    values = d.get(k)

    if isinstance(values, list):
        for i, value in enumerate(values):
            if value is v:
                return i

    return -1


class Dispatcher:
    """A class that helps manage events and listeners.

    Attributes
    ----------
    events: :type:`Dict[str, CoroFunc]`
        The events for this dispatcher.
    listener: :type:`MultipleValuesDict[str, CoroFunc]`
        The listeners for this dispatcher.
    """

    def __init__(self):
        self.events: Dict[str, CoroFunc] = {}
        self.listeners: MultipleValuesDict[str, CoroFunc] = MultipleValuesDict()

        async def on_error(exception: Exception):
            traceback.print_exception(
                type(exception), exception, exception.__traceback__
            )

        self.set_event(on_error)

    async def run(self, coro: CoroFunc, *args: Any, **kwargs: Any):
        """Runs the given coroutine. Do not run this yourself, :meth:`.dispatch` takes care of that.

        If the coroutine returns anything, then the coroutine result is ignored..

        Parameters
        ----------
        coro: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The coroutine to run.
        *args: :type:`Any`
            Arguments to pass into the coroutine.
        **kwargs: :type:`Any`
            Keyword arguments to pass into the coroutine.
        """
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    async def dispatch(self, name: str, *args: Any, **kwargs: Any):
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
        event_func = self.events.get(name)
        listeners = self.listeners.get(name)

        if event_func:
            await self.run(event_func, *args, **kwargs)

        if listeners:
            if isinstance(listeners, list):
                for listener in listeners:
                    await self.run(listener, *args, **kwargs)

                    if listener.__one_shot__:
                        self.remove_listener(
                            name, _find_value_in_multidict(listeners, name, listener)
                        )
            else:
                await self.run(listeners, *args, **kwargs)

                if listeners.__one_shot__:
                    self.remove_listener(name, -1)

    def set_event(self, func: CoroFunc, name: Optional[str] = None):
        """Sets an event to a callback.

        Parameters
        ----------
        func: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The callback for this event.
        name: :type:`Optional[str]` = `None`
            The name of this event. If not set, then it uses the name of
            the function.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Function provided is not a coroutine.")

        event_name = func.__name__ if not name else name
        self.events[event_name] = func

    def remove_event(self, name: str):
        """Removes an event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove.
        """
        del self.events[name]

    def has_event(self, name: str):
        """
        Check if this dispatcher already has a event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to find.

        Returns
        -------
        :type:`bool`
            A bool correlating to if there is a event callback with that
            name or not.
        """
        return name in self.events

    def add_listener(
        self, func: CoroFunc, name: Optional[str] = None, one_shot: bool = False
    ):
        """Adds a new listener to an event.

        Parameters
        ----------
        func: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The callback for this listener.
        name: :type:`Optional[str]` = `None`
            The name of the event to listen to. If not set, then it uses the name
            of the function.
        one_shot: :type:`bool` = `False`
            If this listener should be deleted or not.
        """
        event_name = func.__name__ if not name else name

        if event_name in self.events:
            events_sig = inspect.signature(self.events[event_name])
            listener_sig = inspect.signature(self.listeners[event_name])

            if events_sig.parameters != listener_sig.parameters:
                raise TypeError(
                    "Overloaded function does not have the same parameters as original function."
                )

            setattr(func, "__one_shot__", one_shot)
            self.listeners[event_name] = func

    def remove_listener(self, name: str, index: int):
        """Removes a listener for an event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove the overloaded event callback.
        index: :type:`int`
            The index of the overloaded event callback to remove.
        """
        if isinstance(self.listeners.get(name), list):
            del self.listeners[name][index]
        elif name in self.listeners:
            del self.listeners[name]
