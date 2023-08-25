from Ex8.heuristic import a_star
from state import State

init_state = State(
    eightPuzzle=[
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ],
    emptyRow=1,
    emptyCol=1
)

result = a_star(init_state)

for i in range(len(result.log)):
    print(f'Action {i}: ' + result.log[i])

