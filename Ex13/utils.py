from Ex13.constants import State
from Ex13.graph import Graph


def read_graph_from_file(input_file: str) -> Graph:
    graph = Graph()
    with open('input.txt', 'r') as file:
        for line in file:
            state_abbreviations = line.strip().split()
            state_list = [State[abbreviation] for abbreviation in state_abbreviations]

            state_name = state_list[0]
            neighbors = state_list[1:]

            graph.add_vertex(state_name, neighbors)

    return graph




