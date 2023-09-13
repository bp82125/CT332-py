from functools import reduce

from Ex11.constants import GRID_SIZE
from Ex11.helper_classes import Tile, Coordinate, Cage, char_to_operator, Operator


class Board:
    """
    @grid: A matrix hold the value of each tile
    @cages: A list of cages in the board
    @possibilities: A matrix which hold the possible values of a tile
    @placed_tile: A list to track the tiles which already used
    """

    def __init__(self):
        self.grid: list[list[Tile]] = [
            [
                Tile(Coordinate(row, col), 0, 0) for col in range(GRID_SIZE)
            ]
            for row in range(GRID_SIZE)
        ]

        self.cages: list[Cage] = []

        self.possibilities: [list[list[list[int]]]] = []
        self.placed_tiles: list[Tile] = []

        self.reset_possibilities()

        # For tracking solving only
        self.iteration_count = 0

    # Check whether a board is completed or not
    @property
    def is_solved(self):
        return len(self.placed_tiles) == GRID_SIZE * GRID_SIZE

    def get_tile_by_coord(self, coord: Coordinate) -> Tile:
        return self.grid[coord.row][coord.col]

    def get_cage_by_coord(self, coord: Coordinate) -> Cage:
        return self.cages[self.get_tile_by_coord(coord).cage_index]

    def get_possible_values_by_coord(self, coord: Coordinate) -> list[int]:
        return self.possibilities[coord.row][coord.col]

    # For printing result
    def print_values(self):
        for row in self.grid:
            print("  |".join([str(row[i].value) for i in range(GRID_SIZE)]))

    # For printing result
    def print_cages(self):
        def get_char_operator(op: Operator):
            for key, value in char_to_operator.items():
                if value == op:
                    return key if key != '.' else ' '

        for row in self.grid:
            print("  |".join(
                [f"{self.cages[row[i].cage_index].goal:2}{get_char_operator(self.cages[row[i].cage_index].operator)}"
                 for i in range(GRID_SIZE)]))

    # Reset the possible values of each tile to [1,2,3,4].
    # Then use the already visited tiles to collapse the possible values of unvisited tiles
    def reset_possibilities(self):
        self.possibilities = [[[n + 1 for n in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for tile in self.placed_tiles:
            self.propagate(tile)

    # For creating cage from file
    def create_cage(self, value: int, char_operator: chr, list_coords: list[Coordinate]):
        operator = char_to_operator.get(char_operator)
        self.cages.append(Cage(value, operator, list_coords))

        for coord in list_coords:
            self.get_tile_by_coord(coord).cage_index = len(self.cages) - 1

        if len(list_coords) == 1:
            self.collapse_tile(list_coords[0], value)

    # Collapse the possible values of all tiles in the the source's col and source's row
    def propagate(self, tile: Tile) -> bool:
        for i in range(GRID_SIZE):
            if tile.value in self.possibilities[tile.coord.row][i] and i != tile.coord.col:
                self.possibilities[tile.coord.row][i].remove(tile.value)
                if len(self.possibilities[tile.coord.row][i]) <= 0:
                    return False

        for i in range(GRID_SIZE):
            if tile.value in self.possibilities[i][tile.coord.col] and i != tile.coord.row:
                self.possibilities[i][tile.coord.col].remove(tile.value)
                if len(self.possibilities[i][tile.coord.col]) <= 0:
                    return False

        return True

    # Assign a value to the tile according to the coordinate
    # Then try to spread the constraints
    # If false, restore the board to the previous state
    def collapse_tile(self, coord: Coordinate, value: int) -> bool:
        tile = self.get_tile_by_coord(coord)
        possible_values = self.get_possible_values_by_coord(coord)
        cage = self.get_cage_by_coord(coord)

        if tile.value != 0:
            return False

        if len(possible_values) <= 0:
            return False

        if value not in possible_values:
            return False

        tile.value = value
        self.placed_tiles.append(tile)
        self.possibilities[coord.row][coord.col] = [value]

        if not self.propagate(tile):
            self.restore_tile(coord)
            return False

        if self.check_if_full_cage(cage) and self.calculate_cage_value(cage) != cage.goal:
            self.restore_tile(coord)
            return False

        return True

    # Remove last added tile from the placed_tiles
    # Restore the value of the tile to default
    # Start propagating again
    def restore_tile(self, coord: Coordinate):
        self.placed_tiles.pop()
        self.get_tile_by_coord(coord).value = 0
        self.reset_possibilities()

    # Return a list of coordinates of unvisited tiles, which have the lowest entropy
    def smallest_possibilities(self) -> list[Coordinate]:
        min_length = GRID_SIZE + 1
        list_coords = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].value == 0:
                    min_length = min(min_length, len(self.possibilities[row][col]))

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if len(self.possibilities[row][col]) == min_length:
                    if self.grid[row][col].value == 0:
                        list_coords.append(Coordinate(row, col))

        return list_coords

    # Helper function to calculate the value of the cage so far
    # If the cage isn't completed, return 0
    # If the operator is NONE, return the goal
    def calculate_cage_value(self, cage: Cage) -> int:
        operator = cage.operator
        list_coords = cage.list_coords

        list_values = [self.get_tile_by_coord(coord).value for coord in list_coords]

        if 0 in list_values:
            return 0

        if operator != Operator.NONE:
            return reduce(operator, list_values)
        else:
            return list_values[0]

    # Helper function to check if a cage is fully filled or not
    def check_if_full_cage(self, cage: Cage) -> bool:
        list_values = [self.get_tile_by_coord(coord).value for coord in cage.list_coords]
        return 0 not in list_values

    def solve(self) -> bool:
        self.iteration_count += 1
        if self.is_solved:
            return True

        least_entropy = self.smallest_possibilities()

        for coord in least_entropy:
            values = self.get_possible_values_by_coord(coord)
            if len(values) <= 0:
                return False

            for value in values:
                if self.collapse_tile(coord, value):
                    if self.solve():
                        return True
                    else:
                        self.restore_tile(coord)

        return False
