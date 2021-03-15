import typing
import numpy as np


# struktura przechowująca dane o zestawie danych wykorzystywanych do testowania algorytmów szeregowania zadań
class SchedulingData:
    name: str  # nazwa zestawu
    n_jobs: int  # ilość zadan
    n_machines: int  # ilość maszyn
    t_matrix: np.array  # macierz o wymiarach n_jobs x n_machines,
    # zawiera czasy wykonania zadań na maszynach
    schedule: np.array = None

    def __init__(self, name: str, n_jobs: int, n_machines: int, t_matrix: np.array, schedule: np.array = None):
        self.name = name
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.t_matrix = t_matrix
        if schedule is not None:
            self.schedule = schedule

    def __str__(self):
        t_matrix_str = "\n"
        for row in range(0, self.n_jobs, 1):
            for column in range(0, self.n_machines-1, 1):
                t_matrix_str = t_matrix_str + str(int(self.t_matrix[row][column])) + " "
            t_matrix_str = t_matrix_str + str(int(self.t_matrix[row][self.n_machines-1])) + "\n"
        return self.name + str(int(self.n_jobs)) + " " + str(int(self.n_machines)) + t_matrix_str

    def __repr__(self):
        return str(self)


def read_scheduling_data_file(filename: str, n_sets: int) -> typing.List[SchedulingData]:
    file = open(filename)
    ret = []  # lista do której będą dodawane wczytywane zestawy danych
    sets_read = 0  # licznik wczytanych zestawów
    while sets_read != n_sets:  # dopóki nie wczytano
        line = file.readline()  # wczytany wiersz
        if not line:  # jeśli nie udaje sie dalej wczytać wieszy, przerwij pętlę (np. EOF)
            break
        if line[0:4] == "data":  # jeśli linia zaczyna sie od 'data' to rozpoznano początek zestawu
            name = line
            [n_jobs, n_machines] = [int(item) for item in file.readline().split(' ')]  # konwersja na inty 2 wpisów
            t_matrix = np.empty(shape=(n_jobs, n_machines))
            for row in range(0, n_jobs, 1):
                t_matrix[row] = np.array([int(column) for column in file.readline().split(' ')])
            sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawów
            ret.append(SchedulingData(name, n_jobs, n_machines, t_matrix))
    file.close()
    return ret


def draw_gantt_plot(data: SchedulingData):
    pass


#  tworzy macierz harmonogramu zadań, szeregując zadania rosnąco dla każdej maszyny (najprostszy algorytm)
def naive_scheduling(data: SchedulingData):
    schedule = np.full(shape=(data.n_machines, data.n_jobs), fill_value=-1, dtype=int)
    for machine in range(0, data.n_machines, 1):
        for job in range(0, data.n_jobs, 1):
            schedule[machine][job] = job
    data.schedule = schedule


def johnson_rule(data: SchedulingData):
    pass


sched = read_scheduling_data_file("neh.data.txt", 3)`
print(sched[0])
naive_scheduling(sched[0])
print(sched[0].schedule)
