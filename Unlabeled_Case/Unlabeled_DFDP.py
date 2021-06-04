import copy
from util import set2tuple
import math
import random

class DFDP(object):
    '''
    Args: 
    dependency graph Bi_Partite: DG[objID]=set(obj1, obj2, ...)
    MRB limit: int

    Returns:
    self.mapping: start-goal mapping. key: start pose, value: goal pose
    self.IsConnected
    self.action_sequence: action sequence
    '''
    def __init__(self, Bi_Partite, limit):
        # Bi_Partite: key: goal index; value: a set of neighbor starts
        self.limit = limit
        self.goal2start = copy.deepcopy(Bi_Partite)
        self.start2goal = self.reverse_graph(Bi_Partite)
        self.n = len(self.goal2start)
        self.goals = tuple(sorted(self.goal2start.keys()))
        self.start_ordering = []
        self.goal_ordering = []

        # Solution
        self.mapping = {}
        self.action_sequence = []
        self.IsConnected = False

        self.Dynamic_Programming()

        if len(self.goal_ordering) > 0:
            self.IsConnected = True


    def Dynamic_Programming(self):
        '''
        tree node: ordered tuple of filled goals
        '''
        parents = {}
        node_ordering = []
        self.explored = set()
        self.explored.add(())
        stack = []

        #first prune
        pruned_goals, current_AB, initial_AB = self.graph_pruning(tuple())
        if max(current_AB, initial_AB)<=self.limit:
            if pruned_goals != ():
                parents[pruned_goals] = ()
            self.explored.add(pruned_goals)
            for i in self.next_object(pruned_goals):
                stack.append((pruned_goals, i)) #(previous_set, new_goal)
            
        Found = False
        while((len(stack)>0) and (not Found)):
            plan = stack.pop(-1)
            old_node = plan[0]
            next_object = plan[1]
            new_node = set2tuple(set(old_node).union({next_object}))
            if new_node in self.explored:
                continue
            pruned_goals, current_AB, initial_AB = self.graph_pruning(new_node)
            if pruned_goals in self.explored:
                continue
            if max(current_AB, initial_AB)<=self.limit:
                parents[new_node] = old_node
                if pruned_goals != new_node:
                    parents[pruned_goals] = new_node
                self.explored.add(new_node)
                self.explored.add(pruned_goals)
                if pruned_goals == self.goals:
                    Found = True
                    break
                for i in self.next_object(pruned_goals):
                    stack.append((pruned_goals,i))
        
        # Check whether the goal state is in the search tree
        if self.goals in self.explored:
            current_node = self.goals
            while current_node in parents:
                parent_node = parents[current_node]
                last_objects = list(set(current_node).difference(parent_node))
                node_ordering.append(last_objects)
                current_node = parent_node
            
            node_ordering = list(reversed(node_ordering))
            self.goal_ordering = []
            for p in node_ordering:
                if len(p) == 1:
                    self.goal_ordering.append(p[0])
                else:
                    self.goal_ordering = self.goal_ordering + self.free_nodes_detection(set2tuple(set(self.goal_ordering)))
            self.start_ordering, self.action_sequence = self.start_order_generation(self.goal_ordering)
            for ii, obj in enumerate(self.start_ordering):
                self.mapping[obj] = self.goal_ordering[ii]

            
    

    def start_order_generation(self,goal_ordering):
        '''
        Based on the filling order of goal poses, 
        generate the ordering of the start poses,
        such that object at the start pose ranking i in start_ordering 
        will go to the goal pose rankng i in the goal_ordering
        '''
        start_ordering = []
        action_sequence = []
        buffer = []
        available_goals = 0
        for g in goal_ordering:
            available_goals += 1
            # objs that have to be moved(possible to be at the buffer or goal already)
            start_set = self.goal2start[g]
            # objs at the start that have to be moved
            moving_list = list((start_set.difference(set(start_ordering))).difference(set(buffer)))
            while (available_goals>0) and (len(moving_list)>0): # obstacles from start to goal
                s = moving_list.pop(0)
                start_ordering.append(s)
                action_sequence.append((s, 'g'))
                available_goals -= 1
            while (available_goals>0) and (len(buffer)>0): # from buffer to goal
                s = buffer.pop(0)
                start_ordering.append(s)
                action_sequence.append((s, 'g'))
                available_goals -= 1
            if len(moving_list) >0: # obstacles from start to buffer
                buffer = buffer + moving_list
                for s in moving_list:
                    action_sequence.insert(len(action_sequence)-1, (s, 'b'))
        # objects whose start poses are isolated
        for start in set(goal_ordering).difference(set(start_ordering)):
            action_sequence.append((start, 'g'))
            start_ordering.append(start)
        

        return start_ordering, action_sequence
    

    def free_nodes_detection(self, g_tuple):
        '''
        Based on the current set of goals, what kinds of objects at the start can be deal with automatically. Return a removing sequence.
        '''
        partial_ordering = []
        pruning_goal2start = copy.deepcopy(self.goal2start) # the resulting graph after pruning
        pruning_start2goal = copy.deepcopy(self.start2goal) # the resulting graph after pruning
        g_set = set(g_tuple)
        transition_AB = -float('inf') # the max active buffer during pruning
        GO_ON = True # still have the potential to go on pruning
        while GO_ON:
            moved_start = set()
            for g in g_set:
                moved_start = moved_start.union( pruning_goal2start[g])
            transition_AB = max(transition_AB, len(moved_start)-len(g_set)) # the active buffer after the g_set
            for s in moved_start:
                del pruning_start2goal[s]
            new_g_set = set()
            for g in list(pruning_goal2start.keys()):
                if g in g_set:
                    del pruning_goal2start[g]
                    continue
                pruning_goal2start[g] = pruning_goal2start[g].difference(moved_start)
                if len(pruning_goal2start[g])==0:
                    new_g_set.add(g)
                elif len(pruning_goal2start[g])==1:
                    new_g_set.add(g)
            partial_ordering = partial_ordering + list(new_g_set)
            g_set = new_g_set
            if len(g_set) == 0:
                GO_ON = False
        
        return partial_ordering


    def graph_pruning(self, g_tuple):
        '''
        Based on the current set of goals, what kinds of objects can be deal with automatically.
        '''
        pruning_goal2start = copy.deepcopy(self.goal2start) # the resulting graph after pruning
        pruning_start2goal = copy.deepcopy(self.start2goal) # the resulting graph after pruning
        g_set = set(g_tuple)
        transition_AB = -float('inf') # the max active buffer during pruning
        GO_ON = True # still have the potential to go on pruning
        while GO_ON:
            moved_start = set()
            for g in g_set:
                moved_start = moved_start.union( pruning_goal2start[g])
            transition_AB = max(transition_AB, len(moved_start)-len(g_set)) # the active buffer after the g_set
            for s in moved_start:
                del pruning_start2goal[s]
            new_g_set = set()
            for g in list(pruning_goal2start.keys()):
                if g in g_set:
                    del pruning_goal2start[g]
                    continue
                pruning_goal2start[g] = pruning_goal2start[g].difference(moved_start)
                if len(pruning_goal2start[g])==0:
                    new_g_set.add(g)
                elif len(pruning_goal2start[g])==1:
                    new_g_set.add(g)
            g_set = new_g_set
            if len(g_set) == 0:
                GO_ON = False
        
        num_g = len(pruning_goal2start)
        num_s = len(pruning_start2goal)
        current_AB = num_g - num_s
        current_goal_tuple = set2tuple(set(self.goal2start.keys()).difference(pruning_goal2start.keys()))
        return ( current_goal_tuple, current_AB, transition_AB)


    def index2set(self, index):
        set_ = set()
        while index != 0:
            e = int(math.floor(math.log( index, 2)))
            set_.add(e)
            index -= (1<<e)
        return set_

            
    def reverse_graph(self, graph):
        r_graph = {}
        for key in graph.keys():
            r_graph[key] = set() # the reverse has the same number of vertices
        for (key, value) in graph.items():
            for v in value:
                r_graph[v].add(key)
        return r_graph


    def next_object(self, old_node):
        obj_list = list(self.goals)
        random.shuffle(obj_list)
        for i in obj_list:
            if i in old_node:
                pass
            else:
                yield i


def DFDP_Search(Bi_Partite):
    '''
    Args: 
    dependency graph Bi_Partite: DG[objID]=set(obj1, obj2, ...)

    Returns:
    Running Buffer size: int
    self.mapping: start-goal mapping. key: start pose, value: goal pose
    self.action_sequence: action sequence
    '''
    n = len(Bi_Partite)
    for limit in range(n):
        Solver = DFDP(Bi_Partite, limit)
        if Solver.IsConnected:
            return limit, Solver.mapping, Solver.action_sequence
