from utils import read_cage_from_file

board = read_cage_from_file("input_cage3.txt")
board.iteration_count = 0

if board.solve():
    print(f'Iteration count: {board.iteration_count}')

    print("\nKenKen board:")
    board.print_values()

    print("\nCages board:")
    board.print_cages()
else:
    print("Can't solve")
    print(board)
