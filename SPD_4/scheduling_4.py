from scheduling_3 import *


class NotRPQException(Exception):
    def __init__(self, data: SchedulingData,
                 message="Scheduling data is not in RPQ format (num of columns different than 3)"):
        self.data = data
        self.message = message
        super().__init__(self.message)


class RPQJob:
    def __init__(self, r: int, p: int, q: int, job_id: int):
        self.r = r
        self.p = p
        self.q = q
        self.id = job_id


class RPQSchedulingData:
    def __init__(self, data: SchedulingData = None, rpq_jobs: list = None):
        if data is not None:
            if data.n_machines != 3:
                raise NotRPQException
            else:
                self.jobs = []
                for job_id, row in enumerate(data.t_matrix):
                    self.jobs.append(RPQJob(r=row[0], p=row[1], q=row[2], job_id=job_id))
                if len(self.jobs) != data.n_jobs:
                    raise Exception
        elif data is None and rpq_jobs is not None:
            self.jobs = rpq_jobs.copy()
        else:
            raise Exception
        self.schedule = []

    def copy(self):
        return RPQSchedulingData(rpq_jobs=self.jobs)


def read_data_file_rpq(filename: str, n_sets: int, no_names: bool = False) -> typing.List[SchedulingData]:
    file = open(filename)
    ret = []  # lista do której będą dodawane wczytywane zestawy danych
    sets_read = 0  # licznik wczytanych zestawów
    if not no_names:
        while sets_read != n_sets:  # dopóki nie wczytano
            line = file.readline()  # wczytany wiersz
            if not line:  # jeśli nie udaje sie dalej wczytać wieszy, przerwij pętlę (np. EOF)
                break
            if line[0:4] == "data":  # jeśli linia zaczyna sie od 'data' to rozpoznano początek zestawu
                name = line
                n_jobs = int(file.readline())
                t_matrix = np.empty(shape=(n_jobs, 3))
                for row in range(0, n_jobs, 1):
                    t_matrix[row] = np.array([int(column) for column in file.readline().split(' ')])
                sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawów
                ret.append(SchedulingData(name, n_jobs, 3, t_matrix))
    else:
        while sets_read != n_sets:  # dopóki nie wczytano
            line = file.readline()  # wczytany wiersz
            if not line:  # jeśli nie udaje sie dalej wczytać wieszy, przerwij pętlę (np. EOF)
                break
            n_jobs = int(file.readline())
            t_matrix = np.empty(shape=(n_jobs, 3))
            for row in range(0, n_jobs, 1):
                t_matrix[row] = np.array([int(column) for column in file.readline().split(' ')])
            sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawów
            ret.append(SchedulingData("no_name", n_jobs, 3, t_matrix))
    file.close()
    return ret


class Heap:
    pass


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


def schrage(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = []
    n_n = data.jobs
    sigma = []
    t = (min(n_n, key=lambda job: job.r)).r  # zmienna pomocnczia
    i = 1
    cmax = 0
    while len(n_g) != 0 or len(n_n) != 0:
        while len(n_n) != 0 and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
            j = min(n_n, key=lambda job: job.r)
            n_g.append(j)
            n_n.remove(j)
        if len(n_g) == 0:
            t = (min(n_n, key=lambda job: job.r)).r
        else:
            j = max(n_g, key=lambda job: job.q)
            n_g.remove(j)
            sigma.append(j)
            t = t + j.p
            i = i + 1
            cmax = max(cmax, t + j.q)
    print(data.schedule)
    return cmax


def pmtn_schrage(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = []
    n_n = data.jobs
    t = (min(n_n, key=lambda job: job.r)).r  # zmienna pomocnczia
    i = 1
    cmax = 0
    while len(n_g) != 0 or len(n_n) != 0:
        while len(n_n) != 0 and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
            j = min(n_n, key=lambda job: job.r)
            n_g.append(j)
            n_n.remove(j)
        if len(n_g) == 0:
            t = (min(n_n, key=lambda job: job.r)).r
        else:
            j = max(n_g, key=lambda job: job.q)
            n_g.remove(j)
            t = t + j.p
            i = i + 1
            cmax = max(cmax, t + j.q)
    return cmax


def schrage_queue(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = []
    n_n = data.jobs
    sigma = []
    t = (min(n_n, key=lambda job: job.r)).r  # zmienna pomocnczia
    i = 1
    cmax = 0
    while len(n_g) != 0 or len(n_n) != 0:
        while len(n_n) != 0 and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
            j = min(n_n, key=lambda job: job.r)
            n_g.append(j)
            n_n.remove(j)
        if len(n_g) == 0:
            t = (min(n_n, key=lambda job: job.r)).r
        else:
            j = max(n_g, key=lambda job: job.q)
            n_g.remove(j)
            sigma.append(j)
            t = t + j.p
            i = i + 1
            cmax = max(cmax, t + j.q)
    print(data.schedule)
    return cmax