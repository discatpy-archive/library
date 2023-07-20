# SPDX-License-Identifier: MIT

import typing as t

import discord_typings as dt
from discatcore.utils import Dispatcher, Event

__all__ = (
    "apply_events",
    "RawGatewayEvents",
)


def apply_events(*, source: type, dest: Dispatcher):
    assert isinstance(source, type), "source parameter must be a class!"
    assert isinstance(dest, Dispatcher), "dest parameter must be a Dispatcher!"

    for name in dir(source):
        value = getattr(source, name)
        if not name.startswith("_") and isinstance(value, staticmethod):
            event: Event
            if dest.has_event(name):
                event = t.cast(Event, dest.get_event(name))
            else:
                event = dest.new_event(name)

            event.set_proto(t.cast(staticmethod[None], value))


class _BaseProtoEvents:
    def __new__(cls):
        raise TypeError(f"You cannot create a {cls.__name__} object!")


class RawGatewayEvents(_BaseProtoEvents):
    @staticmethod
    def ready(data: dt.ReadyData):
        pass

    @staticmethod
    def resumed():
        pass

    @staticmethod
    def reconnect():
        pass

    @staticmethod
    def invalid_session(resumable: bool):
        pass

    @staticmethod
    def application_command_permissions_update(data: dt.ApplicationCommandPermissionsUpdateData):
        pass

    @staticmethod
    def auto_moderation_rule_create(data: dt.AutoModerationRuleData):
        pass

    @staticmethod
    def auto_moderation_rule_update(data: dt.AutoModerationRuleData):
        pass

    @staticmethod
    def auto_moderation_rule_delete(data: dt.AutoModerationRuleData):
        pass

    # TODO: auto_moderation_action_execution

    @staticmethod
    def channel_create(data: dt.ChannelCreateData):
        pass

    @staticmethod
    def channel_update(data: dt.ChannelUpdateData):
        pass

    @staticmethod
    def channel_delete(data: dt.ChannelDeleteData):
        pass

    @staticmethod
    def channel_pins_update(data: dt.ChannelPinsUpdateData):
        pass

    @staticmethod
    def thread_create(data: dt.ThreadCreateData):
        pass

    @staticmethod
    def thread_update(data: dt.ThreadUpdateData):
        pass

    @staticmethod
    def thread_delete(data: dt.ThreadDeleteData):
        pass

    @staticmethod
    def thread_list_sync(data: dt.ThreadListSyncData):
        pass

    @staticmethod
    def thread_member_update(data: dt.ThreadMemberUpdateData):
        pass

    @staticmethod
    def thread_members_update(data: dt.ThreadMembersUpdateData):
        pass

    @staticmethod
    def guild_create(data: dt.GuildCreateData):
        pass

    @staticmethod
    def guild_update(data: dt.GuildUpdateData):
        pass

    @staticmethod
    def guild_delete(data: dt.GuildDeleteData):
        pass

    @staticmethod
    def guild_ban_add(data: dt.GuildBanAddData):
        pass

    @staticmethod
    def guild_ban_remove(data: dt.GuildBanRemoveData):
        pass

    @staticmethod
    def guild_emojis_update(data: dt.GuildEmojisUpdateData):
        pass

    @staticmethod
    def guild_stickers_update(data: dt.GuildStickersUpdateData):
        pass

    @staticmethod
    def guild_integrations_update(data: dt.GuildIntergrationsUpdateData):
        pass

    @staticmethod
    def guild_member_add(data: dt.GuildMemberAddData):
        pass

    @staticmethod
    def guild_member_remove(data: dt.GuildMemberRemoveData):
        pass

    @staticmethod
    def guild_member_update(data: dt.GuildMemberUpdateData):
        pass

    @staticmethod
    def guild_members_chunk(data: dt.GuildMembersChunkData):
        pass

    @staticmethod
    def guild_role_create(data: dt.GuildRoleCreateData):
        pass

    @staticmethod
    def guild_role_update(data: dt.GuildRoleUpdateData):
        pass

    @staticmethod
    def guild_role_delete(data: dt.GuildRoleDeleteData):
        pass

    @staticmethod
    def guild_scheduled_event_create(data: dt.GuildScheduledEventCreateData):
        pass

    @staticmethod
    def guild_scheduled_event_update(data: dt.GuildScheduledEventUpdateData):
        pass

    @staticmethod
    def guild_scheduled_event_delete(data: dt.GuildScheduledEventDeleteData):
        pass

    @staticmethod
    def guild_scheduled_event_user_add(data: dt.GuildScheduledEventUserAddData):
        pass

    @staticmethod
    def guild_scheduled_event_user_remove(data: dt.GuildScheduledEventUserRemoveData):
        pass

    @staticmethod
    def integration_create(data: dt.IntegrationCreateData):
        pass

    @staticmethod
    def integration_update(data: dt.IntegrationUpdateData):
        pass

    @staticmethod
    def integration_delete(data: dt.IntegrationDeleteData):
        pass

    @staticmethod
    def interaction_create(data: dt.InteractionCreateData):
        pass

    @staticmethod
    def invite_create(data: dt.InviteCreateData):
        pass

    @staticmethod
    def invite_delete(data: dt.InviteDeleteData):
        pass

    @staticmethod
    def message_create(data: dt.MessageCreateData):
        pass

    @staticmethod
    def message_update(data: dt.MessageUpdateData):
        pass

    @staticmethod
    def message_delete(data: dt.MessageDeleteData):
        pass

    @staticmethod
    def message_delete_bulk(data: dt.MessageDeleteBulkData):
        pass

    @staticmethod
    def message_reaction_add(data: dt.MessageReactionAddData):
        pass

    @staticmethod
    def message_reaction_remove(data: dt.MessageReactionRemoveData):
        pass

    @staticmethod
    def message_reaction_remove_all(data: dt.MessageReactionRemoveAllData):
        pass

    @staticmethod
    def message_reaction_remove_emoji(data: dt.MessageReactionRemoveEmojiData):
        pass

    @staticmethod
    def presence_update(data: dt.PresenceUpdateData):
        pass

    @staticmethod
    def stage_instance_create(data: dt.StageInstanceCreateData):
        pass

    @staticmethod
    def stage_instance_update(data: dt.StageInstanceUpdateData):
        pass

    @staticmethod
    def stage_instance_delete(data: dt.StageInstanceDeleteData):
        pass

    @staticmethod
    def typing_start(data: dt.TypingStartData):
        pass

    @staticmethod
    def user_update(data: dt.UserUpdateData):
        pass

    @staticmethod
    def voice_state_update(data: dt.VoiceStateData):
        pass

    @staticmethod
    def voice_server_update(data: dt.VoiceServerUpdateData):
        pass

    @staticmethod
    def webhooks_update(data: dt.WebhooksUpdateData):
        pass
