from Ex6.constants import GlassState, MAX_GLASSES, DEFAULT_STATE
from Ex6.state import State, StateMonad
from Ex6.dfs import DFS

initial_state = State(DEFAULT_STATE)
result = DFS(initial_state)

for log in result.getLog():
    print(log)
