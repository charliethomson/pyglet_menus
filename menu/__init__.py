MENUS: dict = {}

__all__ = ["Menu"]
from .src import *
from .menu import Menu


def get_menu_by_id(id_: str) -> Menu:
    if not id_ in MENUS:
        errormsg = f"No menu with id {id_}"
        raise IndexError(errormsg)

    return MENUS[id_]

