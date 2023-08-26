from __future__ import annotations

from heapdict import heapdict

from Ex8_graph.constants import VERTICES
from Ex8_graph.graph import Graph


class Node:
    def __init__(self, vertex: chr, g_score: int, h_score: int, parent: Node = None):
        self.vertex = vertex
        self.parent = parent
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = self.h_score + self.g_score

    def __eq__(self, other):
        return self.vertex == other.vertex

    def __hash__(self):
        return hash(self.vertex)


def a_star(graph: Graph, start: chr, goal: chr):
    if start not in VERTICES:
        ValueError("Invalids start vertex")
    if goal not in VERTICES:
        ValueError("Invalids goal vertex")

    root = Node(
        vertex=start,
        parent=None,
        g_score=0,
        h_score=graph.vertices[start]
    )

    open_queue = heapdict()
    close_dict = {}

    open_queue[root] = root.f_score

    while open_queue:
        current, _ = open_queue.popitem()
        close_dict[current] = current.g_score

        if current.vertex == goal:
            return current

        for vertex in VERTICES:
            if (current.vertex, vertex) in graph.edges:
                new_node = Node(
                    vertex=vertex,
                    parent=current,
                    g_score=current.g_score + graph.edges[(current.vertex, vertex)],
                    h_score=graph.vertices[vertex]
                )

                if new_node in open_queue and current.g_score >= open_queue[new_node]:
                    continue

                if new_node in close_dict and current.g_score >= close_dict[new_node]:
                    continue

                if new_node in close_dict and current.g_score < close_dict[new_node]:
                    close_dict.pop(new_node)

                open_queue[new_node] = new_node.f_score


def get_path(node: Node) -> str:
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node.vertex)
        current_node = current_node.parent

    path.reverse()
    return ' -> '.join(path)
