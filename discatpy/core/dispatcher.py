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
from typing import Any, Callable, Coroutine, Dict, List, Optional, TypeVar, overload

from .utils import MultipleValuesDict

_log = logging.getLogger(__name__)

__all__ = ("Dispatcher",)

T = TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[Any, Any, Any]]


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
        The callbacks for each event.
    event_protos: :type:`Dict[str, inspect.Signature]`
        The event callback prototypes for each event. This is checked alongside a new
        event callback to see if the parameters match up.
    valid_events: :type:`List[str]`
        The list of the name of valid events.
    """

    __slots__ = (
        "events",
        "event_protos",
        "valid_events",
    )

    def __init__(self):
        self.events: MultipleValuesDict[str, CoroFunc] = MultipleValuesDict()
        self.event_protos: Dict[str, inspect.Signature] = {}
        self.valid_events: List[str] = []

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
        if parent:
            args = (parent, *args)

        try:
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
                    _log.debug("Running event callback under event %s with index %s", name, i)
                    asyncio.create_task(
                        self.run(callback, metadat.parent, *args, **kwargs),
                        name=f"DisCatPy Event:{name} Index:{i}",
                    )

                    if metadat.one_shot:
                        _log.debug("Removing event callback under event %s with index %s", name, i)
                        self.remove_event_callback(
                            name, _find_value_in_multidict(self.events, name, callback)
                        )
            else:
                metadat = getattr(event, "__event_metadata__", _EventCallbackMetadata())
                _log.debug("Running event callback under event %s", name)
                asyncio.create_task(
                    self.run(event, metadat.parent, *args, **kwargs), name=f"DisCatPy Event:{name}"
                )

                if metadat.one_shot:
                    _log.debug("Removing event callback under event %s", name)
                    self.remove_event_callback(name)

    @staticmethod
    def _get_event_name(func: Func, name: Optional[str]):
        return func.__name__ if not name else name

    @overload
    def set_event_proto(self, proto_func: Func[Any], *, name: Optional[str] = None):
        ...

    @overload
    def set_event_proto(
        self, proto_func: Func[Any], *, name: Optional[str] = None, parent: Optional[Any] = None
    ):
        ...

    def set_event_proto(
        self, proto_func: Func[Any], *, name: Optional[str] = None, parent: Optional[Any] = None
    ):
        is_static = isinstance(proto_func, staticmethod)
        if is_static:
            proto_func = proto_func.__func__

        event_name = self._get_event_name(proto_func, name)

        if event_name not in self.event_protos:
            sig = inspect.signature(proto_func)
            if parent is not None and not is_static:
                new_params = list(sig.parameters.values())
                print(new_params)
                new_params.pop(0)
                sig = sig.replace(parameters=new_params)
            self.event_protos[event_name] = sig

            _log.debug("Registered new event proto under event %s", event_name)
        else:
            raise ValueError(f"Event prototype for event {event_name} has already been set!")

    def remove_event_proto(self, name: str):
        del self.event_protos[name]
        _log.debug("Removed event under name %s", name)

    @overload
    def add_event_callback(self, func: CoroFunc, *, name: Optional[str] = None):
        ...

    @overload
    def add_event_callback(
        self, func: CoroFunc, *, name: Optional[str] = None, one_shot: bool = False
    ):
        ...

    @overload
    def add_event_callback(
        self,
        func: CoroFunc,
        *,
        name: Optional[str] = None,
        one_shot: bool = False,
        parent: Optional[Any] = None,
    ):
        ...

    def add_event_callback(
        self,
        func: CoroFunc,
        *,
        name: Optional[str] = None,
        one_shot: bool = False,
        parent: Optional[Any] = None,
    ):
        """Adds a new event callback to an event.

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

        event_name = self._get_event_name(func, name)
        if event_name not in self.event_protos:
            raise ValueError("Event prototype for this event has not been defined.")

        event_proto = self.event_protos[event_name]
        callback_sig = inspect.signature(func)
        if parent is not None:
            new_params = list(callback_sig.parameters.values())
            new_params.pop(0)
            callback_sig = callback_sig.replace(parameters=new_params)

        if len(event_proto.parameters) != len(callback_sig.parameters):
            raise TypeError(
                "Event callback parameters do not match up with the event prototype parameters."
            )

        metadat = _EventCallbackMetadata(one_shot, parent)
        setattr(func, "__event_metadata__", metadat)
        self.events[event_name] = func

        _log.debug("Registered new event callback under event %s", event_name)

    @overload
    def remove_event_callback(self, name: str):
        ...

    @overload
    def remove_event_callback(self, name: str, index: Optional[int] = None):
        ...

    def remove_event_callback(self, name: str, index: Optional[int] = None):
        """Removes an event callback or all event callbacks.

        Parameters
        ----------
        name: :type:`str`
            The name of the event callback to remove. If not set, then this will
            remove all callbacks under an event.
        """
        if index is not None and isinstance(self.events[name], list):
            del self.events[name][index]
            _log.debug("Removed event callback under event %s", name)
        elif isinstance(self.events[name], list):
            del self.events[name]
            _log.debug("Removed all event callbacks under event %s", name)
        else:
            del self.events[name]
            _log.debug("Removed event callback under event %s", name)

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
        return name in self.event_protos

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
