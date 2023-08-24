import heapq

from state import State
from heapdict import heapdict

a = State(
    eightPuzzle=[
        [3, 4, 5],
        [1, 0, 2],
        [6, 7, 8]
    ],
    emptyRow=1,
    emptyCol=1
)


state = State(
    eightPuzzle=[
        [3, 4, 5],
        [1, 0, 2],
        [6, 7, 8]
    ],
    emptyRow=1,
    emptyCol=1
)

priority_queue = heapdict()

priority_queue[state] = state.calculate_heuristic()


# b = a_star(a)
#
# for i in range(len(b.getLog())):
#     print(f'Action {i}: ' + b.getLog()[i])

