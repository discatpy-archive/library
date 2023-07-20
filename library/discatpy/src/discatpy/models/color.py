# SPDX-License-Identifier: MIT
from __future__ import annotations

from functools import partial

import attr

__all__ = ("Color", "Colour")


def color_value_validator(instance: Color, attribute: attr.Attribute[int], value: int):
    if value < 0 or value > 255:
        raise ValueError(f"{attribute.name} must be in-between 0 and 255 (inclusive)!")


hex_int: partial[int] = partial(int, base=16)


@attr.define(kw_only=True)
class Color:
    red: int = attr.field(validator=color_value_validator)
    green: int = attr.field(validator=color_value_validator)
    blue: int = attr.field(validator=color_value_validator)

    @classmethod
    def from_hex(cls, hex_code: int):
        actual_hex_code = hex(hex_code).lstrip("0x")
        if len(actual_hex_code) != 6:
            raise ValueError(f"Invalid hex code {actual_hex_code}!")

        red_value = hex_int(actual_hex_code[:2])
        green_value = hex_int(actual_hex_code[:4][2:])
        blue_value = hex_int(actual_hex_code[4:])

        return cls(red=red_value, green=green_value, blue=blue_value)

    def to_hex(self) -> int:
        def _decimal_to_hex(i: int) -> str:
            return hex(i).lstrip("0x")

        hex_code = (
            _decimal_to_hex(self.red)
            + _decimal_to_hex(self.green)
            + _decimal_to_hex(self.blue)
        )
        return hex_int(hex_code)


Colour = Color
