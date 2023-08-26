from Ex8_graph.a_star import a_star, get_path
from Ex8_graph.graph import Graph

with open('input.txt', 'r') as file:
    lines = file.readlines()

matrix = []

for line in lines:
    values = line.strip().split()
    row = [int(value) for value in values]
    matrix.append(row)

graph = Graph().create_from_matrix(matrix)

start = 'A'
goal = 'G'
res = a_star(graph, start, goal)
print(get_path(res))
