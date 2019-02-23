from numpy import mean  # type: ignore
from . import remove_0x, col_comps_from_hex, hex_from_float


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self._r = r % 255
        self._g = g % 255
        self._b = b % 255
        self._a = a % 255

    def __iter__(self):
        for comp in (self._r, self._g, self._b, self._a):
            yield comp

    def __eq__(self, other) -> bool:
        return all(
            (
                self._r == other._r,
                self._g == other._g,
                self._b == other._b,
                self._a == other._a,
            )
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def __lt__(self, other) -> bool:
        return all(
            (
                self._r < other._r,
                self._g < other._g,
                self._b < other._b,
                self._a < other._a,
            )
        )

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return all(
            (
                self._r > other._r,
                self._g > other._g,
                self._b > other._b,
                self._a > other._a,
            )
        )

    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __repr__(self):
        return f"({self._r}, {self._g}, {self._b})"

    def __getitem__(self, item):
        return self.get(item)

    @classmethod
    def blend(self, col1, col2):
        """
        Returns a new color as the average of self and other
        """
        r = int(round(mean((col1.r, col2.r))))
        g = int(round(mean((col1.g, col2.g))))
        b = int(round(mean((col1.b, col2.b))))
        a = int(round(mean((col1.a, col2.a))))
        return Color(r, g, b, a)

    @classmethod
    def from_hex(cls, hex_: str):
        """
        Returns a color object with the hex value `hex_`
        """
        if isinstance(hex_, int):
            hex_ = str(hex(hex_))
        if hex_.startswith("0x"):
            hex_ = hex_[2:]
        r, g, b, a = col_comps_from_hex(hex_)
        return Color(r, g, b, a)

    @classmethod
    def from_floats(cls, r: float, g: float, b: float, a: float = 1.0):

        r_hex = hex_from_float(r)
        g_hex = hex_from_float(g)
        b_hex = hex_from_float(b)
        a_hex = hex_from_float(a)

        return Color.from_hex(r_hex + g_hex + b_hex + a_hex)

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, r: int) -> None:
        self._r = r

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, g: int) -> None:
        self._g = g

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, b: int) -> None:
        self._b = b

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, a: int) -> None:
        self._a = a

    def get(self, item, hex_: bool = False, prefix: bool = True) -> str:
        if isinstance(item, slice):
            errormsg = "Colors do not support slices. If you want more than one value,"
            errormsg += " index with a string with the components you're looking for"
            raise IndexError(errormsg)

        elif isinstance(item, int):
            if not 0 <= item <= 3:
                errormsg = f"Index {item} out of bounds"
                raise IndexError(errormsg)
            val = [self._r, self._g, self._b, self._a][item]
            if not hex_:
                return str(val)
            else:
                return hex(val)

        elif isinstance(item, str):
            wrong = []
            for char in item:
                if not char.lower() in ["r", "g", "b", "a"]:
                    wrong.append(char)
            if len(wrong) != 0:
                # If I didn't want the items that weren't supposed to be there, i could do this
                # if not all([char.lower() in ("r", "g", "b") for char in item]):
                # to check if they're all correct
                errormsg = f"Encountered unexpected color {'component' if len(wrong) == 1 else 'components'} {', '. join(wrong)}"
                raise IndexError(errormsg)

            data = [] if not hex_ else [] if not prefix else ["0x"]
            for char in item:
                if char.lower() == "r":
                    val = self._r
                elif char.lower() == "g":
                    val = self._g
                elif char.lower() == "b":
                    val = self._b
                elif char.lower() == "a":
                    val = self._a
                data.append(remove_0x(hex(val)) if hex_ else str(val))
            sep = "" if hex_ else ", "
            ret = sep.join(data)
            return ret
        else:
            errormsg = f"Unable to get item from {item}. Type mismatch {type(item)} not {int} or {str}"
            raise TypeError(errormsg)

    def get_pyglet_colors(self, point_count: int) -> list:
        return [self._r, self._g, self._b] * point_count

    def to_rgba(self) -> list:
        return [i for i in self]

    def to_hex(self, prefix: bool = False, alpha: bool = False) -> str:

        r = remove_0x(hex(self._r))
        g = remove_0x(hex(self._g))
        b = remove_0x(hex(self._b))
        a = remove_0x(hex(self._a))

        return (
            ("0x" if prefix else "") + r.upper() + g.upper() + b.upper() + (a.upper() if alpha else "")
        )

