from dataclasses import dataclass

from Ex13.constants import State, Color


@dataclass
class Vertex:
    state: State
    neighbors: list[State]
    color: Color
    possible_colors: list[Color]

    def __repr__(self) -> str:
        res = ""
        res += "State: " + str(self.state.value) + "\n"
        res += "Neighbors: " + ", ".join([neighbor.value for neighbor in self.neighbors]) + "\n"
        res += "Color: " + str(self.color.value) + "\n"
        return res


class Graph:
    def __init__(self):
        self.vertices: list[Vertex] = []

        # For colorizing
        self.visited_states: list[State] = []

        # For debugging
        self.iteration_count: int = 0

        self.reset_possible_values()

    def add_vertex(self, state: State, neighbors: list[State], color: Color = Color.NONE,
                   possible_colors: list[Color] = None):
        new_vertex = Vertex(
            state=state,
            neighbors=neighbors,
            color=color,
            possible_colors=possible_colors if possible_colors is not None else [Color.RED, Color.GREEN, Color.BLUE]
        )
        self.vertices.append(new_vertex)

    def get_vertex_by_state(self, state: State) -> Vertex:
        for vertex in self.vertices:
            if vertex.state == state:
                return vertex

    def print_all_vertices(self):
        for vertex in self.vertices:
            print(vertex)

    def print_all_possible_values(self):
        for vertex in self.vertices:
            possibilities = [color.value for color in vertex.possible_colors]
            print(f"{vertex.state.value}: " + ", ".join(possibilities))
        print()

    def get_smallest_entropy_vertex(self) -> Vertex:
        min_entropy = len(Color)
        min_entropy_vertices = []
        for vertex in self.vertices:
            if vertex.state not in self.visited_states:
                current_entropy = len(vertex.possible_colors)
                if current_entropy < min_entropy:
                    min_entropy = current_entropy
                    min_entropy_vertices = [vertex]
                elif current_entropy == min_entropy:
                    min_entropy_vertices.append(vertex)

        if min_entropy_vertices:
            return min_entropy_vertices[0]

    def reset_possible_values(self):
        for vertex in self.vertices:
            vertex.possible_colors = [Color.RED, Color.GREEN, Color.BLUE]

        for state in self.visited_states:
            vertex = self.get_vertex_by_state(state)
            self.propagate(vertex)

    def propagate(self, vertex: Vertex) -> bool:
        neighbors = vertex.neighbors

        for neighbor in neighbors:
            neighbor_vertex = self.get_vertex_by_state(neighbor)
            if vertex.color in neighbor_vertex.possible_colors:
                neighbor_vertex.possible_colors.remove(vertex.color)
                if len(neighbor_vertex.possible_colors) <= 0:
                    return False

        return True

    def collapse(self, state: State, color: Color) -> bool:
        vertex = self.get_vertex_by_state(state)
        vertex.color = color
        vertex.possible_colors = [color]
        self.visited_states.append(state)

        return self.propagate(vertex)

    def restore(self, state: State):
        for vertex in self.vertices:
            if vertex.state == state:
                vertex.color = Color.NONE
                self.visited_states.remove(state)
                self.reset_possible_values()

    def solve(self):
        self.iteration_count += 1
        if len(self.visited_states) == len(State):
            return True

        current_vertex = self.get_smallest_entropy_vertex()

        if current_vertex is None:
            return False

        possible_colors = current_vertex.possible_colors

        for color in possible_colors:
            if self.collapse(current_vertex.state, color):
                if self.solve():
                    return True
            self.restore(current_vertex.state)
        return False
