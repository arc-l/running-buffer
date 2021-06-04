from util import limit_memory, generate_instance, construct_DG
from Unlabeled_DFDP import DFDP_Search
from show_arrangement import show_arrangement

import numpy as np
import math


def DFDP_Experiment(numObjs, Density, Height=1000, Width=1000):
    '''
    Args:
    numObjs: number of objects in this problem
    Density: S(occupied area)/S(environment)
    Height, Width: Environment size
    '''
    # disc radius
    RAD = math.sqrt((Height*Width*Density)/(math.pi*numObjs))
    
    # Load instance (start arrangement, goal arrangement)
    start_arr, goal_arr = generate_instance(numObjs, Density)

    # show instance
    show_arrangement(numObjs, Density, start_arr, goal_arr)

    # Generate the dependnecy graph
    DG = construct_DG(start_arr, goal_arr, RAD)

    # DFDP
    RB, mapping, action_sequence = DFDP_Search(DG)

    # Result
    print( "Running Buffer size", RB)
    print("start-goal mapping:")
    for start in sorted(mapping.keys()):
        print(start, "-", mapping[start])
    print( "action sequence (objectID, to buffer/goal)")
    for action in action_sequence:
        print( action)


if __name__ == '__main__':
    # Set a limit of the memory usage
    limit_memory(1.3 * 2**(34))  #2**34=16G

    DFDP_Experiment(20, 0.4)