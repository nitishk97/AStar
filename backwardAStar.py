import time
from minHeap import MinHeap
import common as commonFuncs

# Backward A* algorithm
def pathGeneration(open_heap, closed_heap, start_state, expanded_states, cntr, cell_states):
    while start_state.g_value > open_heap.peek().f_value:
        # print(open_heap.toString())
        min_state = open_heap.pop()  # Remove a state s with the smallest f-value g(s) + h(s) from open_heap
        expanded_states.append(min_state.loc)
        # print(open_heap.toString())
        closed_heap.push(min_state)
        actList = commonFuncs.genActList(min_state, cell_states, closed_heap)  # Generate action list for the state
        for act in actList:
            searched_state = commonFuncs.stateAfterMov(min_state, act, cell_states)  # Get the state after taking a specific action
            if searched_state.search_value < cntr:
                searched_state.g_value = 99999
                searched_state.search_value = cntr
            if searched_state.g_value > min_state.g_value + 1:
                searched_state.g_value = min_state.g_value + 1  # Update the cost
                searched_state.treePtr = min_state  # Build a forward link pointing to the last state

                # print("open_heap: %s" % open_heap.toString())  # print open_heap

                if open_heap.contains(searched_state):
                    # print("open_heap contains %d: %s" % (searched_state.f_value, searched_state.location))
                    open_heap.remove(searched_state)  # Remove existed state from opehHeap

                # insert succ(s, a) into OPEN with f-value g(succ(s, a)) + h(succ(s, a))
                searched_state.updateFValue()
                # print("searched_state.g_value = %d" % searched_state.g_value)
                # print("searched_state.h_value = %d" % searched_state.h_value)
                # print("searched_state.f_value = %d" % searched_state.f_value)
                # print("searched_state.location = %s" % searched_state.location)
                open_heap.push(searched_state)
                # print("open_heap: %s" % open_heap.toString())  # print open_heap
                # print("")
        if open_heap.isEmpty():
            break


# main function
def repeatedBackwardAStar(cell_states, start_location, goal_location, largerGFirst: bool):
    cntr = 0  # A star cntr
    agent_path = []  # Path recorder
    time_step = 0  # Time step cntr
    expanded_states = []  # Expanded cell_states during the whole repeated A star search

    # Respectively label the cell_states at start location and at goal location as start state and goal state
    start_state = cell_states[start_location[0]][start_location[1]]
    goal_state = cell_states[goal_location[0]][goal_location[1]]

    commonFuncs.nearbyBlockCheck(start_state, cell_states)  # Check the status of nearby cell_states

    agent_path.append(start_location)  # Add the start location to the path
    # print("Start location: %s" % start_state.location)  # Print the start location
    # print("Goal location: %s" % goal_state.location)  # Print the goal location
    # print("")

    # Compute and set heuristic value for all cell_states
    for state_list in cell_states:
        for st in state_list:
            st.h_value = commonFuncs.heuristicFn(st, goal_state)

    print("Iterating...\n")
    start_time = time.time()  # Record start time
    while goal_state != start_state:
        cntr += 1

        start_state.g_value = 99999  # record cost for start state to reach goal state, which uses 999 as infinity
        start_state.search_value = cntr  #
        goal_state.g_value = 0  # record cost for goal state to reach goal state, which is 0
        goal_state.search_value = cntr  #

        # initialize open heap and closed heap
        open_heap = MinHeap(largerGFirst)
        closed_heap = MinHeap(largerGFirst)

        # calculate f value
        start_state.updateFValue()
        # print("State f Value: %d" % start_state.f_value)

        open_heap.push(goal_state)  # insert goal state into open heap

        pathGeneration(open_heap, closed_heap, start_state, expanded_states, cntr, cell_states)  # Run backward A*

        # if open heap is empty, report that can't reach the target
        if open_heap.heap_size() == 0:
            print("\033[1;31mI cannot reach the target...o(╥﹏╥)o\033[0m")
            return False

        # A star search finds the start state and move start location according to the tree pointer
        # Track the tree pointers from goal state to start state
        while start_state != goal_state:
            time_step += 1
            # print("Time Step %d: " % time_step)
            # print("\tTree path: %s(agent)" % start_state.location, end="")
            next_state = start_state

            # Find the next state
            while (next_state.treePtr is not None) & (next_state != goal_state):
                next_state = next_state.treePtr
                # if next_state.discoveredBlockStatus is True:
                #     print("→%s(Blocked)" % next_state.location, end="")
                # else:
                #     print("→%s" % next_state.location, end="")
            # print("→%s(goal)" % goal_state.location)
            if start_state.treePtr.discBlockStatus is False:
                start_state = start_state.treePtr
                agent_path.append(start_state.loc)
                commonFuncs.nearbyBlockCheck(start_state, cell_states)
                # print("\tAgent Moves To: %s" % start_state.location)
            else:
                # print("\tAgent Stops: Next state %s is blocked" % start_state.treePtr.location)
                break
            # print("")

        # Update heuristic value for all cell_states
        for state_list in cell_states:
            for st in state_list:
                st.h_value = commonFuncs.heuristicFn(st, start_state)
    expanded_states.append(goal_state.loc)
    end_time = time.time()  # Record end time
    print("\033[Reached target......")
    print("Search Metrics:")
    print("\tstart loc: %s" % start_location)
    print("\tgoal loc: %s" % goal_location)
    print("\tagent path: ", end="")
    for index in range(len(agent_path)):
        if index == 0:
            print(agent_path[0], end="")
            continue
        print("→%s" % agent_path[index], end="")
    print("")
    print("\tTotal Time Step: %d" % time_step)
    print("\tActual Cost: %d" % (len(agent_path) - 1))
    print("\tNo.of A Star Iterations: %d " % cntr)
    print("\tTime Cost: %.10f seconds" % (end_time - start_time))
    # print("\tExpanded Cells: ", end="")
    # for i in range(len(expanded_states)):
    #     if i == 0:
    #         print(expanded_states[0], end="")
    #         continue
    #     print(",%s" % expanded_states[i], end="")
    # print("")
    print("\tNo.of Cells Expanded: %d" % len(expanded_states))

    return agent_path
