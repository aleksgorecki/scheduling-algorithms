from scheduling_3 import *
import operator


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

    def __str__(self):
        return f"{self.r} {self.p} {self.q}"

    def __repr__(self):
        return str(self)


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


class HeapList:
    def __init__(self, key: callable = lambda x: x, op: operator = operator.gt) -> None:
        self.heap_list = []
        self.key = key
        self.op = op

    def __len__(self) -> int:
        return len(self.heap_list)

    def __str__(self) -> str:
        return str(self.heap_list)

    def __repr__(self) -> str:
        return str(self.heap_list)

    def __iter__(self):
        return iter(self.heap_list)

    def __getitem__(self, item):
        return self.heap_list[item]

    def __setitem__(self, key, value):
        self.heap_list[key] = value

    def __bool__(self):
        if len(self.heap_list) > 0:
            return True
        else:
            return False

    @staticmethod
    def parent(pos) -> int:
        return (pos - 1)//2

    @staticmethod
    def left_child(pos) -> int:
        return pos*2 + 1

    @staticmethod
    def right_child(pos) -> int:
        return pos*2 + 2

    def swap(self, pos_1, pos_2):
        self.heap_list[pos_1], self.heap_list[pos_2] = self.heap_list[pos_2], self.heap_list[pos_1]

    def heapify(self, pos: int):
        key = self.key
        op = self.op
        largest = pos
        left = self.left_child(pos)
        right = self.right_child(pos)
        if left < len(self) and op(key(self[left]), key(self[largest])):
            largest = left
        if right < len(self) and op(key(self[right]), key(self[largest])):
            largest = right
        if largest != pos:
            self.swap(pos, largest)
            self.heapify(largest)

    def root(self):
        return self[0]

    def pop_root(self):
        if len(self) > 1:
            self[0] = self.heap_list.pop()
            self.heapify(0)
        else:
            self.heap_list.pop()

    def append(self, x) -> None:
        key = self.key
        if len(self) == 0:
            self.heap_list.append(x)
        else:
            self.heap_list.append(x)
            pos = len(self) - 1
            while pos > 0:
                if self.op(key(x), key(self.heap_list[self.parent(pos)])):
                    self.swap(pos, self.parent(pos))
                    pos = self.parent(pos)
                else:
                    break


def schrage(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = []
    n_n = data.jobs
    sigma = []
    t = (min(n_n, key=lambda job: job.r)).r  # zmienna pomocnczia
    cmax = 0
    while n_g or n_n:
        while n_n and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
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
            cmax = max(cmax, t + j.q)
    print(data.schedule)
    return cmax


def pmtn_schrage(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = []
    n_n = data.jobs
    t = 0
    cmax = 0
    l = RPQJob(0, 0, 0, -1)
    while n_g or n_n:
        while n_n and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
            j = min(n_n, key=lambda job: job.r)
            n_g.append(j)
            n_n.remove(j)
            if j.q > l.q:
                l.p = t - j.r
                t = j.r
                if l.p > 0:
                    n_g.append(l)
        if len(n_g) == 0:
            t = (min(n_n, key=lambda job: job.r)).r
        else:
            j = max(n_g, key=lambda job: job.q)
            n_g.remove(j)
            l = j
            t = t + j.p
            cmax = max(cmax, t + j.q)
    return cmax


def schrage_heap(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = HeapList(key=lambda j: j.q, op=operator.gt)
    n_n = HeapList(key=lambda j: j.r, op=operator.lt)
    for job in data.jobs:
        n_n.append(job)
    sigma = []
    t = n_n.root().r
    cmax = 0
    while n_g or n_n:
        while n_n and n_n.root().r <= t:
            j = n_n.root()
            n_g.append(j)
            n_n.pop_root()
        if len(n_g) == 0:
            t = n_n.root().r
        else:
            j = n_g.root()
            n_g.pop_root()
            sigma.append(j)
            t = t + j.p
            cmax = max(cmax, t + j.q)
    return cmax


def pmtn_schrage_heap(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = HeapList(key=lambda j: j.q, op=operator.gt)
    n_n = HeapList(key=lambda j: j.r, op=operator.lt)
    for job in data.jobs:
        n_n.append(job)
    t = n_n.root().r
    cmax = 0
    l = RPQJob(0, 0, 0, -1)
    while n_g or n_n:
        while n_n and n_n.root().r <= t:
            j = n_n.root()
            n_g.append(j)
            n_n.pop_root()
            if j.q > l.q:
                l.p = t - j.r
                t = j.r
                if l.p > 0:
                    n_g.append(l)
        if len(n_g) == 0:
            t = n_n.root().r
        else:
            j = n_g.root()
            n_g.pop_root()
            l = j
            t = t + j.p
            cmax = max(cmax, t + j.q)
    return cmax


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