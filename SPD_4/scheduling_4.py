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


def get_min_job(to_compare: list, jobs: list):
    min_job = jobs[0]
    min_time = to_compare[min_job]
    for job in jobs:
        if to_compare[job] < min_time:
            min_job = job
    return min_job


def get_max_job(to_compare: list, jobs: list):
    max_job = jobs[0]
    max_time = to_compare[max_job]
    for job in jobs:
        if to_compare[job] > max_time:
            max_job = job
    return max_job



def schrage(data: SchedulingData):
    if data.n_machines != 3:
        raise NotRPQException
    data_copy = SchedulingData(name="copy", n_jobs=data.n_jobs, n_machines=data.n_machines, t_matrix=data.t_matrix)
    jobs_to_schedule = []  # N_G
    unscheduled_jobs = list(range(0, data_copy.n_jobs, 1))  # N_N
    partial_schedule = []  # sigma
    time = np.min(data_copy.t_matrix[:, 0])  # zmienna pomocnczia
    i = 0
    while len(jobs_to_schedule) != 0 or len(unscheduled_jobs) != 0:
        print(i)
        while len(unscheduled_jobs) != 0 and int(np.min(data_copy.t_matrix[:, 0])) <= time: # tylko z dostępnych w N_N
            job = np.argmin(data_copy.t_matrix[:, 0]) # tylko z dostępnych w N_N
            jobs_to_schedule.append(job)
            unscheduled_jobs.remove(job)
            data_copy.t_matrix[job, 0] = np.max(data.t_matrix) + 1
        if len(jobs_to_schedule) == 0:
            time = np.min(data_copy.t_matrix[:, 0])  # tylko z dostępnych w N_N
        else:
            job = np.argmax(data_copy.t_matrix[:, 2])  # tylko z dostępnych w N_G
            jobs_to_schedule.remove(job)
            partial_schedule.append(job)
            time = time + data_copy.t_matrix[job, 1]
    data.schedule = partial_schedule
    return time


def pmtn_schrage(data: SchedulingData):
    pass