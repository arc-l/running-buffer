import copy
import random

from util import set2tuple
from SCC_decomposition import SCC_decomposition, Graph_Decomposition, Topological_SCC_ordering

class DFDP(object):
    '''
    Input: 
    dependency graph DG: DG[objID]=set(obj1, obj2, ...)
    MRB limit: int

    Output:
    self.ordering: object ordering sorted by the time when objects arrive at the goal
    self.action_sequence: (objID, 'g'/'b') 'g' means to the goal, 'b' means to the buffer
    self.TB: total buffer size
    self.ordering = [] when problem is infeasible
    '''
    def __init__(self, DG, limit):
        self.limit = limit
        self.DG = DG
        self.n = len(self.DG)
        
        # goal state
        self.objects = set2tuple(self.DG.keys())

        # output
        self.ordering = [] # object ordering sorted by the time when objects arrive at the goal
        self.action_sequence = [] # (objID, 'g'/'b') 'g' means to the goal, 'b' means to the buffer
        self.TB = 0
        self.IsConnected = False

        self.DFDP()

        if len(self.ordering) > 0:
            self.IsConnected = True

    def DFDP(self):
        '''
        tree node: ordered tuple of objects at the goal
        '''
        object_ordering = []
        parents = {}
        self.explored = set()
        self.buffer_objects = {}
        
        # start state: ()
        stack = [()] 
        self.explored.add(())
        self.buffer_objects[()] = set()

        Found = False
        while((len(stack)>0) and (not Found)):
            old_node = stack.pop(-1)
            for next_object in self.next_object(old_node):
                new_node = set2tuple(set(old_node).union({next_object}))
                if new_node in self.explored:
                    continue
                # Check whether the running buffer size exceed the limit 
                # during the transition
                if self.valid_transition(old_node, next_object, new_node):
                    parents[new_node] = old_node
                    stack.append(new_node)
                    if new_node == self.objects:
                        Found = True
                        break
        
        # check whether the goal state is connected to the search tree
        if self.objects in self.explored:
            # Sort the objects based on the time arriving at the goal 
            current_node = self.objects
            while current_node in parents:
                parent_node = parents[current_node]
                last_object = list(set(current_node).difference(parent_node))[0]
                object_ordering.append(last_object)
                current_node = parent_node

            # Generate action sequence
            self.TB = 0
            self.ordering = list(reversed(object_ordering))
            self.action_sequence = [(x,'g') for x in self.ordering]
            for (i, obs) in enumerate(self.ordering):
                for (j, obj) in enumerate(self.ordering[:i]):
                    if obs in self.DG[obj]:
                        self.TB += 1
                        index = self.action_sequence.index((obj, 'g'))
                        self.action_sequence.insert(index, (obs, 'b'))
                        break

            # print "ordering", self.ordering
            # print "actions", self.action_sequence
    
    def next_object(self, old_node):
        '''
        Choose a proper branch to go
        '''
        obj_list = list(self.objects)
        
        # randomness can be added to the branching
        # random.shuffle(obj_list)

        for i in obj_list:
            if i in old_node:
                pass
            else:
                yield i

    def valid_transition(self,old_node, next_object, new_node):
        old_buffer = self.buffer_objects[old_node]
        new_objects = set(self.DG[next_object]).difference(set(old_node))
        new_buffer = (old_buffer.union(new_objects)).difference(set([next_object]))

        if next_object in old_buffer:
            transition_cost = max(len(old_buffer), len(new_buffer)+1)
        else:
            transition_cost = max(len(old_buffer), len(new_buffer))

        if len(new_buffer) > self.limit:
            self.explored.add(new_node) # dead_end
            return False

        if transition_cost <= self.limit:
            self.buffer_objects[new_node] = new_buffer
            self.explored.add(new_node)
            return True
        else:
            return False


def DFDP_Search(Dgraph, RB=0):
    '''
    Generate action sequence solution with RB = MRB
    Args: 
    dependency graph DG: DG[objID]=set(obj1, obj2, ...)
    RB: Running Buffer lower bound(=0)

    Returns:
    RB: int running buffer size
    action sequence: [(objID, 'g'/'b')]
    '''
    action_sequence = []

    # strongly connected components decomposition
    Partition = SCC_decomposition(Dgraph, Dgraph.keys())
    SCC_ordering = Topological_SCC_ordering(Dgraph, Partition)
    
    RB = 0 # start with 0 running buffers
    for SCC_index in SCC_ordering:
        SCC = Partition[SCC_index]
        SCC_list = list(SCC)
        # construct the strongly connected component
        new_Graph = Graph_Decomposition(Dgraph, SCC_list)
        
        # increase RB size when it fails
        solver = DFDP(new_Graph, RB)
        while not solver.IsConnected:
            RB += 1
            solver = DFDP(new_Graph, RB)

        # transform the action sequence
        real_action_sequence = []
        for action in solver.action_sequence:
            real_action = (SCC_list[action[0]], action[1])
            real_action_sequence.append(real_action)
        action_sequence = action_sequence + real_action_sequence

    return RB, action_sequence

        
