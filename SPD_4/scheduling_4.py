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
    data_copy = SchedulingData(name="copy", n_jobs=data.n_jobs, n_machines=data.n_machines, t_matrix=data.t_matrix)
    N_G = []  # N_G
    N_N = list(range(0, data_copy.n_jobs, 1))  # N_N
    partial_schedule = []  # sigma
    time = np.min(data_copy.t_matrix[:, 0])  # zmienna pomocnczia
    i = 0
    while len(N_G) != 0 or len(N_N) != 0:
        print(i)
        while len(N_N) != 0 and np.min(data_copy.t_matrix[:, 0]) <= time:
            job = np.argmin(data_copy.t_matrix[:, 0])
            N_G.append(job)
            N_N.remove(job)
            data_copy.t_matrix[job, 0] = np.max(data.t_matrix) + 99
        if len(N_G) == 0:
            time = np.argmin(data_copy.t_matrix[:, 0])
        else:
            job = np.argmax(data_copy.t_matrix[:, 2])
            N_G.remove(job)
            partial_schedule.append(job)
            time = time + data_copy.t_matrix[job, 1]
    data.schedule = partial_schedule
    return -1


def pmtn_schrage(data: SchedulingData):
    pass