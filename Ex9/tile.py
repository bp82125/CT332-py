import random
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


class Tile:
    def __init__(self, coord: Coordinate, value: int = 0):
        self.coord = coord
        self.value = value
        self.group = self.coord.y // 3 + (self.coord.x // 3) * 3

        self.collapsed = False
        self.possibilities = [i + 1 for i in range(9)]

    def __repr__(self):
        return str(self.value)

    @property
    def entropy(self):
        return len(self.possibilities)

    def collapse(self, value=None):
        self.collapsed = True

        if value is None:
            option = random.choice(self.possibilities)
        else:
            option = value

        self.value = option
        self.possibilities = [option]
