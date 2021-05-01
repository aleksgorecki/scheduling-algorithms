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
    def __init__(self) -> None:
        self.heap_list = []

    def __len__(self) -> int:
        return len(self.heap_list)

    def __str__(self) -> str:
        return str(self.heap_list)

    def __repr__(self) -> str:
        return str(self.heap_list)

    def __iter__(self):
        return iter(self.heap_list)

    @staticmethod
    def parent(pos) -> int:
        return pos//2

    @staticmethod
    def left_child(pos) -> int:
        return pos*2 + 1

    @staticmethod
    def right_child(pos) -> int:
        return pos*2 + 2

    def __getitem__(self, item):
        return self.heap_list[item]

    def swap(self, pos_1, pos_2):
        self.heap_list[pos_1], self.heap_list[pos_2] = self.heap_list[pos_2], self.heap_list[pos_1]

    def heapify(self, pos: int, key: callable = lambda j: j.q):
        pos_largest = pos
        pos_left = self.left_child(pos)
        pos_right = self.right_child(pos)
        if pos_left < len(self) and key(self[pos_left]) > key(self[pos_largest]):
            pos_largest = pos_left
        if pos_right < len(self) and key(self[pos_right]) > key(self[pos_largest]):
            pos_largest = pos_right
        if pos_largest != pos:
            self.swap(pos, pos_largest)
            self.heapify(pos_largest)

    def remove(self, x) -> None:
        i = self.heap_list.index(x)
        self.heap_list.pop(i)
        self.heapify(i)

    def append(self, x, key: callable) -> None:
        #  key = lambda x: x
        if len(self) == 0:
            self.heap_list.append(x)
        else:
            self.heap_list.append(x)
            current_position = len(self)-1
            while True:
                if key(x) > key(self.heap_list[self.parent(current_position)]):
                    self.swap(current_position, self.parent(current_position))
                    current_position = self.parent(current_position)
                else:
                    break


class MinHeap:
    def __init__(self) -> None:
        self.heap_list = []

    def __len__(self) -> int:
        return len(self.heap_list)

    def __str__(self) -> str:
        return str(self.heap_list)

    def __repr__(self) -> str:
        return str(self.heap_list)

    def __iter__(self):
        return iter(self.heap_list)

    @staticmethod
    def parent(pos) -> int:
        return pos//2

    @staticmethod
    def left_child(pos) -> int:
        return pos*2 + 1

    @staticmethod
    def right_child(pos) -> int:
        return pos*2 + 2

    def swap(self, pos_1, pos_2):
        self.heap_list[pos_1], self.heap_list[pos_2] = self.heap_list[pos_2], self.heap_list[pos_1]

    def __getitem__(self, item):
        return self.heap_list[item]

    def heapify(self, pos: int, key: callable = lambda j: j.r):
        pos_largest = pos
        pos_left = self.left_child(pos)
        pos_right = self.right_child(pos)
        if pos_left < len(self) and key(self[pos_left]) < key(self[pos_largest]):
            pos_largest = pos_left
        if pos_right < len(self) and key(self[pos_right]) < key(self[pos_largest]):
            pos_largest = pos_right
        if pos_largest != pos:
            self.swap(pos, pos_largest)
            self.heapify(pos_largest)

    def remove(self, x) -> None:
        i = self.heap_list.index(x)
        self.heap_list.pop(i)
        self.heapify(i)

    def append(self, x, key: callable) -> None:
        #  key = lambda x: x
        if len(self) == 0:
            self.heap_list.append(x)
        else:
            self.heap_list.append(x)
            current_position = len(self)-1
            while True:
                if key(x) < key(self.heap_list[self.parent(current_position)]):
                    self.swap(current_position, self.parent(current_position))
                    current_position = self.parent(current_position)
                else:
                    break


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
    t = 0
    i = 1
    cmax = 0
    l = RPQJob(0, 0, 0, -1)
    q_0 = math.inf
    while len(n_g) != 0 or len(n_n) != 0:
        while len(n_n) != 0 and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
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
            i = i + 1
            cmax = max(cmax, t + j.q)
    return cmax


def schrage_heap(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    n_g = Heap()
    n_n = MinHeap()
    for job in data.jobs:
        n_n.append(job, key=lambda j: j.r)
    sigma = []
    t = (min(n_n, key=lambda job: job.r)).r  # zmienna pomocnczia
    i = 1
    cmax = 0
    while len(n_g) != 0 or len(n_n) != 0:
        while len(n_n) != 0 and (min(n_n, key=lambda job: job.r)).r <= t:  # tylko z dostępnych w N_N
            j = min(n_n, key=lambda job: job.r)
            n_g.append(j, key=lambda x: x.q)
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
