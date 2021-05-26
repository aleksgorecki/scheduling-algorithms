from scheduling_4 import *


def rpq_start_time(data: RPQSchedulingData, job: RPQJob):
    if data.schedule is None or not data.schedule:
        raise Exception
    else:
        job_index = data.schedule.index(job)
        if job_index == 0:
            return job.r
        else:
            return max(job.r, rpq_start_time(data, data.schedule[job_index-1]) + data.schedule[job_index-1].p)


def rpq_finish_time(data: RPQSchedulingData, job: RPQJob):
    if data.schedule is None or not data.schedule:
        raise Exception
    else:
        return rpq_start_time(data, job) + job.p


def get_job_b(data: RPQSchedulingData, cmax: int):
    if data.schedule is None or not data.schedule:
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
    if data.schedule is None or not data.schedule:
        raise Exception
    viable_jobs = []
    job_b_index = data.schedule.index(job_b)
    for job_index, job in enumerate(data.schedule):
        p_sum = 0
        for j in data.schedule[job_index:job_b_index+1]:
            p_sum = p_sum + j.p
        if job.r + p_sum + job_b.q == cmax:
            viable_jobs.append(job)
    if len(viable_jobs) == 0:
        print("brak zadan a")
        raise Exception
    return viable_jobs[0]


def get_job_c(data: RPQSchedulingData, job_a: RPQJob, job_b: RPQJob):
    if data.schedule is None or not data.schedule:
        raise Exception
    viable_jobs = []
    job_a_index = data.schedule.index(job_a)
    job_b_index = data.schedule.index(job_b)
    for job in data.schedule[job_a_index:job_b_index+1]:
        if job.q < job_b.q:
            viable_jobs.append(job)
    if not viable_jobs:
        return None
    return viable_jobs[len(viable_jobs) - 1]


def carlier(data: RPQSchedulingData, ub=math.inf):
    cmax = None
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    best_schedule = []
    u = schrage(data)
    if u < ub:
        ub = u
        best_schedule = data.schedule
    b = get_job_b(data, u)
    a = get_job_a(data, u, b)
    c = get_job_c(data, a, b)
    if c is None:
        data.schedule = best_schedule
        return u
    job_c_index = data.schedule.index(c)
    job_b_index = data.schedule.index(b)
    k = data.schedule[job_c_index+1:job_b_index+1]  # blok zadań
    k_c = data.schedule[job_c_index:job_b_index+1]
    r_k = min(k, key=lambda job: job.r).r
    q_k = min(k, key=lambda job: job.q).q
    p_k = sum(job.p for job in k)
    c.r = max(c.r, r_k + p_k)
    lb = pmtn_schrage(data)
    h_k = r_k + q_k + p_k
    h_k_c = min(k_c, key=lambda job: job.r).r + min(k_c, key=lambda job: job.q).q + sum(job.p for job in k_c)
    lb = max(h_k, h_k_c, lb)
    if lb < ub:
        cmax = carlier(data, ub)
    c.r = max(c.r, r_k + p_k)  # odtworzenie ?
    c.q = max(c.q, q_k + p_k)
    lb = pmtn_schrage(data)
    h_k = r_k + q_k + p_k
    h_k_c = min(k_c, key=lambda job: job.r).r + min(k_c, key=lambda job: job.q).q + sum(job.p for job in k_c)
    lb = max(h_k, h_k_c, lb)
    if lb < ub:
        cmax = carlier(data, ub)
    c.q = max(c.q, q_k + p_k)  # odtworzenie ?
    if cmax is None:
        cmax = u
    return cmax


def carlier_heap(data: RPQSchedulingData, ub=math.inf):
    cmax = None
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    best_schedule = []
    u = schrage_heap(data)
    if u < ub:
        ub = u
        best_schedule = data.schedule
    b = get_job_b(data, u)
    a = get_job_a(data, u, b)
    c = get_job_c(data, a, b)
    if c is None:
        data.schedule = best_schedule
        return u
    job_c_index = data.schedule.index(c)
    job_b_index = data.schedule.index(b)
    k = data.schedule[job_c_index+1:job_b_index+1]  # blok zadań
    k_c = data.schedule[job_c_index:job_b_index+1]
    r_k = min(k, key=lambda job: job.r).r
    q_k = min(k, key=lambda job: job.q).q
    p_k = sum(job.p for job in k)
    c.r = max(c.r, r_k + p_k)
    lb = pmtn_schrage_heap(data)
    h_k = r_k + q_k + p_k
    h_k_c = min(k_c, key=lambda job: job.r).r + min(k_c, key=lambda job: job.q).q + sum(job.p for job in k_c)
    lb = max(h_k, h_k_c, lb)
    if lb < ub:
        cmax = carlier_heap(data, ub)
    c.r = max(c.r, r_k + p_k)  # odtworzenie ?
    c.q = max(c.q, q_k + p_k)
    lb = pmtn_schrage_heap(data)
    h_k = r_k + q_k + p_k
    h_k_c = min(k_c, key=lambda job: job.r).r + min(k_c, key=lambda job: job.q).q + sum(job.p for job in k_c)
    lb = max(h_k, h_k_c, lb)
    if lb < ub:
        cmax = carlier_heap(data, ub)
    c.q = max(c.q, q_k + p_k)  # odtworzenie ?
    if cmax is None:
        cmax = u
    return cmax


if __name__ == "__main__":
    print("carlier:")
    rpq_l = read_data_file_rpq(filename="data/mm.data.txt", n_sets=8, no_names=False)
    for data in rpq_l:
        print(carlier(data))