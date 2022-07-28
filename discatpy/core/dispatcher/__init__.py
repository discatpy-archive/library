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
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Optional, TypeVar, overload

from .event import Event

if TYPE_CHECKING:
    from ..client import Client

_log = logging.getLogger(__name__)

__all__ = ("Dispatcher",)

T = TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[Any, Any, Any]]


class Dispatcher:
    """A class that helps manage events.

    Attributes
    ----------
    events: :type:`MultipleValuesDict[str, CoroFunc]`
        The callbacks for each event.
    event_protos: :type:`Dict[str, inspect.Signature]`
        The event callback prototypes for each event. This is checked alongside a new
        event callback to see if the parameters match up.
    valid_events: :type:`List[str]`
        The list of the name of valid events.
    """

    __slots__ = (
        "client",
        "events",
        "event_protos",
        "valid_events",
    )

    def __init__(self, client: "Client") -> None:
        self.client = client
        self.events: Dict[str, Event] = {}

    def get_event(self, name: str) -> Optional[Event]:
        """Returns an event with the name provided.

        Parameters
        ----------
        name: :class:`str`
            The name of the event that will be grabbed.

        Return
        ------
        Optional[:class:`Event`]
            The event, none if not found.
        """
        return self.events.get(name)

    def add_event(self, name: str) -> Event:
        """Adds a new event. Returns this new event after creation.

        Parameters
        ----------
        name: :class:`str`
            The name of the new event.

        Return
        ------
        :class:`Event`
            The new event created.
        """
        new_event = Event(name, self)
        self.events[name] = new_event
        return new_event

    def remove_event(self, name: str) -> None:
        """Removes an event.

        Parameters
        ----------
        name: :class:`str`
            The name of the event to remove.
        """
        if name not in self.events:
            raise ValueError(f"There is no event with name {name}!")

        del self.events[name]
        _log.debug("Removed event with name %s", name)

    def has_event(self, name: str) -> bool:
        """Check if this dispatcher already has a event.

        Parameters
        ----------
        name: :type:`str`
            The name of the event to find.

        Returns
        -------
        :type:`bool`
            A bool correlating to if there is a event with that name or not.
        """
        return name in self.events

    def event(
        self,
        *,
        proto: bool = False,
        callback: bool = False,
        name: Optional[str] = None,
        parent: bool = False,
        one_shot: bool = False,
    ) -> Func[Event]:
        if not proto and not callback:
            raise ValueError("Proto and callback parameters cannot both be None!")

        def wrapper(func: CoroFunc):
            event_name = func.__name__ if not name else name
            new_event = self.add_event(event_name)

            if proto:
                new_event.set_proto(func, parent=parent)
            if callback:
                new_event.add_callback(func, one_shot=one_shot, parent=parent)

            return new_event

        return wrapper

    # global error handler

    async def error_handler(self, exception: Exception) -> None:
        """Basic error handler for dispatched events.

        Parameters
        ----------
        exception: :type:`Exception`
            The exception from the dispatched event.
        """
        traceback.print_exception(type(exception), exception, exception.__traceback__)

    def override_error_handler(self, func: CoroFunc) -> None:
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

    # dispatch

    def dispatch(self, name: str, *args: Any, **kwargs: Any) -> None:
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
            event.dispatch(*args, **kwargs)
