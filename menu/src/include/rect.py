from pyglet.graphics import Batch, draw as gl_draw
from pyglet.gl import GL_QUADS
from math import radians as radians_, atan, degrees, sin, cos
from . import Color, validate_hex_str
from pprint import pprint
from typing import Any
from ...colors import SEA_GREEN


class Rect:
    "Interface class for pyglet Rectangles"

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        rotation: float = 0.0,
        radians: bool = False,
        color: Any = SEA_GREEN,
        batch: Batch = None,
        draw: bool = True,
        id_: str = "Rectangle",
    ):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.angle = rotation if radians else radians_(rotation)
        self.color = self._get_color(color)
        self.coords = self.get_coords()
        self.batch = batch

        if draw:
            self.draw()

    def __repr__(self):
        return f"Rect:\
            \n\tpos: ({self.x}, {self.y});\
            \n\tw, h: {self.w}, {self.h};\
            \n\tangle: {self.angle};\
            \n\tcolor:\
            \n\t\n\t{self.color};\
            \n\tcoords:\
            \n\t\n\t{self.coords};"

    def _get_color(self, color):
        "format the color of the rectangle"
        assert isinstance(
            color, (Color, tuple, list, str, int)
        ), "<Rect>.color must be type Color, iterable, grayscale int, or hex string"

        if isinstance(color, Color):
            return color
        elif isinstance(color, str):
            if not validate_hex_str(color):
                errormsg = f"{color} is not a valid hex string"
                raise ValueError(errormsg)
            assert (
                len(color) == 3
            ), f"Length for color incorrect; expected 3, recieved {len(color)}"
            return Color(*color)

        else:
            # For the rectangle, we need 12 values, i.e. a tuple len 12
            # (3 RGB values per corner, 4 corners, 12 values)
            if isinstance(color, int):
                return Color(color, color, color)
            elif len(color) == 3:
                return Color(*color)

    def get_coords(self):
        "get the coordinates of the rectangle's vertices"

        def get_corner(x, y, angle, x_offset, y_offset):
            new_x = x + (x_offset * cos(angle)) - (y_offset * sin(angle))
            new_y = y + (x_offset * sin(angle)) + (y_offset * cos(angle))
            return (new_x, new_y)

        def fix_list(list_to_fix):
            out = []
            for sub_list in list_to_fix:
                [out.append(item) for item in sub_list]

            return out

        offsets = [
            [-self.w // 2, self.h // 2],
            [-self.w // 2, -self.h // 2],
            [self.w // 2, -self.h // 2],
            [self.w // 2, self.h // 2],
        ]

        return fix_list(
            [get_corner(self.x, self.y, self.angle, *offset) for offset in offsets]
        )

    def draw(self):
        "draw the rectangle"

        for coord in self.coords:
            if isinstance(coord, int):
                coord = float(coord)
            elif not isinstance(coord, float):
                raise TypeError(f"coordinate '{coord}' type incorrect ({type(coord)})")

        # if there's no batch, draw the shape, if there is a batch, add the shape to the batch
        if not self.batch:
            gl_draw(
                4,
                GL_QUADS,
                ("v2f", self.coords),
                ("c3B", self.color.get_pyglet_colors(4)),
            )
            # pprint(rectargs)
        else:
            self.batch.add(
                4,
                GL_QUADS,
                None,
                ("v2f", self.coords),
                ("c3B", self.color.get_pyglet_colors(4)),
            )

