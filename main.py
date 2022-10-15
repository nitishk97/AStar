import numpy as np
import common as commonFuncs
from gridWorld import generateGrid
import forwardAStar
import backwardAStar
import adaptiveAStar
import matplotlib.pyplot as plot
import shutil
import os


def pathVisualization(typeOfMaze: str, pathOfAgent, TimeCost, typeOfAStar):
    if not os.path.exists("results/result"):
        os.mkdir("results/result")
    if not os.path.exists("grids/result"):
        os.mkdir("grids/result")
    if os.path.exists("results/result/" + typeOfAStar):
        shutil.rmtree("results/result/" + typeOfAStar)
    if os.path.exists("grids/result/" + typeOfAStar):
        shutil.rmtree("grids/result/" + typeOfAStar)
    os.mkdir("results/result/" + typeOfAStar)
    os.mkdir("grids/result/" + typeOfAStar)

    dataset = np.loadtxt('grids/{}/00.txt'.format(typeOfMaze), dtype=np.int32)
    for r_index in range(len(dataset)):
        for col_index in range(len(dataset)):
            if dataset[r_index][col_index] == 1:
                dataset[r_index][col_index] = 20 

    plot.ion()  
    plot.figure(figsize=(8, 8)) 
    plot.title(typeOfAStar, family="Comic Sans MS")  
    img_art = plot.imshow(dataset, cmap=plot.cm.binary, vmin=0, vmax=20, interpolation='nearest', extent=(0, len(dataset), 0, len(dataset)))    # Initialize drawer
    plot.text(start_location[1] + 0.1, len(dataset) - 0.9 - start_location[0], 'S', fontdict={'size': 432/len(dataset), 'color': 'red'})     # Label start location
    plot.text(goal_location[1] + 0.1, len(dataset) - 0.9 - goal_location[0], 'G', fontdict={'size': 432/len(dataset), 'color': 'red'})       # Label goal location
    for index in range(len(pathOfAgent)):
        if dataset[pathOfAgent[index][0]][pathOfAgent[index][1]] == 0:
            dataset[pathOfAgent[index][0]][pathOfAgent[index][1]] = 10
        else:
            dataset[pathOfAgent[index][0]][pathOfAgent[index][1]] += 1

        img_art.set_data(dataset) 
        plot.pause(0.01) 

    i = 0
    while i < len(pathOfAgent) - 1:
        loc = pathOfAgent[i]
        has_duplicate = False
        for j in range(i + 1, len(pathOfAgent)):
            if all(loc == pathOfAgent[j]):
                has_duplicate = True
                del(pathOfAgent[i + 1: j + 1])
                break
        if not has_duplicate:
            i += 1
    for r_index in range(len(dataset)):
        for col_index in range(len(dataset)):
            if (dataset[r_index][col_index] > 0) & (dataset[r_index][col_index] < 20):
                dataset[r_index][col_index] = 0

    for index in range(len(pathOfAgent)):
        dataset[pathOfAgent[index][0]][pathOfAgent[index][1]] = 10

    img_art.set_data(dataset) 

    plot.text(3/8 * len(cell_states), -len(cell_states)/15, "Finished!", family="Comic Sans MS", fontdict={'size': 12})   # Notice that current drawing is finished
    plot.text(2/8 * len(cell_states), -len(cell_states)/10, "Total steps in optimal path: %d" % (len(pathOfAgent) - 1), family="Comic Sans MS", fontdict={'size': 12})
    #plot.text(1/8 * len(cell_states), -len(cell_states)/10, "Total Time Cost: %d" %TimeCost, family="Comic Sans MS", fontdict={'size': 12})
    
    plot.ioff() 
    plot.show()
if __name__ == '__main__':

    typeOfMaze = "randomGrid"  
    mazeNumber = 1    
    sizeOfMaze = 101   

    print("Checking grid world...", end="")
    if not os.path.exists("grids/%s/00.txt" % typeOfMaze):
        print("\033[1;33mDoes not detect grid world.\033[0m")
        print("Generating grid world...", end="")
        generateGrid(mazeNumber, sizeOfMaze)
        print("\033[1;32mDone!\033[0m")
    else:
        print("\033[1;32mGrid world detected!\033[0m")
        dataset = np.loadtxt('grids/%s/00.txt' % typeOfMaze, dtype=np.int32)
        print("Checking existing grid world...", end="")
        if len(dataset) != sizeOfMaze:
            print("Error!")
            print("\tError Type: Maze Size Unmatched")
            print("\tExpected maze size: %d" % sizeOfMaze)
            print("\tExisting maze size: %d" % len(dataset))
            print("Regenerating the maze with correct size...", end="")
            generateGrid(mazeNumber, sizeOfMaze)
            print("Done!")
        else:
            print("Clear!")

    print("Initializing cell_states...", end="")
    cell_states = commonFuncs.genStates(typeOfMaze)
    print("Done!")

    print("Generating start location and goal location...", end="")
    start_location = commonFuncs.genUnblockedLocation(cell_states)
    goal_location = commonFuncs.genUnblockedLocation(cell_states)

    while (start_location == goal_location).all():
        goal_location = commonFuncs.genUnblockedLocation(cell_states)
    print("Done!")
    print("Start Location: %s" % start_location)
    print("Goal Location: %s" % goal_location)
    print("")

    largerGFirst = False

    print("Repeated Forward A Star Smaller G First: ")
    pathOfAgent, TimeCost = forwardAStar.repeatedForwardAStar(cell_states, start_location, goal_location, largerGFirst)
    if pathOfAgent is not False:
        pathVisualization(typeOfMaze, pathOfAgent, TimeCost, "Forward A Star Smaller G First")
        print("\tCosts for optimal path: %d" % (len(pathOfAgent) - 1))
    print("")

    cell_states = commonFuncs.genStates(typeOfMaze) 
    print("Repeated Forward A Star Bigger G First: ")
    pathOfAgent, TimeCost = forwardAStar.repeatedForwardAStar(cell_states, start_location, goal_location, not largerGFirst)
    if pathOfAgent is not False:
        pathVisualization(typeOfMaze, pathOfAgent, TimeCost, "Forward A Star Larger G First")
        print("\tCosts for optimal path: %d" % (len(pathOfAgent) - 1))
    print("")

    cell_states = commonFuncs.genStates(typeOfMaze) 
    print("Repeated Backward A Star: ")
    pathOfAgent, TimeCost = backwardAStar.repeatedBackwardAStar(cell_states, [4,2], [53,19], largerGFirst)
    if pathOfAgent is not False:
        pathVisualization(typeOfMaze, pathOfAgent, TimeCost, "Backward A Star")
        print("\tCosts for optimal path: %d" % (len(pathOfAgent) - 1))
    print("")

    cell_states = commonFuncs.genStates(typeOfMaze) 
    print("Repeated Adaptive A Star: ")
    pathOfAgent, TimeCost = adaptiveAStar.repeatedAdaptiveAStar(cell_states, start_location, goal_location, largerGFirst)
    if pathOfAgent is not False:
        pathVisualization(typeOfMaze, pathOfAgent, TimeCost, "Adaptive A Star")
        print("\tCosts for optimal path: %d" % (len(pathOfAgent) - 1))
    print("")
