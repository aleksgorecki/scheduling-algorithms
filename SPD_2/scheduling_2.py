import typing
import numpy as np
from matplotlib import pyplot as plt
import itertools


# struktura przechowująca dane o zestawie danych wykorzystywanych do testowania algorytmów szeregowania zadań
class SchedulingData:
    name: str  # nazwa zestawu
    n_jobs: int  # ilość zadan
    n_machines: int  # ilość maszyn
    t_matrix: np.array  # macierz o wymiarach n_jobs x n_machines,
    # zawiera czasy wykonania zadań na maszynach
    schedule: list = None

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
        return self.name + "\n" + str(int(self.n_jobs)) + " " + str(int(self.n_machines)) + t_matrix_str

    def __repr__(self):
        return str(self)


def custom_dataset(n_jobs: int, n_machines: int, name: str = "custom_dataset"):
    t_matrix = np.random.randint(low=1, high=100, size=(n_jobs, n_machines))
    return SchedulingData(name=name, n_jobs=n_jobs, n_machines=n_machines, t_matrix=t_matrix)


def read_data_file(filename: str, n_sets: int, no_names: bool = False) -> typing.List[SchedulingData]:
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
                [n_jobs, n_machines] = [int(item) for item in file.readline().split(' ')]  # konwersja na inty 2 wpisów
                t_matrix = np.empty(shape=(n_jobs, n_machines))
                for row in range(0, n_jobs, 1):
                    t_matrix[row] = np.array([int(column) for column in file.readline().split(' ')])
                sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawów
                ret.append(SchedulingData(name, n_jobs, n_machines, t_matrix))
    else:
        while sets_read != n_sets:  # dopóki nie wczytano
            line = file.readline()  # wczytany wiersz
            if not line:  # jeśli nie udaje sie dalej wczytać wieszy, przerwij pętlę (np. EOF)
                break
            [n_jobs, n_machines] = [int(item) for item in line.split(' ')]  # konwersja na inty 2 wpisów
            t_matrix = np.empty(shape=(n_jobs, n_machines))
            for row in range(0, n_jobs, 1):
                t_matrix[row] = np.array([int(column) for column in file.readline().split(' ')])
            sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawów
            ret.append(SchedulingData("no_name", n_jobs, n_machines, t_matrix))
    file.close()
    return ret


def makespan(data: SchedulingData, return_value_picker: str = "cmax") -> int or int and np.array or np.array:
    if data.schedule is None:
        print("Dataset not yet scheduled!")
        return
    #  macierz czasów zakończenia zadań, indeksy zadań (wierszy)
    #  zgodne z poszeregowaną kolejnością zadań (data.schedule), a nie absolutnymi indeksami zadań (jak w data.t_matrix)
    fin_matrix = np.array(data.t_matrix)
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            if j == 0:
                if m == 0:
                    fin_matrix[j][m] = data.t_matrix[data.schedule[j]][m]
                else:
                    fin_matrix[j][m] = fin_matrix[j][m - 1] + data.t_matrix[data.schedule[j]][m]
            else:
                if m == 0:
                    fin_matrix[j][m] = fin_matrix[j - 1][m] + data.t_matrix[data.schedule[j]][m]
                else:
                    fin_matrix[j][m] = \
                        np.amax([fin_matrix[j - 1][m], fin_matrix[j][m - 1]]) + data.t_matrix[data.schedule[j]][m]
    if return_value_picker == "matrix":
        return fin_matrix
    elif return_value_picker == "both":
        return fin_matrix[data.n_jobs - 1][data.n_machines - 1], fin_matrix
    else:
        return fin_matrix[data.n_jobs - 1][data.n_machines - 1]


def print_scheduling_data_list(sd_list: typing.List[SchedulingData]):
    for data in sd_list:
        print(data)


def verify_dataset(data: SchedulingData) -> bool:
    if data.t_matrix.shape != tuple([data.n_jobs, data.n_machines]):
        return False
    return True


#  tworzy macierz harmonogramu zadań, szeregując zadania rosnąco dla każdej maszyny (najprostszy algorytm)
def naive(data: SchedulingData) -> int:
    data.schedule = list(range(0, data.n_jobs, 1))
    return makespan(data)


def johnson_rule_2(data: SchedulingData) -> int:
    if data.n_machines != 2:
        print("Number of machines in the dataset is not equal to 2!")
        return -1
    jobs_to_schedule = list(range(0, data.n_jobs, 1))
    tail_list, head_list = [], []
    working_matrix = np.array(data.t_matrix)  # kopia do pracy
    ignore_tag = np.amax(working_matrix) + 1  # najwyższa wartość w macierzy, ignorowanie już uszeregowanych zadań
    while jobs_to_schedule:  # dopóki nie uszeregowano wszystkich zadań
        min_indices = np.unravel_index(np.argmin(working_matrix), data.t_matrix.shape)  # (j,m) najszybszej operacji
        if min_indices[1] == 0:
            tail_list.append(min_indices[0])
        else:
            head_list = [min_indices[0]] + head_list
        jobs_to_schedule.remove(min_indices[0])
        for m in range(0, data.n_machines, 1):
            working_matrix[min_indices[0]][m] = ignore_tag  # usuniecie uszeregowanego zadania poprzez nadpisanie czasu
    data.schedule = tail_list + head_list  # harmonogram w postaci uszeregowanych indeksów zadań do wykonania
    return int(makespan(data))


def johnson_rule_multiple(data: SchedulingData) -> int:
    if data.n_machines == 2:
        johnson_rule_2(data)
        return makespan(data)
    center = int((data.n_machines - 1) / 2)
    imaginary_matrix = np.zeros((data.n_jobs, 2))
    if data.n_machines % 2 == 0:
        for j in range(0, data.n_jobs, 1):
            for m in range(0, center + 1, 1):
                imaginary_matrix[j][0] = imaginary_matrix[j][0] + data.t_matrix[j][m]
            for m in range(center + 1, data.n_machines, 1):
                imaginary_matrix[j][1] = imaginary_matrix[j][1] + data.t_matrix[j][m]
    else:
        for j in range(0, data.n_jobs, 1):
            for m in range(0, center + 1, 1):
                imaginary_matrix[j][0] = imaginary_matrix[j][0] + data.t_matrix[j][m]
            for m in range(center, data.n_machines, 1):
                imaginary_matrix[j][1] = imaginary_matrix[j][1] + data.t_matrix[j][m]
    imaginary_data = SchedulingData(name="imaginary_tmp", n_jobs=data.n_jobs, n_machines=2, t_matrix=imaginary_matrix)
    johnson_rule_2(imaginary_data)
    data.schedule = imaginary_data.schedule
    return makespan(data)


def bruteforce(data: SchedulingData) -> int:
    brute_schedules = list(itertools.permutations(list(range(0, data.n_jobs, 1))))
    makespan_list = []
    for schedule in brute_schedules:
        makespan_list.append(makespan(SchedulingData(name="tmp", n_jobs=data.n_jobs, n_machines=data.n_machines,
                                                     t_matrix=data.t_matrix, schedule=schedule)))
    min_makespan_index = np.argmin(np.array(makespan_list))
    data.schedule = brute_schedules[min_makespan_index]
    return makespan_list[min_makespan_index]


def gantt_chart(data: SchedulingData):
    if data.schedule is None:
        print("Dataset not yet scheduled!")
        return
    [c_max, timespan_matrix] = makespan(data, return_value_picker="both")
    figure, gantt = plt.subplots()
    gantt.set_title("Gantt chart for " + data.name)
    gantt.set_xlabel("Time")
    gantt.set_ylabel("Machine")
    gantt.grid(True)
    gantt.set_xlim(0, c_max)
    barh_height = 100 / data.n_machines
    barh_offset = barh_height / 2
    gantt.set_ylim(0, data.n_machines * barh_height + barh_offset * 2)
    gantt.set_yticks([machine * barh_height + barh_offset * 2 for machine in range(0, data.n_machines, 1)])
    gantt.set_yticklabels(str(machine) for machine in range(data.n_machines-1, -1, -1))  # kolejność maszyn od góry
    job_colors = ["red", "blue", "pink", "green", "orange", "purple"]
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            job_duration = data.t_matrix[data.schedule[j]][m]
            job_beginning_time = timespan_matrix[j][m] - job_duration
            gantt.broken_barh([(job_beginning_time, job_duration)],
                              (data.n_machines * barh_height - (barh_height * m + barh_offset), barh_height),
                              facecolors=f"tab:{job_colors[j % len(job_colors)]}")  # bloki zadan
            gantt.text(x=job_beginning_time+job_duration/2,
                       y=(data.n_machines * barh_height - (barh_height * m)),
                       s=str(data.schedule[j]),
                       horizontalalignment="center",
                       verticalalignment="center")  # indeks zadań na blokach odpowiadających zadaniom
    plt.show()


def neh(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans = []
        schedules = []
        for p in range(0, position+1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=p, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    best_schedule = best_schedule.tolist()
    data.schedule = best_schedule
    return makespan(data)


#  Byc moze zastapi listy w funkcji od sciezki krytycznej
class PathNode:
    job: int
    machine: int


# Zwraca liste par indeksow wezlow sciezki krytycznej, indeksy odnoszą się do schedule, a nie macierzy z czasem operacji
def critical_path(data: SchedulingData) -> list:
    makespan_matrix = makespan(data, return_value_picker="matrix")
    job, machine = 0, 0
    steps = data.n_machines - 1 + data.n_jobs - 1  # kroki, odleglosc do pokonania w grafie (macierzy)
    path = [[job, machine]]
    for step in range(0, steps, 1):
        if machine == data.n_machines-1:
            job = job + 1
        elif makespan_matrix[job + 1][machine] > makespan_matrix[job][machine + 1]:
            job = job + 1
        else:
            machine = machine + 1
        path.append([job, machine])
    return path


# Zadanie zawierające najdłuższą operację na ścieżce krytycznej
def neh1(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans = []
        schedules = []
        for k in range(0, position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=k, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
        #####
        # w tym miejscu wybór zadania x, które nie może być zadaniem równym job
        #####
        for x in range(0, position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=x, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    best_schedule = best_schedule.tolist()
    data.schedule = best_schedule
    return makespan(data)
