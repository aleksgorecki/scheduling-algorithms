from scheduling_3 import *


class NotRPQException(Exception):
    def __init__(self, data: SchedulingData,
                 message="Scheduling data is not in RPQ format (num of columns different than 3)"):
        self.data = data
        self.message = message
        super().__init__(self.message)


class PriorityQueue:
    def __init__(self):
        self.len = 0

    def __len__(self):
        return self.len
        pass

    def push(self):
        pass

    def pop(self):
        pass

    pass


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