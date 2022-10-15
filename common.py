from cellState import cellState
from gridWorld import generateGrid
import numpy as np

def genStates(typeOfMaze: str):
    data_set = np.loadtxt('grids/{}/00.txt'.format(typeOfMaze),dtype=np.int32)
    return [[cellState(a, b, True if int(data_set[a][b]) == 1 else False) for b in range(len(data_set[0]))] for a in range(len(data_set))]

def heuristicFn(state1: cellState, state2: cellState):
    return abs(state1.loc[0] - state2.loc[0]) + abs(state1.loc[1] - state2.loc[1])

def genActList(cell_state: cellState, cell_states, closeHeap):
    possibleActs = []
    rw = cell_state.loc[0]
    col = cell_state.loc[1]
    if rw + 1 <= len(cell_states) - 1:
        if (cell_states[rw + 1][col].discBlockStatus is False)&(not closeHeap.contains(cell_states[rw + 1][col])):
            possibleActs.append(1)
    if rw - 1 >= 0:
        if (cell_states[rw - 1][col].discBlockStatus is False)&(not closeHeap.contains(cell_states[rw - 1][col])):
            possibleActs.append(2)
    if col + 1 <= len(cell_states) - 1:
        if (cell_states[rw][col + 1].discBlockStatus is False)&(not closeHeap.contains(cell_states[rw][col + 1])):
            possibleActs.append(3)
    if col - 1 >= 0:
        if (cell_states[rw][col - 1].discBlockStatus is False)&(not closeHeap.contains(cell_states[rw][col - 1])):
            possibleActs.append(4)
    return possibleActs

def stateAfterMov(cell_state, act, cell_states):
    rw = cell_state.loc[0]
    col = cell_state.loc[1]
    if act == 1:
        return cell_states[rw + 1][col]
    elif act == 2:
        return cell_states[rw - 1][col]
    elif act == 3:
        return cell_states[rw][col + 1]
    elif act == 4:
        return cell_states[rw][col - 1]
    else:
        return None

def nearbyBlockCheck(st: cellState, cell_states):
    rw = st.loc[0]
    col = st.loc[1]
    if rw + 1 <= len(cell_states) - 1:
        cell_states[rw + 1][col].discBlockStatus = cell_states[rw + 1][col].actBlockStatus
    if rw - 1 >= 0:
        cell_states[rw - 1][col].discBlockStatus = cell_states[rw - 1][col].actBlockStatus
    if col + 1 <= len(cell_states) - 1:
        cell_states[rw][col + 1].discBlockStatus = cell_states[rw][col + 1].actBlockStatus
    if col - 1 >= 0:
        cell_states[rw][col - 1].discBlockStatus = cell_states[rw][col - 1].actBlockStatus

def genUnblockedLocation(cell_states):
    EdgeSize = len(cell_states)
    loc = np.random.randint(0,EdgeSize,2)
    while cell_states[loc[0]][loc[1]].actBlockStatus is True:
        loc = np.random.randint(0,EdgeSize,2)
    return loc
