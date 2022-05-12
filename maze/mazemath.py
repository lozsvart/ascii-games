from enum import Enum

class RelativeDirection(Enum):
    FRONT = 0
    LEFT = 1
    BACK = 2
    RIGHT = 3

class Coord:
    def __init__(self, x, y):
        self.coords = (x, y)

    def __add__(self, other):
        x0, y0 = self.coords
        x1, y1 = other.coords
        return Coord(x0+x1, y0+y1)

    def __sub__(self, other):
        x0, y0 = self.coords
        x1, y1 = other.coords
        return Coord(x0-x1, y0-y1)

    def __pow__(self, relative_direction):
        x, y = self.coords
        if relative_direction == RelativeDirection.FRONT:
            return self
        if relative_direction == RelativeDirection.LEFT:
            return Coord(-y, x)
        if relative_direction == RelativeDirection.BACK:
            return Coord(-x, -y)
        if relative_direction == RelativeDirection.RIGHT:
            return Coord(y, -x)

    def size(self):
        return max(abs(self.coords[0], self.coords[1]))

    def dist(self, other):
        return (self-other).size()

    def __str__(self):
        return f"({self.coords[0]}, {self.coords[1]})"


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 3
    EAST = 4
