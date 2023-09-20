from Ex10.constants import MAX_QUEENS
from Ex10.utils import Coordinate


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(MAX_QUEENS)] for col in range(MAX_QUEENS)]
        self.constraints: list[list[int]] = [[0 for _ in range(MAX_QUEENS)] for col in range(MAX_QUEENS)]
        self.placed_queens: list[Coordinate] = []

        self.iteration_count: int = 0

    def __repr__(self):
        res = ""
        for row in self.grid:
            res += " ".join(["W" if col == 1 else "0" for col in row]) + "\n"

        return res

    def print_board(self):
        print("Board:")
        for row in self.grid:
            print(" ".join(["W" if col == 1 else "0" for col in row]))
        print("\nConstraints:")
        for row in self.constraints:
            print(" ".join([str(col) for col in row]))

    def spread_horizontally_right(self, coord: Coordinate):
        row = coord.row
        col = coord.col

        while col < MAX_QUEENS:
            self.constraints[row][col] = 1
            col += 1

    def spread_upper_right(self, coord: Coordinate):
        row = coord.row
        col = coord.col
        while row >= 0 and col < MAX_QUEENS:
            self.constraints[row][col] = 1
            row -= 1
            col += 1

    #
    def spread_lower_right(self, coord: Coordinate):
        row = coord.row
        col = coord.col
        while row < MAX_QUEENS and col < MAX_QUEENS:
            self.constraints[row][col] = 1
            row += 1
            col += 1

    def spread_constraints_from(self, coord: Coordinate):
        self.spread_horizontally_right(coord)
        self.spread_lower_right(coord)
        self.spread_upper_right(coord)

    def reset_constraints(self):
        self.constraints: list[list[int]] = [[0 for _ in range(MAX_QUEENS)] for col in range(MAX_QUEENS)]
        for coord in self.placed_queens:
            self.spread_constraints_from(coord)

    def check_conflict(self, coord: Coordinate) -> bool:
        if self.constraints[coord.row][coord.col] == 1:
            return True
        return False

    def place_queen(self, coord: Coordinate) -> bool:
        if self.check_conflict(coord):
            return False

        self.grid[coord.row][coord.col] = 1
        self.placed_queens.append(coord)
        self.spread_constraints_from(coord)
        return True

    def remove_queen(self, coord: Coordinate):
        self.placed_queens.pop()
        self.grid[coord.row][coord.col] = 0
        self.reset_constraints()

    def solve(self, col: int):
        self.iteration_count += 1

        if col >= MAX_QUEENS:
            return True

        for row in range(MAX_QUEENS):
            current_coord = Coordinate(row, col)
            if self.place_queen(current_coord):
                if self.solve(col + 1):
                    return True
                else:
                    self.remove_queen(current_coord)
        return False




