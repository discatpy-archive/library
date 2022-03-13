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

from typing import Any, Dict, Optional, List

from .types.embed import *
from .abs import APIType

__all__ = (
    "Embed",
)

def _footer_to_dict(footer: EmbedFooter) -> Dict[str, Any]:
    ret_dict: Dict[str, Any] = {
        "text": footer.text
    }

    if footer.icon_url is not None:
        ret_dict["icon_url"] = footer.icon_url
    if footer.proxy_icon_url is not None:
        ret_dict["proxy_icon_url"] = footer.proxy_icon_url

    return ret_dict

def _attrib_to_dict(attrib: EmbedAttribute) -> Dict[str, Any]:
    ret_dict: Dict[str, Any] = {
        "url": attrib.url
    }

    if attrib.proxy_url is not None:
        ret_dict["proxy_url"] = attrib.proxy_url
    if attrib.height is not None:
        ret_dict["height"] = attrib.height
    if attrib.width is not None:
        ret_dict["width"] = attrib.width

    return ret_dict

def _author_to_dict(author: EmbedAuthor) -> Dict[str, Any]:
    ret_dict: Dict[str, Any] = {
        "name": author.name
    }

    if author.url is not None:
        ret_dict["url"] = author.url
    if author.icon_url is not None:
        ret_dict["icon_url"] = author.icon_url
    if author.proxy_icon_url is not None:
        ret_dict["proxy_icon_url"] = author.proxy_icon_url

    return ret_dict

class Embed(APIType):
    def __init__(
        self, 
        title: str, 
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[int] = None,
        footer: Optional[EmbedFooter] = None,
        image: Optional[EmbedAttribute] = None,
        thumbnail: Optional[EmbedAttribute] = None,
        video: Optional[EmbedAttribute] = None,
        # TODO: Provider
        author: Optional[EmbedAuthor] = None,
        fields: Optional[List[EmbedField]] = None
    ):
        self.title = title
        self.description = description
        self.url = url
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.author = author
        self.fields: List[EmbedField] = fields if fields else []

    def add_field(self, name: str, value: str, inline: bool = False):
        field: EmbedField = EmbedField()
        field.name = name
        field.value = value
        field.inline = inline

        self.fields.append(field)
        # TODO: Check if we haven't exceeded the limit of fields

    def to_dict(self) -> Dict[str, Any]:
        ret_dict: Dict[str, Any] = {
            "title": self.title
        }

        if self.description is not None:
            ret_dict["description"] = self.description
        if self.url is not None:
            ret_dict["url"] = self.url
        if self.color is not None:
            ret_dict["color"] = self.color
        if self.footer is not None:
            ret_dict["footer"] = _footer_to_dict(self.footer)
        if self.image is not None:
            ret_dict["image"] = _attrib_to_dict(self.image)
        if self.thumbnail is not None:
            ret_dict["thumbnail"] = _attrib_to_dict(self.thumbnail)
        if self.video is not None:
            ret_dict["video"] = _attrib_to_dict(self.video)
        # TODO: Provider
        if self.author is not None:
            ret_dict["author"] = _author_to_dict(self.author)
        # TODO: Fields

        return ret_dict
