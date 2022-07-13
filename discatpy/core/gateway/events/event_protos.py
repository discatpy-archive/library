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
from __future__ import annotations

from discord_typings import (
    ApplicationCommandPermissionsUpdateData, 
    ChannelCreateData,
    ChannelDeleteData,
    ChannelUpdateEvent,
    EmojiData,
    GuildCreateData,
    GuildDeleteData,
    GuildMemberAddData,
    GuildMemberData,
    GuildMemberUpdateData,
    GuildScheduledEventCreateData,
    GuildScheduledEventDeleteData,
    GuildScheduledEventUpdateData,
    GuildUpdateData,
    IntegrationData,
    InteractionCreateData,
    InviteCreateData,
    MessageCreateData,
    MessageUpdateData,
    PresenceUpdateData,
    RoleData,
    StageInstanceCreateData,
    StageInstanceDeleteData,
    StageInstanceUpdateData,
    StickerData,
    ThreadChannelData,
    ThreadCreateData,
    ThreadDeleteData,
    ThreadMemberData,
    ThreadUpdateData,
    UpdatePresenceData,
    UserData,
    VoiceStateUpdateData
)

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ...types import MissingOr, Snowflake

if TYPE_CHECKING:
    from ..client import Client

__all__ = ("GatewayEventProtos",)

class GatewayEventProtos:
    """Registers event protos for Gateway events."""
    def __init__(self, client: Client):
        self.client = client

        if not self.client._event_protos_handler_hooked:
            for k in dir(self):
                v = getattr(self, k)
                if not k.startswith("_") and callable(v):
                    print(v)
                    self.client.dispatcher.set_event_proto(v) #parent=self)

            self.client._event_protos_handler_hooked = True

    # Gateway State events

    async def ready(self):
        pass

    async def resumed(self):
        pass

    async def reconnect(self):
        pass

    async def invalid_session(self, reconnect: bool):
        pass

    # Application Command events
    
    async def application_command_permissions_update(self, permissions: ApplicationCommandPermissionsUpdateData):
        pass

    # TODO: Auto Moderation events

    # Channel/Thread events

    async def channel_create(self, channel: ChannelCreateData):
        pass

    async def channel_update(self, channel: ChannelUpdateEvent):
        pass

    async def channel_delete(self, channel: ChannelDeleteData):
        pass

    async def thread_create(self, thread: ThreadCreateData):
        pass

    async def thread_update(self, thread: ThreadUpdateData):
        pass

    async def thread_delete(self, thread: ThreadDeleteData):
        pass

    async def thread_list_sync(
        self, 
        guild_id: Snowflake, 
        channel_ids: List[Snowflake], 
        threads: List[ThreadChannelData], 
        members: List[ThreadMemberData]
    ):
        pass

    async def thread_members_update(
        self, 
        id: Snowflake, 
        guild_id: Snowflake, 
        member_count: int, 
        added_members: MissingOr[List[ThreadMemberData]],
        removed_member_ids: MissingOr[List[Snowflake]]
    ):
        pass

    async def channel_pins_update(
        self, 
        guild_id: MissingOr[Snowflake], 
        channel_id: Snowflake, 
        last_pin_timestamp: MissingOr[Optional[datetime]]
    ):
        pass

    # Guild events

    async def guild_create(self, guild: GuildCreateData):
        pass

    async def guild_update(self, guild: GuildUpdateData):
        pass

    async def guild_delete(self, guild: GuildDeleteData):
        pass

    async def guild_ban_add(self, guild_id: Snowflake, user: UserData):
        pass

    async def guild_ban_remove(self, guild_id: Snowflake, user: UserData):
        pass

    async def guild_emojis_update(self, guild_id: Snowflake, emojis: List[EmojiData]):
        pass

    async def guild_stickers_update(self, guild_id: Snowflake, stickers: List[StickerData]):
        pass

    async def guild_integrations_update(self, guild_id: Snowflake):
        pass

    async def guild_member_add(self, member: GuildMemberAddData):
        pass

    async def guild_member_remove(self, guild_id: Snowflake, user: UserData):
        pass

    async def guild_member_update(self, member: GuildMemberUpdateData):
        pass

    async def guild_members_chunk(
        self, 
        guild_id: Snowflake, 
        members: List[GuildMemberData],
        chunk_index: int,
        chunk_count: int,
        not_found: MissingOr[List[Snowflake]],
        presences: MissingOr[List[UpdatePresenceData]],
        nonce: MissingOr[str]
    ):
        pass

    async def guild_role_create(self, guild_id: Snowflake, role: RoleData):
        pass

    async def guild_role_update(self, guild_id: Snowflake, role: RoleData):
        pass

    async def guild_role_delete(self, guild_id: Snowflake, role_id: Snowflake):
        pass

    async def guild_scheduled_event_create(self, scheduled_event: GuildScheduledEventCreateData):
        pass

    async def guild_scheduled_event_update(self, scheduled_event: GuildScheduledEventUpdateData):
        pass

    async def guild_scheduled_event_delete(self, scheduled_event: GuildScheduledEventDeleteData):
        pass

    async def guild_scheduled_event_user_add(self, guild_scheduled_event_id: Snowflake, user_id: Snowflake, guild_id: Snowflake):
        pass

    async def guild_scheduled_event_user_remove(self, guild_scheduled_event_id: Snowflake, user_id: Snowflake, guild_id: Snowflake):
        pass

    # Integration events
    # TODO: remove?

    async def integration_create(self, integration: IntegrationData):
        pass

    async def integration_update(self, integration: IntegrationData):
        pass

    async def integration_delete(self, integration: IntegrationData):
        pass

    # Invite events

    async def invite_create(self, invite: InviteCreateData):
        pass

    async def invite_delete(self, channel_id: Snowflake, guild_id: MissingOr[Snowflake], code: str):
        pass

    # Message events

    async def message_create(self, message: MessageCreateData):
        pass

    async def message_update(self, message: MessageUpdateData):
        pass

    async def message_delete(self, id: Snowflake, channel_id: Snowflake, guild_id: MissingOr[Snowflake]):
        pass

    async def message_delete_bulk(self, ids: List[Snowflake], channel_id: Snowflake, guild_id: MissingOr[Snowflake]):
        pass

    async def message_reaction_add(
        self,
        user_id: Snowflake,
        channel_id: Snowflake,
        message_id: Snowflake,
        guild_id: MissingOr[Snowflake],
        member: MissingOr[GuildMemberData],
        emoji: EmojiData
    ):
        pass

    async def message_reaction_remove(
        self,
        user_id: Snowflake,
        channel_id: Snowflake,
        message_id: Snowflake,
        guild_id: MissingOr[Snowflake],
        emoji: EmojiData
    ):
        pass

    async def message_reaction_remove_all(self, channel_id: Snowflake, message_id: Snowflake, guild_id: MissingOr[Snowflake]):
        pass

    async def message_reaction_remove_emoji(
        self, 
        channel_id: Snowflake, 
        guild_id: MissingOr[Snowflake],
        message_id: Snowflake,
        emoji: EmojiData
    ):
        pass

    # Presence events

    async def presence_update(self, presence: PresenceUpdateData):
        pass

    async def typing_start(self, channel_id: Snowflake, guild_id: MissingOr[Snowflake], user_id: Snowflake, timestamp: int, member: MissingOr[GuildMemberData]):
        pass

    # User events
    # TODO: remove?

    async def user_update(self, user: UserData):
        pass

    # Voice events

    async def voice_state_update(self, voice_state: VoiceStateUpdateData):
        pass

    async def voice_server_update(self, token: str, guild_id: Snowflake, endpoint: Optional[str]):
        pass

    # Webhook events

    async def webhooks_update(self, guild_id: Snowflake, channel_id: Snowflake):
        pass

    # Interaction events

    async def interaction_create(self, interaction: InteractionCreateData):
        pass

    # Stage Instance events

    async def stage_instance_create(self, stage_instance: StageInstanceCreateData):
        pass

    async def stage_instance_update(self, stage_instance: StageInstanceUpdateData):
        pass

    async def stage_instance_delete(self, stage_instance: StageInstanceDeleteData):
        pass
