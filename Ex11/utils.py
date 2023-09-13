from Ex11.board import Board
from Ex11.helper_classes import Coordinate


# Function to read cages from file with the following format:
# "goal, operator, number_of_coordinates, coordinate.row1, coordinate.col1,..."
def read_cage_from_file(file_path: str):
    board = Board()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            value = int(parts[0])
            operator = parts[1]
            num_coordinates = int(parts[2])

            coordinates = [Coordinate(int(parts[i]), int(parts[i + 1])) for i in range(3, 3 + 2 * num_coordinates, 2)]

            board.create_cage(value, operator, coordinates)

    return board

