from Ex13.constants import State, Color
from Ex13.graph import Graph
from Ex13.utils import read_graph_from_file

graph = read_graph_from_file("input.txt")

if graph.solve():
    print(f'Iteration count: {graph.iteration_count}')
    graph.print_all_possible_values()
else:
    print("Cannot solve")