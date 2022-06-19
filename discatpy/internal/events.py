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

from typing import List

from .dispatcher import *

__all__ = ("EventsMixin",)


class EventsMixin:
    """
    This mixin adds Discord Gateway events functionality like listening to an event
    or all the avaliable event types out there.

    This is for internal use only.
    """

    dispatcher: Dispatcher

    valid_events: List[str] = [
        "on_ready",
        "on_resumed",
        "on_reconnect",
        "on_channel_create",
        "on_channel_update",
        "on_channel_delete",
        "on_channel_pins_update",
        "on_thread_create",
        "on_thread_update",
        "on_thread_delete",
        "on_thread_list_sync",
        "on_thread_member_update",
        "on_thread_members_update",
        "on_guild_create",
        "on_guild_update",
        "on_guild_delete",
        "on_guild_ban_add",
        "on_guild_ban_remove",
        "on_guild_emojis_update",
        "on_guild_stickers_update",
        "on_guild_intergrations_update",
        "on_guild_member_add",
        "on_guild_member_remove",
        "on_guild_member_update",
        "on_guild_members_chunk",
        "on_guild_role_create",
        "on_guild_role_update",
        "on_guild_role_delete",
        "on_guild_scheduled_event_create",
        "on_guild_scheduled_event_update",
        "on_guild_scheduled_event_delete",
        "on_guild_scheduled_event_user_add",
        "on_guild_scheduled_event_user_remove",
        "on_integration_create",
        "on_integration_update",
        "on_integration_delete",
        "on_interaction_create",
        "on_invite_create",
        "on_invite_delete",
        "on_message_create",
        "on_message_update",
        "on_message_delete",
        "on_message_delete_bulk",
        "on_message_reaction_add",
        "on_message_reaction_remove",
        "on_message_reaction_remove_all",
        "on_message_reaction_remove_emoji",
        "on_presence_update",
        "on_stage_instance_create",
        "on_stage_instance_delete",
        "on_stage_instance_update",
        "on_typing_start",
        "on_user_update",
        "on_voice_state_update",
        "on_voice_server_update",
        "on_webhooks_update",
    ]

    def listen(self, event: str):
        """
        Registers a callback for an event. This will automatically check if the event name
        provided is a valid event or the function name if they are the same value.

        This function is a decorator.

        Parameters
        ----------
        event: :type:`str`
            The event to listen for
        """

        def wrapper(func):
            name = func.__name__
            if event != name:
                name = event

            if name not in self.valid_events:
                raise ValueError("Event name provided is not a valid event!")

            self.dispatcher.add_event_callback(func, name=name)
            return func

        return wrapper

    def event(self, func):
        """
        Similar to `EventsMixin.listen()` except that it checks if the function name is
        a valid event.

        This function is a decorator.
        """
        if func.__name__ not in self.valid_events:
            raise ValueError("Event name provided is not a valid event!")

        self.dispatcher.add_event_callback(func)
        return func
