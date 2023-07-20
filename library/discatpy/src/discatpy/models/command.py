# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from enum import Enum, auto

import attr
import discord_typings as dt
from typing_extensions import NotRequired, TypedDict

from discatcore.types import Unset, UnsetOr
from discatcore.utils import Snowflake

from .permissions import Permissions

if t.TYPE_CHECKING:
    from ..bot import Bot

__all__ = (
    "Locales",
    "ApplicationCommandTypes",
    "ApplicationCommandOptionTypes",
    "ApplicationCommand",
    "ApplicationCommandOptionChoiceData",
    "ApplicationCommandOptionChoice",
    "ApplicationCommandOption",
)


class Locales(str, Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[t.Any]
    ) -> t.Any:
        return name.replace("_", "-")

    da = auto()
    de = auto()
    en_GB = auto()
    en_US = auto()
    es_ES = auto()
    fr = auto()
    hr = auto()
    it = auto()
    lt = auto()
    hu = auto()
    nl = auto()
    no = auto()
    pl = auto()
    pt_BR = auto()
    ro = auto()
    fi = auto()
    sv_SE = auto()
    vi = auto()
    tr = auto()
    cs = auto()
    el = auto()
    bg = auto()
    ru = auto()
    uk = auto()
    hi = auto()
    th = auto()
    zh_CN = auto()
    ja = auto()
    zh_TW = auto()
    ko = auto()


class ApplicationCommandTypes(int, Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionTypes(int, Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class ApplicationCommand:
    def __init__(self, *, bot: Bot, data: dt.ApplicationCommandData):
        self.bot: Bot = bot
        self.data: dt.ApplicationCommandData = data
        # TODO: guild

        self.id: Snowflake = Snowflake(self.data["id"])

        self.type: ApplicationCommandTypes
        raw_type = self.data.get("type")
        if isinstance(raw_type, int):
            self.type = ApplicationCommandTypes(raw_type)
        else:
            self.type = ApplicationCommandTypes.CHAT_INPUT

        self.application_id: dt.Snowflake = self.data["application_id"]

        self.guild_id: UnsetOr[Snowflake]
        raw_guild_id = self.data.get("guild_id", Unset)
        if isinstance(raw_guild_id, (int, str)):
            self.guild_id = Snowflake(raw_guild_id)
        else:
            self.guild_id = raw_guild_id

        self.name: str = self.data["name"]
        self.description: UnsetOr[str] = self.data.get("description", Unset)

        self.name_localizations: UnsetOr[t.Optional[dict[Locales, str]]]
        raw_name_localizations = self.data.get("name_localizations", Unset)
        if isinstance(raw_name_localizations, dict):
            self.name_localizations = {
                Locales(n): v for n, v in raw_name_localizations.items()
            }
        else:
            self.name_localizations = raw_name_localizations

        self.description_localizations: UnsetOr[t.Optional[dict[Locales, str]]]
        raw_description_localizations = self.data.get(
            "description_localizations", Unset
        )
        if isinstance(raw_description_localizations, dict):
            self.description_localizations = {
                Locales(n): v for n, v in raw_description_localizations.items()
            }
        else:
            self.description_localizations = raw_description_localizations

        self.options: UnsetOr[list[ApplicationCommandOption]]
        raw_options = self.data.get("options", Unset)
        if isinstance(raw_options, list):
            self.options = [ApplicationCommandOption.from_dict(o) for o in raw_options]
        else:
            self.options = raw_options

        self.default_member_permissions: t.Optional[Permissions]
        raw_default_member_permissions = self.data.get("default_member_permissions")
        if isinstance(raw_default_member_permissions, str):
            self.default_member_permissions = Permissions.from_value(
                int(raw_default_member_permissions)
            )
        else:
            self.default_member_permissions = raw_default_member_permissions

        self.dm_permission: UnsetOr[bool] = self.data.get("dm_permission", Unset)
        self.version: Snowflake = Snowflake(self.data["version"])

    async def edit(
        self,
        *,
        name: UnsetOr[str] = Unset,
        name_localizations: UnsetOr[t.Optional[dict[Locales, str]]] = Unset,
        description: UnsetOr[str] = Unset,
        description_localizations: UnsetOr[t.Optional[dict[Locales, str]]] = Unset,
        options: UnsetOr[list[ApplicationCommandOption]] = Unset,
        default_member_permissions: UnsetOr[t.Optional[Permissions]] = Unset,
        dm_permission: UnsetOr[t.Optional[bool]] = Unset,
    ):
        kwargs: dict[str, t.Any] = {}

        if name is not Unset:
            kwargs["name"] = name

        if name_localizations is not Unset:
            kwargs["name_localizations"] = name_localizations

        if description is not Unset:
            kwargs["description"] = description

        if description_localizations is not Unset:
            kwargs["description_localizations"] = description_localizations

        if options is not Unset:
            kwargs["options"] = [o.to_dict() for o in options]

        if default_member_permissions is not Unset:
            if isinstance(default_member_permissions, Permissions):
                kwargs["default_member_permissions"] = str(
                    default_member_permissions.value
                )
            else:
                kwargs["default_member_permissions"] = default_member_permissions

        if dm_permission is not Unset:
            # TODO: uncomment when guild attribute is added
            # if self.guild is not None:
            #     raise ValueError("dm_permission cannot be set if this application command is set in a guild!")
            kwargs["dm_permission"] = dm_permission

        # TODO: uncomment when guild attribute is added
        # new_cmd_data: dt.ApplicationCommandData
        # if self.guild:
        #     new_cmd_data = t.cast(dt.ApplicationCommandData, await self.bot.http.edit_guild_application_command(self.application_id, self.id, self.guild.id, **kwargs))
        # else:
        new_cmd_data = t.cast(
            dt.ApplicationCommandData,
            await self.bot.http.edit_global_application_command(
                self.application_id, self.id, **kwargs
            ),
        )
        new_cmd = ApplicationCommand(bot=self.bot, data=new_cmd_data)
        # TODO: edit cache
        return new_cmd


# currently, discord_typings doesn't expose application command option choices to the user
@t.final
class ApplicationCommandOptionChoiceData(TypedDict):
    name: str
    name_localizations: NotRequired[t.Optional[dict[dt.Locales, str]]]
    value: t.Union[str, int, float]


@attr.define(kw_only=True)
class ApplicationCommandOptionChoice:
    name: str
    name_localizations: UnsetOr[t.Optional[dict[Locales, str]]] = Unset
    value: t.Union[str, int, float]

    @classmethod
    def from_dict(cls, data: ApplicationCommandOptionChoiceData):
        name_localizations = data.get("name_localizations", Unset)
        if isinstance(name_localizations, dict):
            name_localizations = {Locales(n): v for n, v in name_localizations.items()}

        return cls(
            name=data["name"],
            name_localizations=name_localizations,
            value=data["value"],
        )

    def to_dict(self) -> ApplicationCommandOptionChoiceData:
        data: ApplicationCommandOptionChoiceData = {
            "name": self.name,
            "value": self.value,
        }

        if self.name_localizations is not Unset:
            if isinstance(self.name_localizations, dict):
                data["name_localizations"] = {
                    n.value: v for n, v in self.name_localizations.items()
                }
            else:
                data["name_localizations"] = self.name_localizations

        return data


@attr.define(kw_only=True)
class ApplicationCommandOption:
    type: ApplicationCommandOptionTypes
    name: str
    description: str
    name_localizations: UnsetOr[t.Optional[dict[Locales, str]]] = Unset
    description_localizations: UnsetOr[t.Optional[dict[Locales, str]]] = Unset
    required: bool = False
    choices: UnsetOr[list[ApplicationCommandOptionChoice]] = Unset
    options: UnsetOr[list[ApplicationCommandOption]] = Unset
    # TODO: channel_types
    min_value: UnsetOr[t.Union[int, float]] = Unset
    max_value: UnsetOr[t.Union[int, float]] = Unset
    min_length: UnsetOr[int] = Unset
    max_length: UnsetOr[int] = Unset
    autocomplete: UnsetOr[bool] = Unset

    @classmethod
    def from_dict(cls, data: dt.ApplicationCommandOptionData):
        name_localizations = data.get("name_localizations", Unset)
        if isinstance(name_localizations, dict):
            name_localizations = {Locales(n): v for n, v in name_localizations.items()}

        description_localizations = data.get("description_localizations", Unset)
        if isinstance(description_localizations, dict):
            description_localizations = {
                Locales(n): v for n, v in description_localizations.items()
            }

        choices = data.get("choices", Unset)
        if isinstance(choices, list):
            choices = [ApplicationCommandOptionChoice.from_dict(c) for c in choices]

        processed_options: UnsetOr[list[ApplicationCommandOption]] = Unset
        options = data.get("options", Unset)
        if isinstance(options, list):
            processed_options = [ApplicationCommandOption.from_dict(o) for o in options]

        return cls(
            type=ApplicationCommandOptionTypes(data["type"]),
            name=data["name"],
            description=data["description"],
            required=data.get("required", False),
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            choices=choices,
            options=processed_options,
            min_value=data.get("min_value", Unset),
            max_value=data.get("max_value", Unset),
            min_length=data.get("min_length", Unset),
            max_length=data.get("max_length", Unset),
            autocomplete=data.get("autocomplete", Unset),
        )

    def to_dict(self) -> dt.ApplicationCommandOptionData:
        data: dt.ApplicationCommandOptionData = {
            "type": self.type.value,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.name_localizations is not Unset:
            if isinstance(self.name_localizations, dict):
                data["name_localizations"] = {
                    n.value: v for n, v in self.name_localizations.items()
                }
            else:
                data["name_localizations"] = self.name_localizations

        if self.description_localizations is not Unset:
            if isinstance(self.description_localizations, dict):
                data["description_localizations"] = {
                    n.value: v for n, v in self.description_localizations.items()
                }
            else:
                data["description_localizations"] = self.description_localizations

        if self.choices is not Unset:
            # since discord_typings doesn't make their application command option choice typed dicts available,
            # the two list types are incompatible with each other
            data["choices"] = [c.to_dict() for c in self.choices]  # pyright: ignore

        # the following pyright ignore comments are because certain items are defined in certain typed dicts that
        # are all combined in one big union that makes up dt.ApplicationCommandOptionData
        # TODO: type the data variable accordingly depending on the attributes that are set

        if self.options is not Unset:
            data["options"] = [o.to_dict() for o in self.options]  # pyright: ignore

        if self.min_value is not Unset:
            data["min_value"] = self.min_value  # pyright: ignore

        if self.max_value is not Unset:
            data["max_value"] = self.max_value  # pyright: ignore

        if self.min_length is not Unset:
            data["min_length"] = self.min_length  # pyright: ignore

        if self.max_length is not Unset:
            data["max_length"] = self.max_length  # pyright: ignore

        if self.autocomplete is not Unset:
            data["autocomplete"] = self.autocomplete  # pyright: ignore

        return data
