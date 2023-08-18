import dfs
from Ex1 import constants
from Ex1.state import State

initState = State(constants.START_X, constants.START_Y)
result = dfs.DFS(initState)
log = result.getLog()

for i in range(len(log)):
    print("Action {}: ".format(i) + log[i])
