# SPDX-License-Identifier: MIT

# this file was auto-generated by scripts/generate_endpoints.py

import typing as t

import discord_typings as dt

from ...file import BasicFile
from ...types import Unset, UnsetOr
from ..route import Route
from .core import EndpointMixin

__all__ = ("ChannelEndpoints",)


class ChannelEndpoints(EndpointMixin):
    def get_channel(self, channel_id: dt.Snowflake):
        return self.request(
            Route("GET", "/channels/{channel_id}", channel_id=channel_id)
        )

    def modify_channel(
        self,
        channel_id: dt.Snowflake,
        *,
        name: UnsetOr[str] = Unset,
        type: UnsetOr[dt.ChannelTypes] = Unset,
        position: UnsetOr[t.Optional[int]] = Unset,
        topic: UnsetOr[t.Optional[str]] = Unset,
        nsfw: UnsetOr[t.Optional[bool]] = Unset,
        rate_limit_per_user: UnsetOr[t.Optional[int]] = Unset,
        bitrate: UnsetOr[t.Optional[int]] = Unset,
        user_limit: UnsetOr[t.Optional[int]] = Unset,
        permission_overwrites: UnsetOr[
            t.Optional[list[dt.PermissionOverwriteData]]
        ] = Unset,
        parent_id: UnsetOr[t.Optional[dt.Snowflake]] = Unset,
        rtc_region: UnsetOr[t.Optional[str]] = Unset,
        video_quality_mode: UnsetOr[t.Optional[dt.VideoQualityModes]] = Unset,
        default_auto_archive_duration: UnsetOr[t.Optional[int]] = Unset,
        flags: UnsetOr[int] = Unset,
        available_tags: UnsetOr[list[dt.ForumTagData]] = Unset,
        default_reaction_emoji: UnsetOr[t.Optional[dt.DefaultReactionData]] = Unset,
        default_thread_rate_limit_per_user: UnsetOr[int] = Unset,
        default_sort_order: UnsetOr[t.Optional[int]] = Unset,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route("PATCH", "/channels/{channel_id}", channel_id=channel_id),
            json_params={
                "name": name,
                "type": type,
                "position": position,
                "topic": topic,
                "nsfw": nsfw,
                "rate_limit_per_user": rate_limit_per_user,
                "bitrate": bitrate,
                "user_limit": user_limit,
                "permission_overwrites": permission_overwrites,
                "parent_id": parent_id,
                "rtc_region": rtc_region,
                "video_quality_mode": video_quality_mode,
                "default_auto_archive_duration": default_auto_archive_duration,
                "flags": flags,
                "available_tags": available_tags,
                "default_reaction_emoji": default_reaction_emoji,
                "default_thread_rate_limit_per_user": default_thread_rate_limit_per_user,
                "default_sort_order": default_sort_order,
            },
            reason=reason,
        )

    def modify_thread(
        self,
        channel_id: dt.Snowflake,
        *,
        name: UnsetOr[str] = Unset,
        archived: UnsetOr[bool] = Unset,
        auto_archive_duration: UnsetOr[int] = Unset,
        locked: UnsetOr[bool] = Unset,
        invitable: UnsetOr[bool] = Unset,
        rate_limit_per_user: UnsetOr[t.Optional[int]] = Unset,
        flags: UnsetOr[int] = Unset,
        applied_tags: UnsetOr[list[dt.Snowflake]] = Unset,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route("PATCH", "/channels/{channel_id}", channel_id=channel_id),
            json_params={
                "name": name,
                "archived": archived,
                "auto_archive_duration": auto_archive_duration,
                "locked": locked,
                "invitable": invitable,
                "rate_limit_per_user": rate_limit_per_user,
                "flags": flags,
                "applied_tags": applied_tags,
            },
            reason=reason,
        )

    def delete_channel(self, channel_id: dt.Snowflake, reason: t.Optional[str] = None):
        return self.request(
            Route("DELETE", "/channels/{channel_id}", channel_id=channel_id),
            reason=reason,
        )

    def get_channel_messages(
        self,
        channel_id: dt.Snowflake,
        *,
        around: UnsetOr[dt.Snowflake] = Unset,
        before: UnsetOr[dt.Snowflake] = Unset,
        after: UnsetOr[dt.Snowflake] = Unset,
        limit: int = 50,
    ):
        return self.request(
            Route("GET", "/channels/{channel_id}/messages", channel_id=channel_id),
            query_params={
                "around": around,
                "before": before,
                "after": after,
                "limit": limit,
            },
        )

    def get_channel_message(self, channel_id: dt.Snowflake, message_id: dt.Snowflake):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/messages/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            )
        )

    def create_message(
        self,
        channel_id: dt.Snowflake,
        *,
        content: UnsetOr[str] = Unset,
        nonce: UnsetOr[t.Union[str, int]] = Unset,
        tts: UnsetOr[bool] = Unset,
        embeds: UnsetOr[list[dt.EmbedData]] = Unset,
        allowed_mentions: UnsetOr[dt.AllowedMentionsData] = Unset,
        message_reference: UnsetOr[dt.MessageReferenceData] = Unset,
        components: UnsetOr[list[dt.ComponentData]] = Unset,
        sticker_ids: UnsetOr[list[dt.Snowflake]] = Unset,
        attachments: UnsetOr[list[dt.PartialAttachmentData]] = Unset,
        flags: UnsetOr[int] = Unset,
        files: UnsetOr[list[BasicFile]] = Unset,
    ):
        return self.request(
            Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id),
            json_params={
                "content": content,
                "nonce": nonce,
                "tts": tts,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "message_reference": message_reference,
                "components": components,
                "sticker_ids": sticker_ids,
                "attachments": attachments,
                "flags": flags,
            },
            files=files,
        )

    def crosspost_message(self, channel_id: dt.Snowflake, message_id: dt.Snowflake):
        return self.request(
            Route(
                "POST",
                "/channels/{channel_id}/messages/{message_id}/crosspost",
                channel_id=channel_id,
                message_id=message_id,
            )
        )

    def create_reaction(
        self, channel_id: dt.Snowflake, message_id: dt.Snowflake, emoji: str
    ):
        return self.request(
            Route(
                "PUT",
                "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            )
        )

    def delete_own_reaction(
        self, channel_id: dt.Snowflake, message_id: dt.Snowflake, emoji: str
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            )
        )

    def delete_user_reaction(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        emoji: str,
        user_id: dt.Snowflake,
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}",
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                user_id=user_id,
            )
        )

    def get_reactions(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        emoji: str,
        *,
        after: UnsetOr[dt.Snowflake] = Unset,
        limit: int = 25,
    ):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            ),
            query_params={"after": after, "limit": limit},
        )

    def delete_all_reactions(self, channel_id: dt.Snowflake, message_id: dt.Snowflake):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}/reactions",
                channel_id=channel_id,
                message_id=message_id,
            )
        )

    def delete_all_reactions_for_emoji(
        self, channel_id: dt.Snowflake, message_id: dt.Snowflake, emoji: str
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
            )
        )

    def edit_message(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        *,
        content: UnsetOr[t.Optional[str]] = Unset,
        embeds: UnsetOr[t.Optional[list[dt.EmbedData]]] = Unset,
        flags: UnsetOr[t.Optional[int]] = Unset,
        allowed_mentions: UnsetOr[t.Optional[dt.AllowedMentionsData]] = Unset,
        components: UnsetOr[t.Optional[list[dt.ComponentData]]] = Unset,
        attachments: UnsetOr[t.Optional[list[dt.PartialAttachmentData]]] = Unset,
        files: UnsetOr[list[BasicFile]] = Unset,
    ):
        return self.request(
            Route(
                "PATCH",
                "/channels/{channel_id}/messages/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            ),
            json_params={
                "content": content,
                "embeds": embeds,
                "flags": flags,
                "allowed_mentions": allowed_mentions,
                "components": components,
                "attachments": attachments,
            },
            files=files,
        )

    def delete_message(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            ),
            reason=reason,
        )

    def bulk_delete_messages(
        self,
        channel_id: dt.Snowflake,
        *,
        messages: list[dt.MessageData],
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "POST",
                "/channels/{channel_id}/messages/bulk-delete",
                channel_id=channel_id,
            ),
            json_params={"messages": messages},
            reason=reason,
        )

    def edit_channel_permissions(
        self,
        channel_id: dt.Snowflake,
        overwrite_id: dt.Snowflake,
        *,
        allow: UnsetOr[t.Optional[str]] = Unset,
        deny: UnsetOr[t.Optional[str]] = Unset,
        type: int,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "PUT",
                "/channels/{channel_id}/permissions/{overwrite_id}",
                channel_id=channel_id,
                overwrite_id=overwrite_id,
            ),
            json_params={"allow": allow, "deny": deny, "type": type},
            reason=reason,
        )

    def get_channel_invites(self, channel_id: dt.Snowflake):
        return self.request(
            Route("GET", "/channels/{channel_id}/invites", channel_id=channel_id)
        )

    def create_channel_invite(
        self,
        channel_id: dt.Snowflake,
        *,
        max_age: int = 86400,
        max_uses: int = 0,
        temporary: bool = False,
        unique: bool = False,
        target_type: dt.InviteTargetTypes,
        target_user_id: UnsetOr[dt.Snowflake] = Unset,
        target_application_id: UnsetOr[dt.Snowflake] = Unset,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route("POST", "/channels/{channel_id}/invites", channel_id=channel_id),
            json_params={
                "max_age": max_age,
                "max_uses": max_uses,
                "temporary": temporary,
                "unique": unique,
                "target_type": target_type,
                "target_user_id": target_user_id,
                "target_application_id": target_application_id,
            },
            reason=reason,
        )

    def delete_channel_permission(
        self,
        channel_id: dt.Snowflake,
        overwrite_id: dt.Snowflake,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/permissions/{overwrite_id}",
                channel_id=channel_id,
                overwrite_id=overwrite_id,
            ),
            reason=reason,
        )

    def follow_announcement_channel(
        self, channel_id: dt.Snowflake, *, webhook_channel_id: dt.Snowflake
    ):
        return self.request(
            Route("POST", "/channels/{channel_id}/followers", channel_id=channel_id),
            json_params={"webhook_channel_id": webhook_channel_id},
        )

    def trigger_typing_indicator(self, channel_id: dt.Snowflake):
        return self.request(
            Route("POST", "/channels/{channel_id}/typing", channel_id=channel_id)
        )

    def get_pinned_messages(self, channel_id: dt.Snowflake):
        return self.request(
            Route("GET", "/channels/{channel_id}/pins", channel_id=channel_id)
        )

    def pin_message(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "PUT",
                "/channels/{channel_id}/pins/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            ),
            reason=reason,
        )

    def unpin_message(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/pins/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            ),
            reason=reason,
        )

    def start_thread_from_message(
        self,
        channel_id: dt.Snowflake,
        message_id: dt.Snowflake,
        *,
        name: str,
        auto_archive_duration: UnsetOr[int] = Unset,
        rate_limit_per_user: UnsetOr[t.Optional[int]] = Unset,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route(
                "POST",
                "/channels/{channel_id}/messages/{message_id}/threads",
                channel_id=channel_id,
                message_id=message_id,
            ),
            json_params={
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "rate_limit_per_user": rate_limit_per_user,
            },
            reason=reason,
        )

    def start_thread_without_message(
        self,
        channel_id: dt.Snowflake,
        *,
        name: str,
        auto_archive_duration: UnsetOr[int] = Unset,
        type: UnsetOr[int] = Unset,
        invitable: UnsetOr[bool] = Unset,
        rate_limit_per_user: UnsetOr[t.Optional[int]] = Unset,
        reason: t.Optional[str] = None,
    ):
        return self.request(
            Route("POST", "/channels/{channel_id}/threads", channel_id=channel_id),
            json_params={
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "type": type,
                "invitable": invitable,
                "rate_limit_per_user": rate_limit_per_user,
            },
            reason=reason,
        )

    def start_thread_in_forum_channel(
        self,
        channel_id: dt.Snowflake,
        *,
        name: str,
        auto_archive_duration: UnsetOr[int] = Unset,
        rate_limit_per_user: UnsetOr[t.Optional[int]] = Unset,
        content: UnsetOr[str] = Unset,
        embeds: UnsetOr[list[dt.EmbedData]] = Unset,
        allowed_mentions: UnsetOr[dt.AllowedMentionsData] = Unset,
        components: UnsetOr[list[dt.ComponentData]] = Unset,
        sticker_ids: UnsetOr[list[dt.Snowflake]] = Unset,
        attachments: UnsetOr[list[dt.PartialAttachmentData]] = Unset,
        flags: UnsetOr[int] = Unset,
        applied_tags: UnsetOr[list[dt.Snowflake]] = Unset,
        reason: t.Optional[str] = None,
        files: UnsetOr[list[BasicFile]] = Unset,
    ):
        return self.request(
            Route("POST", "/channels/{channel_id}/threads", channel_id=channel_id),
            json_params={
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "rate_limit_per_user": rate_limit_per_user,
                "content": content,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "components": components,
                "sticker_ids": sticker_ids,
                "attachments": attachments,
                "flags": flags,
                "applied_tags": applied_tags,
            },
            reason=reason,
            files=files,
        )

    def join_thread(self, channel_id: dt.Snowflake):
        return self.request(
            Route(
                "PUT",
                "/channels/{channel_id}/thread-members/@me",
                channel_id=channel_id,
            )
        )

    def add_thread_member(self, channel_id: dt.Snowflake, user_id: dt.Snowflake):
        return self.request(
            Route(
                "PUT",
                "/channels/{channel_id}/thread-members/{user_id}",
                channel_id=channel_id,
                user_id=user_id,
            )
        )

    def leave_thread(self, channel_id: dt.Snowflake):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/thread-members/@me",
                channel_id=channel_id,
            )
        )

    def remove_thread_member(self, channel_id: dt.Snowflake, user_id: dt.Snowflake):
        return self.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/thread-members/{user_id}",
                channel_id=channel_id,
                user_id=user_id,
            )
        )

    def get_thread_member(self, channel_id: dt.Snowflake, user_id: dt.Snowflake):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/thread-members/{user_id}",
                channel_id=channel_id,
                user_id=user_id,
            )
        )

    def list_thread_members(self, channel_id: dt.Snowflake):
        return self.request(
            Route("GET", "/channels/{channel_id}/thread-members", channel_id=channel_id)
        )

    def list_public_archived_threads(
        self,
        channel_id: dt.Snowflake,
        *,
        before: UnsetOr[str] = Unset,
        limit: UnsetOr[int] = Unset,
    ):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/threads/archived/public",
                channel_id=channel_id,
            ),
            query_params={"before": before, "limit": limit},
        )

    def list_private_archived_threads(
        self,
        channel_id: dt.Snowflake,
        *,
        before: UnsetOr[str] = Unset,
        limit: UnsetOr[int] = Unset,
    ):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/threads/archived/private",
                channel_id=channel_id,
            ),
            query_params={"before": before, "limit": limit},
        )

    def list_joined_private_archived_threads(
        self,
        channel_id: dt.Snowflake,
        *,
        before: UnsetOr[str] = Unset,
        limit: UnsetOr[int] = Unset,
    ):
        return self.request(
            Route(
                "GET",
                "/channels/{channel_id}/users/@me/threads/archived/private",
                channel_id=channel_id,
            ),
            query_params={"before": before, "limit": limit},
        )