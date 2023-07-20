# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import inspect
import logging
import typing as t
from collections.abc import Callable, Coroutine
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from .dispatcher import Dispatcher

_log = logging.getLogger(__name__)

__all__ = ("Event",)

T = t.TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[t.Any, t.Any, t.Any]]


@dataclass
class _EventCallbackMetadata:
    one_shot: bool = False
    parent: bool = False


class Event:
    """Represents an event for a dispatcher.

    Args:
        name (str): The name of this event.
        parent (Dispatcher): The parent dispatcher of this event.

    Attributes:
        name (str): The name of this event.
        parent (Dispatcher): The parent dispatcher of this event.
        callbacks (list[Callable[..., Coroutine[t.Any, t.Any, t.Any]]]): The callbacks for this event.
        metadata (dict[Callable[..., Coroutine[t.Any, t.Any, t.Any]], _EventCallbackMetadata]): The metadata for the callbacks for this event.
        _proto (t.Optional[inspect.Signature]): The prototype of this event.
            This will define what signature all of the callbacks will have.
        _error_handler (Callable[..., Coroutine[t.Any, t.Any, t.Any]]): The error handler of this event.
            The error handler will be run whenever an event dispatched raises an error.
            Defaults to the error handler from the parent dispatcher.
    """

    def __init__(self, name: str, parent: Dispatcher) -> None:
        self.name: str = name
        self.parent: Dispatcher = parent
        self.callbacks: list[CoroFunc] = []
        self.metadata: dict[CoroFunc, _EventCallbackMetadata] = {}
        self._proto: t.Optional[inspect.Signature] = None
        self._error_handler: CoroFunc = self.parent.error_handler

    # setters/decorators

    def set_proto(
        self,
        proto_func: t.Union[Func[t.Any], staticmethod[..., t.Any]],
        *,
        force_parent: bool = False,
    ) -> None:
        """Sets the prototype for this event.

        Args:
            proto_func (Callable[..., t.Any]): The prototype for this event.
            force_parent (bool): Whether or not this callback contains a self parameter. Defaults to ``False``.
        """
        is_static = isinstance(proto_func, staticmethod)
        if is_static:
            proto_func = proto_func.__func__

        if not self._proto:
            sig = inspect.signature(proto_func)
            if force_parent and not is_static:
                new_params = list(sig.parameters.values())
                new_params.pop(0)
                sig = sig.replace(parameters=new_params)
            self._proto = sig

            _log.debug("Registered new event prototype under event %s", self.name)
        else:
            raise ValueError(f"Event prototype for event {self.name} has already been set!")

    @t.overload
    def proto(self, func: CoroFunc, *, force_parent: bool = ...) -> Event:
        pass

    @t.overload
    def proto(
        self, func: None = ..., *, force_parent: bool = ...
    ) -> Callable[[Func[t.Any]], Event]:
        pass

    def proto(
        self,
        func: t.Optional[t.Union[Func[t.Any], staticmethod[..., t.Any]]] = None,
        *,
        force_parent: bool = False,
    ) -> t.Union[Event, Callable[[Func[t.Any]], Event]]:
        """A decorator to set the prototype of this event.

        Args:
            func (t.Optional[Callable[..., t.Any]]): The prototype to pass into this decorator. Defaults to ``None``.
            force_parent (bool): Whether or not this callback contains a self parameter. Defaults to ``False``.

        Returns:
            Either this event object or a wrapper function that acts as the actual decorator.
            This depends on if the ``func`` arg was passed in.
        """

        def wrapper(func: t.Union[Func[t.Any], staticmethod[..., t.Any]]):
            self.set_proto(func, force_parent=force_parent)
            return self

        if func:
            return wrapper(func)
        return wrapper

    def set_error_handler(self, func: CoroFunc) -> None:
        """Overrides the error handler of this event.

        Args:
            func (Callable[..., Coroutine[t.Any, t.Any, t.Any]]): The new error handler for this event.
        """
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

    def error_handler(self) -> Callable[[Func[t.Any]], Event]:
        """A decorator to override the error handler of this event.

        Returns:
            A wrapper function that acts as the actual decorator.
        """

        def wrapper(func: CoroFunc):
            self.set_error_handler(func)
            return self

        return wrapper

    def add_callback(
        self, func: CoroFunc, *, one_shot: bool = False, force_parent: bool = False
    ) -> None:
        """Adds a new callback to this event.

        Args:
            func (Callable[..., Coroutine[t.Any, t.Any, t.Any]]): The callback to add to this event.
            one_shot (bool): Whether or not the callback should be a one shot (which means the callback will be removed after running). Defaults to False.
            force_parent (bool): Whether or not this callback contains a self parameter. Defaults to False.
        """
        if not self._proto:
            self.set_proto(func, force_parent=force_parent)
            # this is to prevent static type checkers from inferring that self._proto is
            # still None after setting it indirectly via a different function
            # (it should never go here tho because exceptions stop the flow of this code
            # and it should be set if we don't reach t.Any exceptions)
            if not self._proto:
                return

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Callback provided is not a coroutine.")

        callback_sig = inspect.signature(func)
        if force_parent:
            new_params = list(callback_sig.parameters.values())
            new_params.pop(0)
            callback_sig = callback_sig.replace(parameters=new_params)

        if len(self._proto.parameters) != len(callback_sig.parameters):
            raise TypeError(
                "Event callback parameters do not match up with the event prototype parameters."
            )

        metadat = _EventCallbackMetadata(one_shot)
        self.metadata[func] = metadat
        self.callbacks.append(func)

        _log.debug("Registered new event callback under event %s", self.name)

    def remove_callback(self, index: int) -> None:
        """Removes a callback located at a certain index.

        Args:
            index (int): The index where the callback is located.
        """
        if len(self.callbacks) - 1 < index:
            raise ValueError(f"Event {self.name} has less callbacks than the index provided!")

        del self.callbacks[index]
        _log.debug("Removed event callback with index %d under event %s", index, self.name)

    @t.overload
    def callback(self, func: CoroFunc, *, one_shot: bool = ..., force_parent: bool = ...) -> Event:
        pass

    @t.overload
    def callback(
        self, func: None = ..., *, one_shot: bool = ..., force_parent: bool = ...
    ) -> Callable[[Func[t.Any]], Event]:
        pass

    def callback(
        self,
        func: t.Optional[CoroFunc] = None,
        *,
        one_shot: bool = False,
        force_parent: bool = False,
    ) -> t.Union[Event, Callable[[Func[t.Any]], Event]]:
        """A decorator to add a callback to this event.

        Args:
            func (t.Optional[Callable[..., Coroutine[t.Any, t.Any, t.Any]]]): The function to pass into this decorator. Defaults to None.
            one_shot (bool): Whether or not the callback should be a one shot (which means the callback will be removed after running). Defaults to False.
            force_parent (bool): Whether or not this callback contains a self parameter. Defaults to False.

        Returns:
            Either this event object or a wrapper function that acts as the actual decorator.
            This depends on if the ``func`` arg was passed in.
        """

        def wrapper(func: CoroFunc):
            self.add_callback(func, one_shot=one_shot, force_parent=force_parent)
            return self

        if func:
            return wrapper(func)
        return wrapper

    # dispatch

    async def _run(self, coro: CoroFunc, *args: t.Any, **kwargs: t.Any) -> None:
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
        index: t.Optional[int],
        *args: t.Any,
        **kwargs: t.Any,
    ) -> asyncio.Task[t.Any]:
        task_name = f"DisCatCore Event:{self.name}"
        if index:
            task_name += f" Index:{index}"
        task_name = task_name.rstrip()

        wrapped = self._run(coro, *args, **kwargs)
        return asyncio.create_task(wrapped, name=task_name)

    def dispatch(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Runs all event callbacks with arguments.

        Args:
            *args (t.Any): Arguments to pass into the event callbacks.
            **kwargs (t.Any): Keyword arguments to pass into the event callbacks.
        """
        for i, callback in enumerate(self.callbacks):
            metadata = self.metadata.get(callback, _EventCallbackMetadata())
            _log.debug("Running event callback under event %s with index %s", self.name, i)

            self._schedule_task(callback, i, *args, **kwargs)

            if metadata.one_shot:
                _log.debug("Removing event callback under event %s with index %s", self.name, i)
                self.remove_callback(i)
