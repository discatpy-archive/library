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

from typing import Any, Dict, Optional

__all__ = (
    "EmbedFooter",
    "EmbedAttribute",
    "EmbedAuthor",
    "EmbedField",
    "to_embed_footer",
    "to_embed_attribute",
    "to_embed_author",
    "to_embed_field",
)

class EmbedFooter:
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

class EmbedAttribute:
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]

class EmbedAuthor:
    name: str
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

class EmbedField:
    name: str
    value: str
    inline: bool = False

def to_embed_footer(d: Dict[str, Any]):
    text: str = d.get("text")
    icon_url: Optional[str] = d.get("icon_url")
    proxy_icon_url: Optional[str] = d.get("proxy_icon_url")

    embed_foot = EmbedFooter()
    embed_foot.text = text
    embed_foot.icon_url = icon_url
    embed_foot.proxy_icon_url = proxy_icon_url

    return embed_foot

def to_embed_attribute(d: Dict[str, Any]):
    url: str = d.get("url")
    proxy_url: Optional[str] = d.get("proxy_url")
    height: Optional[int] = d.get("height")
    width: Optional[int] = d.get("width")

    embed_attr = EmbedAttribute()
    embed_attr.url = url
    embed_attr.proxy_url = proxy_url
    embed_attr.height = height
    embed_attr.width = width

    return embed_attr

def to_embed_author(d: Dict[str, Any]):
    name: str = d.get("name")
    url: Optional[str] = d.get("url")
    icon_url: Optional[str] = d.get("icon_url")
    proxy_icon_url: Optional[str] = d.get("proxy_icon_url")

    embed_auth = EmbedAuthor()
    embed_auth.name = name
    embed_auth.url = url
    embed_auth.icon_url = icon_url
    embed_auth.proxy_icon_url = proxy_icon_url

    return embed_auth

def to_embed_field(d: Dict[str, Any]):
    name: str = d.get("name")
    value: str = d.get("value")
    inline: bool = d.get("inline", False)

    embed_field = EmbedField()
    embed_field.name = name
    embed_field.value = value
    embed_field.inline = inline

    return embed_field