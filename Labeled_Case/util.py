import numpy as np
import os
import random
import math
import resource

MemLimit = 1.3 * 2**(34)
  
def limit_memory(maxsize): 
    soft, hard = resource.getrlimit(resource.RLIMIT_AS) 
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


def generate_instance(numObjs, Density):
    '''
    Args:
    numObjs: number of objects in this problem
    Density: S(occupied area)/S(environment)

    Returns:
    start_arr: start arrangement. key: int obj ID, value: (x,y) coordinate
    goal_arr: goal arrangement. key: int obj ID, value: (x,y) coordinate
    '''
    instance_num = 20
    arrangement_choices = np.random.choice(range(instance_num),size=2, replace=False)
    my_path = os.path.abspath(os.path.dirname(__file__)) + "/arrangements"
    
    # randomly assign obj IDs to discs
    start_list = list(range(numObjs))
    goal_list = list(range(numObjs))
    random.shuffle(start_list)
    random.shuffle(goal_list)

    # Construct start and goal arrangements
    start_arr = {}
    goal_arr = {}

    ### start arr ###
    f = open( 
        os.path.join(
            my_path, 
            "D="+str(round(Density,1)), 
            "n="+str(numObjs),
            str(arrangement_choices[0])+"_"+str(numObjs)+"_"+str(round(Density,1))+".txt"
            ), 'rb')
    object_index = 0
    for line in f.readlines():
        line = line.decode('utf-8')
        if line == "objects\n":
            continue
        else:
            pose = line.split()
            start_arr[start_list[object_index]] = (float(pose[0]), float(pose[1]))
            object_index += 1
    f.close()

    ### goal arr ###
    f = open( 
        os.path.join(
            my_path, 
            "D="+str(round(Density,1)), 
            "n="+str(numObjs),
            str(arrangement_choices[1])+"_"+str(numObjs)+"_"+str(round(Density,1))+".txt"
            ), 'rb')
    object_index = 0
    for line in f.readlines():
        line = line.decode('utf-8')
        if line == "objects\n":
            continue
        else:
            pose = line.split()
            goal_arr[goal_list[object_index]] = (float(pose[0]), float(pose[1]))
            object_index += 1
    f.close()
    
    return start_arr, goal_arr


def construct_DG( start_arr, goal_arr, radius):
    '''
    Args:
    start_arr: start arrangement. key: int obj ID, value: (x,y) coordinate
    goal_arr: goal arrangement. key: int obj ID, value: (x,y) coordinate
    radius: disc radius

    Returns:
    dependency graph DG: DG[objID]=set(obj1, obj2, ...)
    '''
    DG = {}
    for goal_obj, goal_center in goal_arr.items():
        DG[goal_obj] = set()
        for start_obj, start_center in start_arr.items():
            if start_obj == goal_obj:
                continue
            if (math.sqrt((start_center[0]-goal_center[0])**2+
            (start_center[1]-goal_center[1])**2) <= 2*radius):
                DG[goal_obj].add(start_obj)
    return DG


def set2tuple(s):
    '''
    Args:
    set: number set
    
    Return:
    tuple: ordered number tuple
    '''
    return tuple(sorted(list(s)))
     

if __name__ == '__main__':
    # generate_arrangement()
    batch_generate_instances()
    # split_results()