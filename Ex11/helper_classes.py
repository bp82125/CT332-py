from dataclasses import dataclass
from enum import Enum

from Ex11.constants import GRID_SIZE


@dataclass
class Coordinate:
    row: int
    col: int

    def __repr__(self):
        return f'({self.row}, {self.col})'


@dataclass
class Tile:
    coord: Coordinate
    value: int
    cage_index: int

    def __repr__(self):
        return str(self.value)


class Operator(Enum):
    ADD = lambda x, y: x + y
    SUBTRACT = lambda x, y: max(x, y) - min(x, y)
    MULTIPLY = lambda x, y: x * y
    DIVIDE = lambda x, y: max(x, y) / min(x, y) if min(x, y) != 0 else None
    NONE = lambda x, y: x


@dataclass
class Cage:
    goal: int
    operator: Operator
    list_coords: list[Coordinate]


# Mapping the character from file into the equivalent lambda expression
char_to_operator = {
    '+': Operator.ADD,
    '-': Operator.SUBTRACT,
    '*': Operator.MULTIPLY,
    '/': Operator.DIVIDE,
    '.': Operator.NONE
}
