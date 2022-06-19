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
from typing import Any, Callable, Coroutine, Dict, Optional

from ..utils import MultipleValuesDict

__all__ = ("Dispatcher",)

CoroFunc = Callable[..., Coroutine[Any, Any, Any]]


class Dispatcher:
    """
    Runs coroutines based on if an event is dispatched.
    """

    def __init__(self):
        self.callbacks: MultipleValuesDict[str, CoroFunc] = MultipleValuesDict()
        self.one_shots: Dict[str, Any] = {}

    async def run(self, coro: CoroFunc, *args: Any, **kwargs: Any):
        """
        Runs the given coroutine. Do not run this yourself, :meth:`dispatch` takes care of that.

        Parameters
        ----------
        coro: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The coroutine to run
        *args: :type:`Any`
            Arguments to pass into the coroutine
        **kwargs: :type:`Any`
            Keyword arguments to pass into the coroutine
        """
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    async def dispatch(self, name: str, *args: Any, **kwargs: Any):
        """
        Dispatches a event. This will trigger the all of the event's
        callbacks.

        Parameters
        ----------
        name: :type:`str`
            The name of the event to dispatch
        *args: :type:`Any`
            Arguments to pass into the event callback
        **kwargs: :type:`Any`
            Keyword arguments to pass into the event callback
        """
        funcs = self.callbacks.get(name)
        one_shot = self.one_shots.get(name)

        if isinstance(funcs, list):
            for f in funcs:
                await self.run(f, *args, **kwargs)
        elif funcs is not None:
            await self.run(funcs, *args, **kwargs)

        # this ensures that the listener gets removed after all of the callbacks are called
        if one_shot and funcs is not None:
            self.remove_event_callback(name)

    def add_event_callback(
        self, func: CoroFunc, name: Optional[str] = None, one_shot: bool = False
    ):
        """
        Adds a new callback for an event.

        Parameters
        ----------
        func: :type:`Callable[..., Coroutine[Any, Any, Any]]`
            The function for this callback.
        name: :type:`Optional[str]`
            The name of this event. If not set, then it uses the name of
            the function.
        one_shot: :type:`bool`
            If this event should be deleted or not. Set to False
            by default.
        """
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Function provided is not a coroutine.")

        event_name = func.__name__ if not name else name
        self.one_shots[event_name] = one_shot

        if event_name in self.callbacks:
            original_callback = self.callbacks.get(event_name)

            if isinstance(original_callback, list):
                original_callback = original_callback[0]

            original_callback_sig = inspect.signature(original_callback)
            overloaded_callback_sig = inspect.signature(func)

            if original_callback_sig.parameters != overloaded_callback_sig.parameters:
                raise TypeError(
                    "Overloaded function does not have the same parameters as original function."
                )

        self.callbacks[event_name] = func

    def remove_event_callback(self, name: str):
        """
        Removes a event callback for an event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove
        """
        del self.callbacks[name]

    def remove_event_callback_overload(self, name: str, index: int):
        """
        Removes an overloaded event callback for an event callback.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove the overloaded event callback
        index: :type:`int`
            The index of the overloaded event callback to remove
        """
        if not self.has_event_callback(name):
            raise Exception(f"There is no original callback with the name {name}.")

        del self.callbacks[name][index]

    def has_event_callback(self, name: str):
        """
        Check if this dispatcher already has a event callback.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to find

        Returns
        -------
            A bool correlating to if there is a event callback with that
            name or not.
        """
        return name in self.callbacks
