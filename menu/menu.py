from . import MenuElement
from typing import Dict

ElementId = str
ElementDict = Dict[ElementId, MenuElement]


class Menu:
    def __init__(self, id_: str):
        self._elements: ElementDict = {}
        self._id = id_

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _):
        errormsg = f"<Menu>.id is a read-only attribute"
        raise AttributeError(errormsg)

    @id.deleter
    def id(self):
        errormsg = f"<Menu>.id cannot be deleted without deleting the entire object"
        raise AttributeError(errormsg)

    @property
    def elements(self) -> ElementDict:
        return self._elements

    @elements.setter
    def elements(self, _):
        errormsg = f"<Menu>.elements is a read-only attribute"
        raise AttributeError(errormsg)

    @elements.deleter
    def elements(self):
        for item in self._elements:
            del item
        self._elements: ElementDict = {}

    def get_element_by_id(self, id_: str) -> MenuElement:
        if id_ not in list(self._elements.keys()):
            errormsg = f"No element found with id {id_} in menu {self.id}"
            raise ValueError(errormsg)

        else:
            return self._elements[id_]
