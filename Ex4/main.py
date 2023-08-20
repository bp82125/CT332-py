from Ex4 import constants, dfs, bfs
from Ex4.state import State
from Ex4.dfs import DFS
from Ex4.bfs import BFS


initState = State(constants.START_X, constants.START_Y, constants.START_Z)

print("DFS")
DFS(initState).printLog()

print("\nBFS")
BFS(initState).printLog()






