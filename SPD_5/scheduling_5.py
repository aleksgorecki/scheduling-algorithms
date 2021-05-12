from scheduling_4 import *


def rpq_start_time(data: RPQSchedulingData, job: RPQJob):
    if data.schedule is None:
        raise Exception
    else:
        job_index = data.schedule.index(job)
        if job_index == 0:
            return job.r
        else:
            return max(job.r, rpq_start_time(data, data.schedule[job_index-1]) + data.schedule[job_index-1].p)


def rpq_finish_time(data:RPQSchedulingData, job: RPQJob):
    if data.schedule is None:
        raise Exception
    else:
        return rpq_start_time(data, job) + job.p


def get_job_b(data: RPQSchedulingData, cmax: int):
    if data.schedule is None:
        raise Exception
    viable_jobs = []
    for job in data.jobs:
        if rpq_finish_time(data, job) + job.q == cmax:
            viable_jobs.append(job)
    if len(viable_jobs) == 0:
        print("brak zadan b")
        raise Exception
    return viable_jobs[len(viable_jobs) - 1]


def get_job_a(data: RPQSchedulingData, cmax: int, job_b: RPQJob):
    if data.schedule is None:
        raise Exception
    viable_jobs = []
    job_b_index = data.schedule.index(job_b)
    for job_index, job  in enumerate(data.schedule):
        p_sum = 0
        for j in data.schedule[job_index:job_b_index]:
            p_sum = p_sum + j.p
        if job.r + p_sum + job_b.q == cmax:
            viable_jobs.append(job)
    if len(viable_jobs) == 0:
        print("brak zadan a")
        raise Exception
    return viable_jobs[0]


def get_job_c(data: RPQSchedulingData, cmax: int, job_b: RPQJob):
    if data.schedule is None:
        raise Exception
    viable_jobs = []
    for job in data.schedule:
        if job.q < job_b.q:
            viable_jobs.append(job)
    return viable_jobs[len(viable_jobs) - 1]


def carlier(data: RPQSchedulingData):
    u_b = math.inf
    best_schedule = []
    u = schrage(data)
    if u < u_b:
        u_b = u
        best_schedule = data.schedule
    b =





if __name__ == "__main__":

    pass
