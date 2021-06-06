import math
import numpy as np
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def getColorMap(obj_list):
    # set colormap
    gist_ncar = plt.get_cmap('gist_ncar')
    cNorm = colors.Normalize(vmin=0, vmax=1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=gist_ncar)

    color_values = np.linspace(0.1, 0.9, len(obj_list))
    color_pool = {} 
    for ii, obj in enumerate(obj_list):
        color_pool[obj] = scalarMap.to_rgba(color_values[ii])

    return color_pool


def show_arrangement(numObjs, Density, start_arr, goal_arr):
    WIDTH = 1000
    HEIGHT = 1000

    Radius = math.sqrt(Density*HEIGHT*WIDTH/numObjs/math.pi)

    color_pool = getColorMap(start_arr.keys())

    fig = plt.figure(num=None, figsize=(int(5 * WIDTH / HEIGHT), 5), dpi=120, facecolor='w', edgecolor='b')
    ax = fig.subplots()

    walls = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    wallx = [p[0] for p in walls + [walls[0]]]
    wally = [p[1] for p in walls + [walls[0]]]
    plt.plot(wallx, wally, 'blue')

    for key, point in goal_arr.items():
        circle = plt.Circle(point,Radius, linestyle='--', edgecolor=color_pool[key], facecolor="white", lw=2,zorder=2)
        ax.add_artist(circle)
        plt.text(point[0], point[1], "G" + str(key),zorder=10)

    for key, point in start_arr.items():
        circle = plt.Circle(point,Radius, facecolor=color_pool[key], lw=2, edgecolor='black',zorder=3)
        ax.add_artist(circle)
        plt.text(point[0], point[1], "S" + str(key),zorder=10)
    # plt.savefig(str(Density)+"ul.svg")
    plt.show()
    