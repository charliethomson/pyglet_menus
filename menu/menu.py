from . import MenuElement, MENUS
from typing import Dict, Type
from .src.include import Vector2D
from pyglet.graphics import Batch
from logging import RootLogger, INFO, ERROR

ElementId = str
ElementDict = Dict[ElementId, MenuElement]


class Menu:
    def __init__(self, id_: str, batch: Batch = None, logger: RootLogger = None):
        self._elements: ElementDict = {}
        self._id = id_
        self._mouse_pos = Vector2D()
        self._batch = batch if batch is not None else Batch()
        self._logger = logger
        MENUS[self._id] = self

    def _log(self, lvl, msg):
        if self._logger:
            self._logger.log(lvl, msg)

    @property
    def mouse_pos(self) -> Vector2D:
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, mouse_pos: Vector2D) -> None:
        if not isinstance(mouse_pos, Vector2D):
            errormsg = f"mouse_pos type mismatch: {type(mouse_pos)} != {Vector2D}"
            raise TypeError(errormsg)

        self._mouse_pos = mouse_pos

    @mouse_pos.deleter
    def mouse_pos(self):
        errormsg = (
            f"<Menu>.mouse_pos cannot be deleted without deleting the entire object"
        )
        self._log
        raise AttributeError(errormsg)

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
    def elements(self) -> dict:
        return dict.copy(self._elements)

    @elements.setter
    def elements(self, _):
        errormsg = f"<Menu>.elements is a read-only attribute"
        raise AttributeError(errormsg)

    @elements.deleter
    def elements(self):
        for item in self._elements:
            del item
        self._elements: ElementDict = {}
        del self._batch
        self._batch = Batch()

    def add_element(self, element: Type[MenuElement]) -> None:
        if not isinstance(element, MenuElement):
            errormsg = f"Unable to add element of type {type(element)} to {self._id}"
            raise TypeError(errormsg)
        elif element.id in self._elements:
            errormsg = f"Element with id {element.id} already in {self._id}"
            raise KeyError(errormsg)

        element.update_data(_batch=self._batch)

        self._log(
            INFO, f"Adding element with id {element.id} to menu with id {self.id}"
        )

        self._elements[element.id] = element

    def get_element_by_id(self, id_: str) -> MenuElement:
        if id_ not in list(self._elements.keys()):
            errormsg = f"No element found with id {id_} in menu {self.id}"
            raise ValueError(errormsg)

        else:
            return self._elements[id_]

    def on_mouse_motion(self, x, y):
        self.mouse_pos = Vector2D(x, y)

    def on_mouse_press(self, x, y, button, mod):
        self.mouse_pos = Vector2D(x, y)

        for element in list(self._elements.values()):
            if element.contains(self.mouse_pos):
                element.on_click()

    def draw(self):
        self._batch.draw()

    @classmethod
    def from_file(cls, filename: str):
        from yaml import load as yml_load

        with open(filename, "r") as file_:
            yml_str = file_.read()

        yml_d = yml_load(yml_str)

        if not "id" in yml_d and "elements" in yml_d:
            missing = ", ".join([i for i in ["id", "elements"] if i not in yml_d])
            errormsg = f"Missing attribute{'s ' + missing if ',' in missing else ' '}. Unable to create menu object from file {filename}"
            raise AttributeError(errormsg)

        menu = cls(yml_d["id"])

        for item in yml_d["elements"]:
            type_, data = yml_d["elements"][item]
            menu.add_element(type_._from_attribs(data))
        
        

    def save_to_file(self, filename: str) -> None:
        from yaml import dump as yml_dump

        def get_elements() -> dict:
            o = {}
            for num, elem in enumerate(list(self._elements.values())):
                o[num] = elem.get_data()
            return o

        data = {"id": self._id, "elements": get_elements()}

        with open(filename, "w") as file_:
            file_.write(yml_dump(data))
