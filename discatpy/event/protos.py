# SPDX-License-Identifier: MIT

from types import FunctionType

import discord_typings as dt
from discatcore import Dispatcher

__all__ = (
    "apply_events",
    "RawGatewayEvents",
)


def apply_events(*, source: type, dest: Dispatcher):
    assert isinstance(source, type), "source parameter must be a class!"
    assert isinstance(dest, Dispatcher), "dest parameter must be a Dispatcher!"

    for name in dir(source):
        value = getattr(source, name)
        if not name.startswith("_") and isinstance(value, FunctionType):
            dest.new_event(name).set_proto(value)


class RawGatewayEvents:
    def __new__(cls):
        raise TypeError("You cannot create a RawGatewayEvents object")

    def ready(self, data: dt.ReadyData):
        pass

    # TODO: resumed, reconnect, invalid_session

    def application_command_permissions_update(
        self, data: dt.ApplicationCommandPermissionsUpdateData
    ):
        pass

    def auto_moderation_rule_create(self, data: dt.AutoModerationRuleData):
        pass

    def auto_moderation_rule_update(self, data: dt.AutoModerationRuleData):
        pass

    def auto_moderation_rule_delete(self, data: dt.AutoModerationRuleData):
        pass

    # TODO: auto_moderation_action_execution

    def channel_create(self, data: dt.ChannelCreateData):
        pass

    def channel_update(self, data: dt.ChannelUpdateData):
        pass

    def channel_delete(self, data: dt.ChannelDeleteData):
        pass

    def channel_pins_update(self, data: dt.ChannelPinsUpdateData):
        pass

    def thread_create(self, data: dt.ThreadCreateData):
        pass

    def thread_update(self, data: dt.ThreadUpdateData):
        pass

    def thread_delete(self, data: dt.ThreadDeleteData):
        pass

    def thread_list_sync(self, data: dt.ThreadListSyncData):
        pass

    def thread_member_update(self, data: dt.ThreadMemberUpdateData):
        pass

    def thread_members_update(self, data: dt.ThreadMembersUpdateData):
        pass

    def guild_create(self, data: dt.GuildCreateData):
        pass

    def guild_update(self, data: dt.GuildUpdateData):
        pass

    def guild_delete(self, data: dt.GuildDeleteData):
        pass

    def guild_ban_add(self, data: dt.GuildBanAddData):
        pass

    def guild_ban_remove(self, data: dt.GuildBanRemoveData):
        pass

    def guild_emojis_update(self, data: dt.GuildEmojisUpdateData):
        pass

    def guild_stickers_update(self, data: dt.GuildStickersUpdateData):
        pass

    def guild_integrations_update(self, data: dt.GuildIntergrationsUpdateData):
        pass

    def guild_member_add(self, data: dt.GuildMemberAddData):
        pass

    def guild_member_remove(self, data: dt.GuildMemberRemoveData):
        pass

    def guild_member_update(self, data: dt.GuildMemberUpdateData):
        pass

    # TODO: guild_members_chunk

    def guild_role_create(self, data: dt.GuildRoleCreateData):
        pass

    def guild_role_update(self, data: dt.GuildRoleUpdateData):
        pass

    def guild_role_delete(self, data: dt.GuildRoleDeleteData):
        pass

    def guild_scheduled_event_create(self, data: dt.GuildScheduledEventCreateData):
        pass

    def guild_scheduled_event_update(self, data: dt.GuildScheduledEventUpdateData):
        pass

    def guild_scheduled_event_delete(self, data: dt.GuildScheduledEventDeleteData):
        pass

    def guild_scheduled_event_user_add(self, data: dt.GuildScheduledEventUserAddData):
        pass

    def guild_scheduled_event_user_remove(self, data: dt.GuildScheduledEventUserRemoveData):
        pass

    def integration_create(self, data: dt.IntegrationCreateData):
        pass

    def integration_update(self, data: dt.IntegrationUpdateData):
        pass

    def integration_delete(self, data: dt.IntegrationDeleteData):
        pass

    def interaction_create(self, data: dt.InteractionCreateData):
        pass

    def invite_create(self, data: dt.InviteCreateData):
        pass

    def invite_delete(self, data: dt.InviteDeleteData):
        pass

    def message_create(self, data: dt.MessageCreateData):
        pass

    def message_update(self, data: dt.MessageUpdateData):
        pass

    def message_delete(self, data: dt.MessageDeleteData):
        pass

    def message_delete_bulk(self, data: dt.MessageDeleteBulkData):
        pass

    def message_reaction_add(self, data: dt.MessageReactionAddData):
        pass

    def message_reaction_remove(self, data: dt.MessageReactionRemoveData):
        pass

    def message_reaction_remove_all(self, data: dt.MessageReactionRemoveAllData):
        pass

    def message_reaction_remove_emoji(self, data: dt.MessageReactionRemoveEmojiData):
        pass

    def presence_update(self, data: dt.PresenceUpdateData):
        pass

    def stage_instance_create(self, data: dt.StageInstanceCreateData):
        pass

    def stage_instance_update(self, data: dt.StageInstanceUpdateData):
        pass

    def stage_instance_delete(self, data: dt.StageInstanceDeleteData):
        pass

    def typing_start(self, data: dt.TypingStartData):
        pass

    def user_update(self, data: dt.UserUpdateData):
        pass

    def voice_state_update(self, data: dt.VoiceStateData):
        pass

    def voice_server_update(self, data: dt.VoiceServerUpdateData):
        pass

    def webhooks_update(self, data: dt.WebhooksUpdateData):
        pass
