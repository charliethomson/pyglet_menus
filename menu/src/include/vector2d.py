class Vector2D:
    def __init__(self, x: int = 0, y: int = 0):
        self._x, self._y = x, y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y) -> None:
        self._y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        return Vector2D(self.x / other.x, self.y / other.y)

    def __fdiv__(self, other):
        return Vector2D(self.x // other.x, self.y // other.y)

