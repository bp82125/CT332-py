from Ex5 import dfs
from Ex5.state import StateMonad, State, Action

initial_state = State(3, 3, "A")

initial_state_monad = StateMonad(initial_state)

result = dfs.DFS(initial_state)

for log in result.log:
    print(log)
