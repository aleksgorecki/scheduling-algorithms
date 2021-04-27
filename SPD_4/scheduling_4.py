from scheduling_3 import *


class NotRPQException(Exception):
    def __init__(self, data: SchedulingData,
                 message="Scheduling data is not in RPQ format (num of columns different than 3)"):
        self.data = data
        self.message = message
        super().__init__(self.message)


class PriorityQueue:
    class Node:
        def __init__(self, elem, priority):
            self.elem = elem
            self.priority = priority

    def __init__(self):
        self.queue = list()

    def __len__(self):
        return len(self.queue)

    def insert(self, new_node: Node):
        if len(self):
            self.queue.append(new_node)
        else:
            for i, node in enumerate(self.queue):
                if new_node.priority >= node.priority:
                    if i == len(self)-1:
                        self.queue.append(new_node)
                else:
                    self.queue.insert(i, new_node)
        pass

    def pop(self):
        return self.queue.pop(0)
        pass

    def __str__(self):
        ret = ""
        for node in self.queue:
            ret = ret + "->" + str(node.elem)
        return ret

    def __repr__(self):
        print(str(self))


def makespan_rpq(data: SchedulingData):
    if data.n_machines != 3:
        raise NotRPQException
    pass


def schrage(data: SchedulingData):
    if data.n_machines != 3:
        raise NotRPQException
    jobs_to_schedule = []  # N_G
    unscheduled_jobs = []  # N_N
    partial_schedule = []  # sigma
    time = 0  # zmienna pomocnczia
    while len(jobs_to_schedule) == 0 or len(unscheduled_jobs) == 0:
        pass
    pass


def pmtn_schrage(data: SchedulingData):
    pass