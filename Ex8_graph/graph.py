from __future__ import annotations
from constants import VERTICES


class Graph:
    def __init__(self, vertices: dict = None, edges: dict = None):
        self.vertices = vertices if vertices is not None else {}
        self.edges = edges if edges is not None else {}

    def add_vertex(self, vertex: int, heuristic: int) -> Graph:
        return Graph(
            vertices=self.vertices | {vertex: heuristic},
            edges=self.edges
        )

    def add_edge(self, start: int, end: int, score: int) -> Graph:
        return Graph(
            vertices=self.vertices,
            edges=self.edges | {(start, end): score}
        )

    @staticmethod
    def create_from_matrix(matrix: list[list[int]]) -> Graph:
        num_vertices = len(VERTICES)
        graph = Graph()
        for i in range(num_vertices):
            heuristic = matrix[i][0]

            graph = graph.add_vertex(VERTICES[i], heuristic)

            for j, score in enumerate(matrix[i][1:], start=0):
                if score != 0:
                    graph = graph.add_edge(VERTICES[i], VERTICES[j], score)

        return graph
