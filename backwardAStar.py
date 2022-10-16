import time
from minHeap import MinHeap
import common as commonFuncs

def pathGeneration(open_heap, closed_heap, start_state, expanded_states, cntr, cell_states):
    while start_state.g_value > open_heap.peek().f_value:
        min_state = open_heap.pop() 
        expanded_states.append(min_state.loc)
        closed_heap.push(min_state)
        actList = commonFuncs.genActList(min_state, cell_states, closed_heap) 
        for act in actList:
            searched_state = commonFuncs.stateAfterMov(min_state, act, cell_states) 
            if searched_state.search_value < cntr:
                searched_state.g_value = 99999
                searched_state.search_value = cntr
            if searched_state.g_value > min_state.g_value + 1:
                searched_state.g_value = min_state.g_value + 1 
                searched_state.treePtr = min_state

                if open_heap.contains(searched_state):
                    open_heap.remove(searched_state)

                searched_state.updateFValue()
                open_heap.push(searched_state)
        if open_heap.isEmpty():
            break


def repeatedBackwardAStar(cell_states, start_location, goal_location, largerGFirst: bool):
    cntr = 0  
    agent_path = []  
    time_step = 0  
    expanded_states = [] 

    start_state = cell_states[start_location[0]][start_location[1]]
    goal_state = cell_states[goal_location[0]][goal_location[1]]

    commonFuncs.nearbyBlockCheck(start_state, cell_states) 

    agent_path.append(start_location) 

    for state_list in cell_states:
        for st in state_list:
            st.h_value = commonFuncs.heuristicFn(st, goal_state)

    print("calculating......")
    start_time = time.time() 
    while goal_state != start_state:
        cntr += 1

        start_state.g_value = 99999 
        start_state.search_value = cntr 
        goal_state.g_value = 0 
        goal_state.search_value = cntr 

        open_heap = MinHeap(largerGFirst)
        closed_heap = MinHeap(largerGFirst)
        start_state.updateFValue()

        open_heap.push(goal_state) 

        pathGeneration(open_heap, closed_heap, start_state, expanded_states, cntr, cell_states) 

        if open_heap.heap_size() == 0:
            print("\033[1;31mI cannot reach the target...o(╥﹏╥)o\033[0m")
            return False

        while start_state != goal_state:
            time_step += 1
            next_state = start_state
            while (next_state.treePtr is not None) & (next_state != goal_state):
                next_state = next_state.treePtr
            if start_state.treePtr.discBlockStatus is False:
                start_state = start_state.treePtr
                agent_path.append(start_state.loc)
                commonFuncs.nearbyBlockCheck(start_state, cell_states)
            else:
                break
        for state_list in cell_states:
            for st in state_list:
                st.h_value = commonFuncs.heuristicFn(st, start_state)
    expanded_states.append(goal_state.loc)
    end_time = time.time()  
    print("We have reached the target")
    print("Search Metrics:")
    print("\t->start location: %s" % start_location)
    print("\t->goal location: %s" % goal_location)
    print("\t->Total Time Step: %d" % time_step)
    print("\t->Actual Cost: %d" % (len(agent_path) - 1))
    print("\t->No.of A* Iterations: %d " % cntr)
    print("\t->Time Cost: %.10f seconds" % (end_time - start_time))
    print("\t->No.of Cells Expanded: %d" % len(expanded_states))

    return agent_path, (end_time-start_time)
