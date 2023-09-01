from copy import deepcopy

from board import Board

if __name__ == "__main__":
    board = Board()

    with open("input.txt", 'r') as file:
        for row_idx, line in enumerate(file):
            row = [int(x) for x in line.split()]
            for col_idx, value in enumerate(row):
                if value != 0:
                    board.grid[row_idx][col_idx].collapse(value)
        board.setEntropy()

    print(board)
    board.solve()
