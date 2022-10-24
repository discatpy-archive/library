# SPDX-License-Identifier: MIT
from __future__ import annotations

import typing as t
from collections.abc import Callable, Mapping
from datetime import datetime

import attr
import discord_typings as dt

from .color import Color

T = t.TypeVar("T")
MT = t.TypeVar("MT", bound=Mapping[str, t.Any])

__all__ = (
    "EmbedThumbnail",
    "EmbedImage",
    "EmbedVideo",
    "EmbedProvider",
    "EmbedAuthor",
    "EmbedFooter",
    "EmbedField",
    "Embed",
)


class _EmbedProxyMixin(t.Generic[MT]):
    def to_dict(self) -> MT:
        return t.cast(MT, attr.asdict(self))


@attr.frozen(kw_only=True)
class EmbedAttribute(_EmbedProxyMixin[dt.EmbedThumbnailData]):
    url: str
    proxy_url: t.Optional[str]
    height: t.Optional[int]
    width: t.Optional[int]


EmbedThumbnail = EmbedAttribute
EmbedImage = EmbedAttribute


@attr.frozen(kw_only=True)
class EmbedVideo(_EmbedProxyMixin[dt.EmbedVideoData]):
    url: t.Optional[str]
    proxy_url: t.Optional[str]
    height: t.Optional[int]
    width: t.Optional[int]


@attr.frozen(kw_only=True)
class EmbedProvider(_EmbedProxyMixin[dt.EmbedProviderData]):
    name: t.Optional[str]
    url: t.Optional[str]


@attr.frozen(kw_only=True)
class EmbedAuthor(_EmbedProxyMixin[dt.EmbedAuthorData]):
    name: str
    url: t.Optional[str]
    icon_url: t.Optional[str]
    proxy_icon_url: t.Optional[str]


@attr.frozen(kw_only=True)
class EmbedFooter(_EmbedProxyMixin[dt.EmbedFooterData]):
    text: str
    icon_url: t.Optional[str]
    proxy_icon_url: t.Optional[str]


@attr.frozen(kw_only=True)
class EmbedField(_EmbedProxyMixin[dt.EmbedFieldData]):
    name: str
    value: str
    inline: bool


def _grab_and_convert(
    d: Mapping[str, t.Any], key: str, type_from: type[Mapping[str, t.Any]], type_to: type[T]
) -> t.Optional[T]:
    return type_to(**t.cast(type_from, d.get(key, {}))) if d.get(key) else None


def _make_optional_converter(
    original: Callable[[t.Any], T]
) -> Callable[[t.Optional[t.Any]], t.Optional[T]]:
    def wrapper(val: t.Optional[t.Any]) -> t.Optional[T]:
        if val is None:
            return None
        return original(val)

    return wrapper


@attr.define(kw_only=True)
class Embed:
    title: t.Optional[str] = None
    type: t.Literal["rich", "image", "video", "gifv", "article", "link"] = "rich"
    description: t.Optional[str] = None
    url: t.Optional[str] = None
    timestamp: t.Optional[datetime] = attr.field(
        default=None, converter=_make_optional_converter(datetime.fromisoformat)
    )
    color: t.Optional[Color] = attr.field(
        default=None, converter=_make_optional_converter(Color.from_hex)
    )
    footer: t.Optional[EmbedFooter] = None
    image: t.Optional[EmbedImage] = None
    thumbnail: t.Optional[EmbedThumbnail] = None
    video: t.Optional[EmbedVideo] = None
    provider: t.Optional[EmbedProvider] = None
    author: t.Optional[EmbedAuthor] = None
    fields: list[EmbedField] = attr.field(factory=list)

    @classmethod
    def from_dict(cls, data: dt.EmbedData):
        timestamp = (
            datetime.fromisoformat(data.get("timestamp", "")) if data.get("timestamp") else None
        )
        color = Color.from_hex(int(data.get("color", 0))) if data.get("color") else None
        footer = _grab_and_convert(data, "footer", dt.EmbedFooterData, EmbedFooter)
        image = _grab_and_convert(data, "image", dt.EmbedImageData, EmbedImage)
        thumbnail = _grab_and_convert(data, "thumbnail", dt.EmbedThumbnailData, EmbedThumbnail)
        video = _grab_and_convert(data, "video", dt.EmbedVideoData, EmbedVideo)
        provider = _grab_and_convert(data, "provider", dt.EmbedProviderData, EmbedProvider)
        author = _grab_and_convert(data, "author", dt.EmbedAuthorData, EmbedAuthor)
        fields = (
            [EmbedField(**field) for field in data.get("fields", [])] if data.get("fields") else []
        )

        return cls(
            title=data.get("title"),
            type=data.get("type", "rich"),
            description=data.get("description"),
            url=data.get("url"),
            timestamp=timestamp,
            color=color,
            footer=footer,
            image=image,
            thumbnail=thumbnail,
            video=video,
            provider=provider,
            author=author,
            fields=fields,
        )

    def to_dict(self) -> dt.EmbedData:
        data: dt.EmbedData = {"type": self.type}

        if self.title:
            data["title"] = self.title

        if self.description:
            data["description"] = self.description

        if self.url:
            data["url"] = self.url

        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()

        if self.color:
            data["color"] = self.color.to_hex()

        if self.footer:
            data["footer"] = self.footer.to_dict()

        if self.image:
            data["image"] = self.image.to_dict()

        if self.thumbnail:
            data["thumbnail"] = self.thumbnail.to_dict()

        if self.video:
            data["video"] = self.video.to_dict()

        if self.provider:
            data["provider"] = self.provider.to_dict()

        if self.author:
            data["author"] = self.author.to_dict()

        if self.fields:
            data["fields"] = [field.to_dict() for field in self.fields]

        return data

    def set_footer(
        self, *, text: str, icon_url: t.Optional[str] = None, proxy_icon_url: t.Optional[str] = None
    ) -> None:
        self.footer = EmbedFooter(text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url)

    def set_image(
        self,
        *,
        url: str,
        proxy_url: t.Optional[str] = None,
        height: t.Optional[int] = None,
        width: t.Optional[int] = None,
    ) -> None:
        self.image = EmbedImage(url=url, proxy_url=proxy_url, height=height, width=width)

    def set_thumbnail(
        self,
        *,
        url: str,
        proxy_url: t.Optional[str] = None,
        height: t.Optional[int] = None,
        width: t.Optional[int] = None,
    ) -> None:
        self.thumbnail = EmbedThumbnail(url=url, proxy_url=proxy_url, height=height, width=width)

    def set_video(
        self,
        *,
        url: t.Optional[str] = None,
        proxy_url: t.Optional[str] = None,
        height: t.Optional[int] = None,
        width: t.Optional[int] = None,
    ) -> None:
        self.video = EmbedVideo(url=url, proxy_url=proxy_url, height=height, width=width)

    def set_provider(self, *, name: t.Optional[str] = None, url: t.Optional[str] = None) -> None:
        self.provider = EmbedProvider(name=name, url=url)

    def set_author(
        self,
        *,
        name: str,
        url: t.Optional[str] = None,
        icon_url: t.Optional[str] = None,
        proxy_icon_url: t.Optional[str] = None,
    ) -> None:
        self.author = EmbedAuthor(
            name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )

    def add_field(self, *, name: str, value: str, inline: bool = False) -> None:
        self.fields.append(EmbedField(name=name, value=value, inline=inline))

    def insert_field_at(self, index: int, *, name: str, value: str, inline: bool = False) -> None:
        self.fields.insert(index, EmbedField(name=name, value=value, inline=inline))

    def remove_field_at(self, index: int) -> None:
        del self.fields[index]
