
import numpy as np
import matplotlib.pyplot as plot
import multiprocessing
import os
import shutil



# use backTrackerMaze as the maze generator
def backTrackMaze(params):
    num = params[0]
    wid = params[1]
    hei = params[2]
    shp = (hei, wid)
    # Build actual maze
    O = np.ones(shp, dtype=bool)  # Maze-grid: 1's are black, 0's are white

    # Initially set all cells as unvisited.
    Z = np.zeros(shp, dtype=bool)  # Visited or not

    # stck of visited cells
    stck = []
    # Recursive backTracker
    # 1 Make the initial cell the current cell and mark it as visited.
    # Random Initial cell
    P, Q = np.random.choice(range(0, (shp[0]), 2)), np.random.choice(range(0, (shp[1]), 2))

    # Making it the current cell   
    O[P][Q] = 0
    # Marking it as visited 
    Z[P][Q] = 1
    stck.append([P, Q])

    # 2 While there are unvisited cells
    while (not Z.all()):
        # print(P,Q)
        # 2.1 If the current cell has any neighbors which have not been visited
        nbs = []
        wals = []

        if P + 2 in range(hei) and Z[P + 2][Q] == 0:
            nbs.append([P + 2, Q])
            wals.append([P + 1, Q])
        if P - 2 in range(hei) and Z[P - 2][Q] == 0:
            nbs.append([P - 2, Q])
            wals.append([P - 1, Q])
        if Q + 2 in range(wid) and Z[P][Q + 2] == 0:
            nbs.append([P, Q + 2])
            wals.append([P, Q + 1])
        if Q - 2 in range(wid) and Z[P][Q - 2] == 0:
            nbs.append([P, Q - 2])
            wals.append([P, Q - 1])
        if nbs:
            # 2.1.1 Choose randomly one of the unvisited neighbors
            choi = np.random.choice(range(len(nbs)))
            # 2.1.2 Push the current cell to the stck
            stck.append([P, Q])
            # 2.1.3 Remove the wall between the current cell and the chosen cell
            O[nbs[choi][0]][nbs[choi][1]] = 0
            O[wals[choi][0]][wals[choi][1]] = 0
            # 2.1.4 Make the chosen cell the current cell and mark it as visited
            P = nbs[choi][0]
            Q = nbs[choi][1]
            Z[nbs[choi][0]][nbs[choi][1]] = 1
            Z[wals[choi][0]][wals[choi][1]] = 1

            stck.append([P, Q])
        # 2.2. Else if stck is not empty
        elif stck:
            if P + 1 in range(hei):
                Z[P + 1][Q] = 1
            if P - 1 in range(hei):
                Z[P - 1][Q] = 1
            if Q + 1 in range(wid):
                Z[P][Q + 1] = 1
            if Q - 1 in range(wid):
                Z[P][Q - 1] = 1
            # 2.2.1 Pop a cell from the stck
            p = stck.pop()
            # 2.2.2 Make it the current cell
            P = p[0]
            Q = p[1]
        else:
            break

    plot.figure()
    plot.imshow(O, cmap=plot.cm.binary, interpolation='nearest')
    plot.xticks([]), plot.yticks([])
    plot.savefig("results/backTracks/backTrackerMaze{0:0=2d}.png".format(num))
    np.savetxt("grids/backTracks/{0:0=2d}.txt".format(num), O, fmt='%d')


def randomGridMaze(params):
    num = params[0]
    wid = params[1]
    hei = params[2]
    shp = (hei, wid)
    O = np.random.choice([0, 1], size=shp, p=[.70, .30])
    plot.figure()
    plot.imshow(O, cmap=plot.cm.binary, interpolation='nearest')
    plot.xticks([]), plot.yticks([])
    # plot.show()
    plot.savefig("results/randomGrid/maze{0:0=2d}.png".format(num))
    np.savetxt("grids/randomGrid/{0:0=2d}.txt".format(num), O, fmt='%d')


def generateGrid(num: int, sizeOfMaze: int):
    if os.path.exists("grids"):
        shutil.rmtree("grids")
    if os.path.exists("results"):
        shutil.rmtree("results")
    if os.path.exists("maze.png"):
        os.remove("maze.png")

    for i in ["", "/backTracks/", "/randomGrid/"]:
        os.mkdir("results" + i)
        os.mkdir("grids" + i)

    # specify the num of grids you want to generate
    # grids_n = int(sys.argv[1])
    grids_n = int(num)

    multiprocessing.freeze_support()
    num_process = multiprocessing.cpu_count()
    # for python 3.6 uncomment the line below, and comment the line above
    # num_proc = os.cpu_count()
    pool = multiprocessing.Pool(processes=num_process)

    ng = [(i, sizeOfMaze, sizeOfMaze) for i in range(grids_n)]
    # randomGridMaze(ng)
    pool.map(randomGridMaze, ng)

    ng = [i for i in ng]
    pool.map(backTrackMaze, ng)
    # backTrackMaze(ng)

    pool.close()
    pool.join()
