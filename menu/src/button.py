from typing import Union, Callable, Tuple, Iterable
from . import Color, MenuElement
from ..colors import WHITE, DARK_GRAY


class Button(MenuElement):
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        id_: str,
        text: str = None,
        text_align: Union[int, str] = "center",
        text_color: Color = WHITE,
        text_size: int = 12,
        background: bool = True,
        background_color: Color = DARK_GRAY,
        visable: bool = True,
        clickable: bool = True,
        on_click: Tuple[Callable, Iterable] = None,
    ):
        """
        Button

        Args:
            x, y: center position of the button
            w, h: width, height of the button
            id_: the button's ID
        Kwargs:
            text:
            text_align : int / str; def 'center' : Where to anchor the text
            text_color : Color; def WHITE : The color of the text
            text_size  : int, 12 : The size (in pt) of the text
            background : 
            background_color
            visable: bool : Whether or not the button can be seen
            clickable: bool : Whether or not the button can be pressed
            on_click: (func, *args) : func(*args) gets executed when the button is pressed if the button is clickable
        """
        super().__init__(id_)

    def draw(self) -> None:
        pass

    def on_click(self):
        pass
