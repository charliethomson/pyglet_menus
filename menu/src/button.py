from typing import Union, Callable, Tuple, Iterable
from .include import Color, Vector2D, Rect
from ..colors import WHITE, DARK_GRAY
from .menu_element import MenuElement
from pyglet.text import Label
from pyglet.graphics import Batch
from logging import RootLogger, DEBUG, ERROR, INFO


class Button(MenuElement):
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        id_: str,
        text: str = "",
        text_dpi: int = 96,
        text_align: str = "center",
        anchor_x: str = "center",
        anchor_y: str = "center",
        text_color: Color = WHITE,
        font: str = "arial",
        font_size: int = 12,
        background: bool = True,
        background_color: Color = DARK_GRAY,
        visible: bool = True,
        clickable: bool = True,
        on_click: Tuple[Callable, Iterable] = None,
        logger: RootLogger = None,
    ):
        super().__init__(id_, logger=logger)

        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._id = id_
        self._text = text
        self._text_align = text_align
        self._text_anchor_x = anchor_x
        self._text_anchor_y = anchor_y
        self._text_color = text_color
        self._font = font
        self._font_size = font_size
        self._background = background
        self._background_color = background_color
        self._visible = visible
        self._clickable = clickable
        self._on_click = on_click
        self._batch = None

        self._label_data: dict = {
            "text": text,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "anchor_x": anchor_x,
            "anchor_y": anchor_y,
            "font_name": font,
            "font_size": font_size,
            "dpi": text_dpi,
            "color": text_color.get_colors(1, mode="c4B"),
            "align": text_align,
            # "batch": self._batch,
        }

        self._background_box_data: dict = {
            "x": self._x,
            "y": self._y,
            "w": self._w,
            "h": self._h,
            "color": self._background_color,
            "draw": False,
            "id_": f"{self.id} Background",
            # "batch": self._batch,
        }

        self._background_box = Rect(**self._background_box_data)
        self._label = Label(**self._label_data)

    @property
    def x(self) -> int:
        self._log(
            INFO,
            f"<Button>.x get method called on Button with id {self._id}, returned {self._x}",
        )
        return self._x

    @x.setter
    def x(self, x) -> None:
        self._log(
            INFO,
            f"<Button>.x set method called on Button with id {self._id}, changed self._x: {self._x} -> {x}",
        )
        self._x = x

    @property
    def y(self) -> int:
        self._log(
            INFO,
            f"<Button>.y get method called on Button with id {self._id}, returned {self._y}",
        )
        return self._y

    @y.setter
    def y(self, y) -> None:
        self._log(
            INFO,
            f"<Button>.y set method called on Button with id {self._id}, changed self._y: {self._y} -> {y}",
        )
        self._y = y

    @property
    def w(self) -> int:
        self._log(
            INFO,
            f"<Button>.w get method called on Button with id {self._id}, returned {self._w}",
        )
        return self._w

    @w.setter
    def w(self, w) -> None:
        self._log(
            INFO,
            f"<Button>.w set method called on Button with id {self._id}, changed self._w: {self._w} -> {w}",
        )
        self._w = w

    @property
    def h(self) -> int:
        self._log(
            INFO,
            f"<Button>.h get method called on Button with id {self._id}, returned {self._h}",
        )
        return self._h

    @h.setter
    def h(self, h) -> None:
        self._log(
            INFO,
            f"<Button>.h set method called on Button with id {self._id}, changed self._h: {self._h} -> {h}",
        )
        self._h = h

    @classmethod
    def _from_attribs(cls, d: dict):
        c = cls(0, 0, 0, 0, "")
        c.__dict__ = d
        return c 

    def update_data(
        self, refresh_label: bool = True, refresh_background: bool = True, **items
    ):
        for k, v in items:
            
            if k in self._label_data or k in self._background_box_data:
                if k in self._label_data:
                    self._log(
                        INFO,
                        f"changed Button with id value {self._id} label data value {k}: {self._label_data[k]} -> {v}; Forcing a refresh of label data",
                    )
                    self._label_data[k] = v
                    refresh_label = True
                if k in self._background_box_data:
                    self._log(
                        INFO, 
                        f"changed Button with id value {self._id} background data value {k}: {self._background_box_data[k]} -> {v}; Forcing a refresh of background data",
                    )
                    self._background_box_data[k] = v
                    refresh_background = True
            else:
                res = super().update_data((k, v))
                if res.is_err():
                    errormsg = f"Failed to update item {k} to {v} on Button with id {self.id} -> {res.err}"
                    self._log(ERROR, errormsg)
                    raise KeyError(errormsg)

        if refresh_label:
            self._log(INFO, f"Refreshing label data")
            self._label = Label(**self._label_data)
        if refresh_background:
            self._log(INFO, f"Refreshing background data")
            self._background_box = Rect(**self._background_box_data)


    def contains(self, point: Vector2D) -> bool:
        self._log(INFO, f"<Button>.contains called on point {point}")
        return all(
            [
                self.x - self.w // 2 < point.x < self.x + self.w // 2,
                self.y - self.h // 2 < point.y < self.y + self.h // 2,
            ]
        )

    def draw(self) -> None:
        self._log(DEBUG, f"<Button>.draw called on button {self.id},")
        if self._visible:
            if not isinstance(self._batch, Batch):
                if self._background:
                    Rect(
                        self._x,
                        self._y,
                        self._w,
                        self._h,
                        color=self._background_color.get_colors(4, mode="c3B"),
                        draw=True,
                        id_=f"{self.id} Background",
                    )
                self._label.draw()

    def on_click(self, func: Callable = None, args: Iterable = []) -> None:
        if not self._clickable:
            self._log(DEBUG, f"Button {self.id} clicked; labeled unclickable")
        else:
            if self._on_click:
                func_, args_ = self._on_click
                func_(*args_)
            elif func:
                func(*args)
            else:
                errormsg = f"Button {self.id} clicked with no function to call"
                self._log(ERROR, errormsg)
                raise Exception(errormsg)

    def get_data(self) -> Tuple[type, dict]:
        return (
            Button,
            {
                "x": self._x,
                "y": self._y,
                "w": self._w,
                "h": self._h,
                "background": self._background,
                "clickable": self._clickable,
                "visible": self._visible,
                "label_data": self._label_data,
                "background_box_data": self._background_box_data,
                "on_click": self._on_click,
            },
        )

