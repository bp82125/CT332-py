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

        # For counting how many times did the solve method was recursively called
        self.iteration_count = 0

    def __repr__(self):
        return str(self.grid)

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

    def get_possible_values_by_row_col(self, row: int, col: int) -> list[int]:
        return self.possibilities[row][col]

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
            cage_strings = []
            for i in range(GRID_SIZE):
                goal = self.cages[row[i].cage_index].goal
                operator = get_char_operator(self.cages[row[i].cage_index].operator)
                cell_str = f"{goal}{operator}"
                cage_strings.append(cell_str.ljust(3))

            print(" |".join(cage_strings))

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

    # Collapse the possible values of all tiles in the source's col and source's row
    def propagate(self, tile: Tile) -> bool:
        # Spread constraints in a row
        for col in range(GRID_SIZE):
            current_possible_values = self.get_possible_values_by_row_col(tile.coord.row, col)
            if tile.value in current_possible_values and col != tile.coord.col:
                current_possible_values.remove(tile.value)
                if len(current_possible_values) <= 0:
                    return False

        # Spread constraints in a col
        for row in range(GRID_SIZE):
            current_possible_value = self.get_possible_values_by_row_col(row, tile.coord.col)
            if tile.value in current_possible_value and row != tile.coord.row:
                current_possible_value.remove(tile.value)
                if len(current_possible_value) <= 0:
                    return False

        return True

    # Assign a value to the tile according to the coordinate
    # Then try to spread the constraints
    # If false, restore the board to the previous state
    def collapse_tile(self, coord: Coordinate, value: int) -> bool:
        tile = self.get_tile_by_coord(coord)
        cage = self.get_cage_by_coord(coord)

        tile.value = value
        self.placed_tiles.append(tile)
        self.possibilities[coord.row][coord.col] = [value]

        if not self.propagate(tile):
            return False

        if self.check_if_full_cage(cage) and self.calculate_cage_value(cage) != cage.goal:
            return False

        return True

    # Remove last added tile from the placed_tiles
    # Restore the value of the tile to default
    # Start propagating again
    def restore_tile(self, coord: Coordinate):
        for tile in self.placed_tiles:
            if tile.coord == coord:
                self.placed_tiles.remove(tile)
                self.get_tile_by_coord(coord).value = 0
                self.reset_possibilities()

    # Return the coordinates of unvisited and having the lowest entropy tile
    def smallest_entropy_coord(self) -> Coordinate:
        min_entropy = GRID_SIZE + 1
        min_entropy_coords = []

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col].value == 0:
                    entropy = len(self.get_possible_values_by_row_col(row, col))
                    if entropy < min_entropy:
                        min_entropy = entropy
                        min_entropy_coords = [Coordinate(row, col)]
                    elif entropy == min_entropy:
                        min_entropy_coords.append(Coordinate(row, col))

        if min_entropy_coords:
            return min_entropy_coords[0]

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

    # Solving the KenKen problem with backtracking
    def solve(self) -> bool:
        self.iteration_count += 1
        if self.is_solved:
            return True

        coord = self.smallest_entropy_coord()

        if coord is None:
            return False

        values = self.get_possible_values_by_coord(coord)

        for value in values:
            if self.collapse_tile(coord, value):
                # Collapse successfully
                if self.solve():
                    return True
                # Backtrack to the previous state
            self.restore_tile(coord)
        return False
