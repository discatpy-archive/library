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

from typing import Any, Dict, List, Optional, overload

from discord_typings import (
    EmbedAuthorData,
    EmbedData,
    EmbedFieldData,
    EmbedFooterData,
    EmbedImageData,
    EmbedProviderData,
    EmbedThumbnailData,
    EmbedVideoData,
)

from .errors import DisCatPyException

__all__ = (
    "Embed",
    "EmbedAuthorData",
    "EmbedFieldData",
    "EmbedFooterData",
    "EmbedImageData",
    "EmbedProviderData",
    "EmbedThumbnailData",
    "EmbedVideoData",
)


class Embed:
    """
    Represents an embed type. Embeds are to be included with messages
    and nothing else.

    Attributes
    ----------
    title: :type:`str`
        The title of this Embed
    description: :type:`Optional[str]`
        The description of this Embed
    url: :type:`Optional[str]`
        The url of this Embed
    color: :type:`Optional[int]`
        The color of this Embed
    footer: :type:`Optional[EmbedFooterData]`
        The footer of this Embed
    image: :type:`Optional[EmbedImageData]`
        The image of this Embed
    thumbnail: :type:`Optional[EmbedThumbnailData]`
        The thumbnail of this Embed
    video: :type:`Optional[EmbedVideoData]`
        The video of this Embed
    provider: :type:`Optional[EmbedProviderData]`
        The provider of this Embed
    author: :type:`Optional[EmbedAuthorData]`
        The author of this Embed
    fields: :type:`List[EmbedFieldData]`
        The fields of this Embed
    """

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[int] = None,
        footer: Optional[EmbedFooterData] = None,
        image: Optional[EmbedImageData] = None,
        thumbnail: Optional[EmbedThumbnailData] = None,
        video: Optional[EmbedVideoData] = None,
        provider: Optional[EmbedProviderData] = None,
        author: Optional[EmbedAuthorData] = None,
        fields: Optional[List[EmbedFieldData]] = None,
    ):
        self.title = title
        self.description = description
        self.url = url
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields: List[EmbedFieldData] = fields if fields else []

    def _field_size_check(self):
        if len(self.fields) > 25:
            return False

        return True

    @overload
    def add_field(self, /, name: str, value: str, inline: bool = False):
        ...

    @overload
    def add_field(self, field: EmbedFieldData):
        ...

    def add_field(self, *args, **kwargs):
        """
        Adds a new field to this Embed. This function will
        automatically check if there is 25 fields, the maximum
        amount of fields.
        """
        if self._field_size_check():
            if "name" in kwargs and "value" in kwargs and "inline" in kwargs:
                field: EmbedFieldData = EmbedFieldData(
                    name=kwargs.get("name"),
                    value=kwargs.get("value"),
                    inline=kwargs.get("inline"),
                )
                self.fields.append(field)
            elif isinstance(args[0], EmbedFieldData):
                self.fields.append(args[0])
        else:
            raise DisCatPyException("Exceeded the number of embed fields (max 25)")

    def to_dict(self) -> EmbedData:
        ret_dict: EmbedData = EmbedData(
            title=self.title,
            type="rich",
        )

        if self.description is not None:
            ret_dict["description"] = self.description
        if self.url is not None:
            ret_dict["url"] = self.url
        if self.color is not None:
            ret_dict["color"] = self.color
        if self.footer is not None:
            ret_dict["footer"] = self.footer
        if self.image is not None:
            ret_dict["image"] = self.image
        if self.thumbnail is not None:
            ret_dict["thumbnail"] = self.thumbnail
        if self.video is not None:
            ret_dict["video"] = self.video
        # TODO: Provider
        if self.author is not None:
            ret_dict["author"] = self.author
        if len(self.fields) > 0:
            ret_dict["fields"] = [f for f in self.fields]

        return ret_dict
