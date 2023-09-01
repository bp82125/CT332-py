import math
import random
from copy import deepcopy

from Ex9.tile import Tile, Coordinate


class Board:
    def __init__(self):
        self.base_grid = []
        for i in range(9):
            self.base_grid.append(([Tile(Coordinate(i, j)) for j in range(9)]))

        self.grid = deepcopy(self.base_grid)

    def __repr__(self):
        board_str = ""

        board_str += "-------------------------\n"

        for index, row in enumerate(self.grid):
            board_str += "| {} {} {} | {} {} {} | {} {} {} |\n".format(*row)
            if (index + 1) % 3 == 0:
                board_str += "-------------------------\n"

        return board_str

    def not_solved(self) -> bool:
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].collapsed is False:
                    return True

        return False

    def propagate(self, tile: Tile):
        row = tile.coord.x
        col = tile.coord.y
        group = tile.group
        pick = tile.possibilities[0]

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != tile and self.grid[i][j].collapsed is False:
                    if self.grid[i][j].coord.x == row:
                        if pick in self.grid[i][j].possibilities:
                            self.grid[i][j].possibilities.remove(pick)

                    if self.grid[i][j].coord.y == col:
                        if pick in self.grid[i][j].possibilities:
                            self.grid[i][j].possibilities.remove(pick)

                    if self.grid[i][j].group == group:
                        if pick in self.grid[i][j].possibilities:
                            self.grid[i][j].possibilities.remove(pick)

    def setEntropy(self):
        input_tiles = []

        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value != 0:
                    input_tiles.append(self.grid[i][j])

        if len(input_tiles) > 0:
            for tile in input_tiles:
                value = tile.value
                tile.collapse(value)
                self.propagate(tile)

    def reset(self):
        self.grid = deepcopy(self.base_grid)
        self.setEntropy()

    def check_valid_board(self):
        input_tiles = []

        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value != 0:
                    input_tiles.append(self.grid[i][j])

        for tile in input_tiles:
            if self.check_valid_rows_cols_groups(tile) is False:
                return False

        return True

    def check_valid_rows_cols_groups(self, tile: Tile):
        row = tile.coord.x
        col = tile.coord.y
        group = tile.group
        value = tile.value

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != tile:
                    if (self.grid[i][j].coord.x == row
                            or self.grid[i][j].coord.y == col
                            or self.grid[i][j].group == group):
                        if self.grid[i][j].value == value:
                            return False

        return True

    def wave_function_collapse(self):
        min_options = math.inf
        for i in range(9):
            for j in range(9):
                if not self.grid[i][j].collapsed:
                    min_options = min(min_options, len(self.grid[i][j].possibilities))

        least_entropy_cells: [Tile] = []
        for i in range(9):
            for j in range(9):
                if not self.grid[i][j].collapsed:
                    if len(self.grid[i][j].possibilities) == min_options:
                        least_entropy_cells.append(self.grid[i][j])

        if len(least_entropy_cells) > 0:
            random_tile: Tile = random.choice(least_entropy_cells)

            if len(random_tile.possibilities) == 0:
                return False

            random_tile.collapse()

            self.propagate(random_tile)
            return True

    def solve(self):
        iteration_counts = 0
        attempt_solving = 1
        while self.not_solved():
            success = self.wave_function_collapse()
            if success:
                iteration_counts += 1
            else:
                print("Solving failed. Resetting")
                iteration_counts = 0
                attempt_solving += 1
                self.reset()
        print(f'Iteration counts: {iteration_counts}')
        print(f'Attempt solving: {attempt_solving}')
        print(self)
