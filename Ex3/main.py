import bfs
from Ex3 import constants
from Ex3.state import State

initState = State(constants.START_X, constants.START_Y)
result = bfs.BFS(initState)
log = result.getLog()

for i in range(len(log)):
    print("Action {}: ".format(i) + log[i])



