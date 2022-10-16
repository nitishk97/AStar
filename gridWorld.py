
import numpy as np
import matplotlib.pyplot as plot
import multiprocessing
import os
import shutil



def backTrackMaze(params):
    num = params[0]
    wid = params[1]
    hei = params[2]
    shp = (hei, wid)
    O = np.ones(shp, dtype=bool)
    Z = np.zeros(shp, dtype=bool)
    stck = []
    P, Q = np.random.choice(range(0, (shp[0]), 2)), np.random.choice(range(0, (shp[1]), 2))
    O[P][Q] = 0
    Z[P][Q] = 1
    stck.append([P, Q])
    while (not Z.all()):
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
            choi = np.random.choice(range(len(nbs)))
            stck.append([P, Q])
            O[nbs[choi][0]][nbs[choi][1]] = 0
            O[wals[choi][0]][wals[choi][1]] = 0
            P = nbs[choi][0]
            Q = nbs[choi][1]
            Z[nbs[choi][0]][nbs[choi][1]] = 1
            Z[wals[choi][0]][wals[choi][1]] = 1
            stck.append([P, Q])
        elif stck:
            if P + 1 in range(hei):
                Z[P + 1][Q] = 1
            if P - 1 in range(hei):
                Z[P - 1][Q] = 1
            if Q + 1 in range(wid):
                Z[P][Q + 1] = 1
            if Q - 1 in range(wid):
                Z[P][Q - 1] = 1
            p = stck.pop()
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
    grids_n = int(num)

    multiprocessing.freeze_support()
    num_process = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_process)
    ng = [(i, sizeOfMaze, sizeOfMaze) for i in range(grids_n)]
    pool.map(randomGridMaze, ng)
    ng = [i for i in ng]
    pool.map(backTrackMaze, ng)
    pool.close()
    pool.join()
