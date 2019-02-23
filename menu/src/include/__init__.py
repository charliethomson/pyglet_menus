from typing import Tuple, Union


def col_comps_from_hex(hex_: str, alpha: bool = False) -> Tuple[int, int, int, int]:
    """Returns the three int tuple with the r, g, b values from the `hex_` hex string"""
    if not isinstance(hex_, str):
        if isinstance(hex_, int):
            hex_ = str(hex(hex_))
    if hex_.startswith("0x"):
        hex_ = hex_[2:]
    if not len(hex_) == 6:
        if alpha:
            hex_ = hex_[:8]
        else:
            hex_ = hex_[:6]

    r = int(hex_[0:2], 16)
    g = int(hex_[2:4], 16)
    b = int(hex_[4:6], 16)
    a = int(hex_[6:8], 16) if alpha else 255
    return (r, g, b, a)


def remove_0x(string: str) -> str:
    if not string.startswith("0x"):
        return string
    return string.split("0x")[1]


def validate_hex_str(hex_: str) -> bool:
    if not isinstance(hex_, str):
        return False
    elif len(hex_) != 6:
        if len(hex_) < 6:
            hex_ = hex_.rjust(6, "0")
        elif len(hex_) > 6:
            hex_ = hex_[:6]
    hex_ = remove_0x(hex_)
    return all([ord(char) in range(97, 103) for char in hex_.lower() if char.isalpha()])
    # for char in hex_.lower():
    #     if char.isalpha():
    #         # If the character's ascii code is not in the right range, return False
    #         if not ord(char) in range(97, 103):
    #             return False
    #
    # return True


Number = Union[int, float]


def remap(
    value: Number, old_min: Number, old_max: Number, new_min: Number, new_max: Number
) -> float:
    return ((value - old_min) * (new_max - new_min)) / (old_max - old_min)


def hex_from_float(f: float) -> str:
    return hex(int(remap(f, 0.0, 1.0, 0, 255)))


from .color import Color
from .rect import Rect

__all__ = ["Color", "Rect"]
