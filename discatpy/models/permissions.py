# SPDX-License-Identifier: MIT
import typing as t

from typing_extensions import Self

from ..flags import Flag, flag

__all__ = ("Permissions", "PermissionOverwrite")


class Permissions(Flag):
    if t.TYPE_CHECKING:

        def __init__(
            self,
            *,
            create_instant_invite: bool = ...,
            kick_members: bool = ...,
            ban_members: bool = ...,
            administrator: bool = ...,
            manage_channels: bool = ...,
            manage_guild: bool = ...,
            add_reactions: bool = ...,
            view_audit_log: bool = ...,
            priority_speaker: bool = ...,
            stream: bool = ...,
            view_channel: bool = ...,
            send_messages: bool = ...,
            send_tts_messages: bool = ...,
            manage_messages: bool = ...,
            embed_links: bool = ...,
            attach_files: bool = ...,
            read_message_history: bool = ...,
            mention_everyone: bool = ...,
            use_external_emojis: bool = ...,
            view_guild_insights: bool = ...,
            connect: bool = ...,
            speak: bool = ...,
            mute_members: bool = ...,
            deafen_members: bool = ...,
            move_members: bool = ...,
            use_vad: bool = ...,
            change_nickname: bool = ...,
            manage_nicknames: bool = ...,
            manage_roles: bool = ...,
            manage_webhooks: bool = ...,
            manage_emojis_and_stickers: bool = ...,
            use_application_commands: bool = ...,
            request_to_speak: bool = ...,
            manage_threads: bool = ...,
            create_public_threads: bool = ...,
            create_private_threads: bool = ...,
            use_external_stickers: bool = ...,
            send_messages_in_threads: bool = ...,
            use_embed_activities: bool = ...,
            moderate_members: bool = ...,
        ) -> None:
            ...

    @flag
    def create_instant_invite() -> int:
        return 1 << 0

    @flag
    def kick_members() -> int:
        return 1 << 1

    @flag
    def ban_members() -> int:
        return 1 << 2

    @flag
    def administrator() -> int:
        return 1 << 3

    @flag
    def manage_channels() -> int:
        return 1 << 4

    @flag
    def manage_guild() -> int:
        return 1 << 5

    @flag
    def add_reactions() -> int:
        return 1 << 6

    @flag
    def view_audit_log() -> int:
        return 1 << 7

    @flag
    def priority_speaker() -> int:
        return 1 << 8

    @flag
    def stream() -> int:
        return 1 << 9

    @flag
    def view_channel() -> int:
        return 1 << 10

    @flag
    def send_messages() -> int:
        return 1 << 11

    @flag
    def send_tts_messages() -> int:
        return 1 << 12

    @flag
    def manage_messages() -> int:
        return 1 << 13

    @flag
    def embed_links() -> int:
        return 1 << 14

    @flag
    def attach_files() -> int:
        return 1 << 15

    @flag
    def read_message_history() -> int:
        return 1 << 16

    @flag
    def mention_everyone() -> int:
        return 1 << 17

    @flag
    def use_external_emojis() -> int:
        return 1 << 18

    @flag
    def view_guild_insights() -> int:
        return 1 << 19

    @flag
    def connect() -> int:
        return 1 << 20

    @flag
    def speak() -> int:
        return 1 << 21

    @flag
    def mute_members() -> int:
        return 1 << 22

    @flag
    def deafen_members() -> int:
        return 1 << 23

    @flag
    def move_members() -> int:
        return 1 << 24

    @flag
    def use_vad() -> int:
        return 1 << 25

    @flag
    def change_nickname() -> int:
        return 1 << 26

    @flag
    def manage_nicknames() -> int:
        return 1 << 27

    @flag
    def manage_roles() -> int:
        return 1 << 28

    @flag
    def manage_webhooks() -> int:
        return 1 << 29

    @flag
    def manage_emojis_and_stickers() -> int:
        return 1 << 30

    @flag
    def use_application_commands() -> int:
        return 1 << 31

    @flag
    def request_to_speak() -> int:
        return 1 << 32

    @flag
    def manage_events() -> int:
        return 1 << 33

    @flag
    def manage_threads() -> int:
        return 1 << 34

    @flag
    def create_public_threads() -> int:
        return 1 << 35

    @flag
    def create_private_threads() -> int:
        return 1 << 36

    @flag
    def use_external_stickers() -> int:
        return 1 << 37

    @flag
    def send_messages_in_threads() -> int:
        return 1 << 38

    @flag
    def use_embedded_activities() -> int:
        return 1 << 39

    @flag
    def moderate_members() -> int:
        return 1 << 40


class PermissionOverwrite:
    @t.overload
    def __init__(
        self,
    ) -> None:
        ...

    @t.overload
    def __init__(
        self,
        *,
        create_instant_invite: bool = ...,
        kick_members: bool = ...,
        ban_members: bool = ...,
        administrator: bool = ...,
        manage_channels: bool = ...,
        manage_guild: bool = ...,
        add_reactions: bool = ...,
        view_audit_log: bool = ...,
        priority_speaker: bool = ...,
        stream: bool = ...,
        view_channel: bool = ...,
        send_messages: bool = ...,
        send_tts_messages: bool = ...,
        manage_messages: bool = ...,
        embed_links: bool = ...,
        attach_files: bool = ...,
        read_message_history: bool = ...,
        mention_everyone: bool = ...,
        use_external_emojis: bool = ...,
        view_guild_insights: bool = ...,
        connect: bool = ...,
        speak: bool = ...,
        mute_members: bool = ...,
        deafen_members: bool = ...,
        move_members: bool = ...,
        use_vad: bool = ...,
        change_nickname: bool = ...,
        manage_nicknames: bool = ...,
        manage_roles: bool = ...,
        manage_webhooks: bool = ...,
        manage_emojis_and_stickers: bool = ...,
        use_application_commands: bool = ...,
        request_to_speak: bool = ...,
        manage_threads: bool = ...,
        create_public_threads: bool = ...,
        create_private_threads: bool = ...,
        use_external_stickers: bool = ...,
        send_messages_in_threads: bool = ...,
        use_embed_activities: bool = ...,
        moderate_members: bool = ...,
    ) -> None:
        ...

    def __init__(self, **kwargs: bool):
        self._allow: Permissions = Permissions.none()
        self._deny: Permissions = Permissions.none()

        self.set(**kwargs)

    def pair(self) -> tuple[Permissions, Permissions]:
        return self._allow, self._deny

    @classmethod
    def from_pair(cls: type[Self], allow: Permissions, deny: Permissions) -> Self:
        permissions_kwargs: dict[str, bool] = {}

        for name, val in allow:
            if val is True:
                permissions_kwargs[name] = True

        for name, val in deny:
            if val is True:
                permissions_kwargs[name] = False

        return cls(**permissions_kwargs)

    @t.overload
    def set(
        self,
    ) -> None:
        ...

    @t.overload
    def set(
        self,
        *,
        create_instant_invite: bool = ...,
        kick_members: bool = ...,
        ban_members: bool = ...,
        administrator: bool = ...,
        manage_channels: bool = ...,
        manage_guild: bool = ...,
        add_reactions: bool = ...,
        view_audit_log: bool = ...,
        priority_speaker: bool = ...,
        stream: bool = ...,
        view_channel: bool = ...,
        send_messages: bool = ...,
        send_tts_messages: bool = ...,
        manage_messages: bool = ...,
        embed_links: bool = ...,
        attach_files: bool = ...,
        read_message_history: bool = ...,
        mention_everyone: bool = ...,
        use_external_emojis: bool = ...,
        view_guild_insights: bool = ...,
        connect: bool = ...,
        speak: bool = ...,
        mute_members: bool = ...,
        deafen_members: bool = ...,
        move_members: bool = ...,
        use_vad: bool = ...,
        change_nickname: bool = ...,
        manage_nicknames: bool = ...,
        manage_roles: bool = ...,
        manage_webhooks: bool = ...,
        manage_emojis_and_stickers: bool = ...,
        use_application_commands: bool = ...,
        request_to_speak: bool = ...,
        manage_threads: bool = ...,
        create_public_threads: bool = ...,
        create_private_threads: bool = ...,
        use_external_stickers: bool = ...,
        send_messages_in_threads: bool = ...,
        use_embed_activities: bool = ...,
        moderate_members: bool = ...,
    ) -> None:
        ...

    def set(self, **kwargs: bool):
        allow_kwargs: dict[str, bool] = {n: v for n, v in kwargs.items() if v is True}
        deny_kwargs: dict[str, bool] = {n: v for n, v in kwargs.items() if v is False}

        self._allow = Permissions(**allow_kwargs) if allow_kwargs else Permissions.none()
        self._deny = Permissions(**deny_kwargs) if deny_kwargs else Permissions.none()
