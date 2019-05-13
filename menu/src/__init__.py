from .menu_element import MenuElement
from .button import Button
from .include import Color, Rect
from .menu import Menu
__all__ = ["MenuElement", "Color", "Button", "Menu"]

MENUS: dict = {}


def get_menu_by_id(id_: str):
    if not id_ in MENUS:
        errormsg = f"No menu with id {id_}"
        raise IndexError(errormsg)

    return MENUS[id_]


