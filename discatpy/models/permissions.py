# SPDX-License-Identifier: MIT

from typing_extensions import Self

from ..flags import Flag, flag

__all__ = ("Permissions", "PermissionOverwrite")


class Permissions(Flag):
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
    def __init__(self, **kwargs: bool):
        self._permission: Permissions = Permissions(**kwargs)

    def pair(self) -> tuple[Permissions, Permissions]:
        allow = Permissions.none()
        deny = Permissions.none()

        for name in self._permission.__members__.keys():
            if getattr(self._permission, name):
                setattr(allow, name, True)
            else:
                setattr(deny, name, False)

        return allow, deny

    @classmethod
    def from_pair(cls: type[Self], allow: Permissions, deny: Permissions) -> Self:
        permissions_kwargs: dict[str, bool] = {}

        for name, val in allow:
            if val:
                permissions_kwargs[name] = True

        for name, val in deny:
            if not val:
                permissions_kwargs[name] = False

        return cls(**permissions_kwargs)

    def set(self, **kwargs: bool):
        self._permission = Permissions(**kwargs)
