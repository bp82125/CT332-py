from Ex10.board import Board
from Ex10.utils import Coordinate

board = Board()
board.iteration_count = 0

if board.solve(0):
    print(f'Iteration count: {board.iteration_count}')
    board.print_board()
else:
    print("Can't solve")

