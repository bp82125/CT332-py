from state import State
from heuristic import best_first_search

a = State(
    eightPuzzle=[
        [3, 4, 5],
        [1, 0, 2],
        [6, 7, 8]
    ],
    emptyRow=1,
    emptyCol=1
)

b = best_first_search(a)

for i in range(len(b.getLog())):
    print(f'Action {i}: ' + b.getLog()[i])

