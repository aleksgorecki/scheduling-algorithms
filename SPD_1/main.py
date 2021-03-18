import typing
import numpy as np
from matplotlib import pyplot as plt


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
        return self.name + str(int(self.n_jobs)) + " " + str(int(self.n_machines)) + t_matrix_str

    def __repr__(self):
        return str(self)


def read_data_file(filename: str, n_sets: int) -> typing.List[SchedulingData]:
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


def makespan(data: SchedulingData, return_value_picker: str = "cmax") -> int or int and np.array or np.array:
    if data.schedule is None:
        print("Dataset not yet scheduled!")
        return
    timespan_matrix = np.array(data.t_matrix)  # kopia do pracy
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            if j == 0:
                if m == 0:
                    timespan_matrix[j][m] = data.t_matrix[data.schedule[j]][m]
                else:
                    timespan_matrix[j][m] = timespan_matrix[j][m-1] + data.t_matrix[data.schedule[j]][m]
            else:
                if m == 0:
                    timespan_matrix[j][m] = timespan_matrix[j-1][m] + data.t_matrix[data.schedule[j]][m]
                else:
                    timespan_matrix[j][m] = np.amax([timespan_matrix[j-1][m], timespan_matrix[j][m-1]]) + data.t_matrix[data.schedule[j]][m]
    if return_value_picker == "matrix":
        return timespan_matrix
    elif return_value_picker == "both":
        return timespan_matrix[data.n_jobs-1][data.n_machines-1], timespan_matrix
    else:
        return timespan_matrix[data.n_jobs-1][data.n_machines-1]


def print_scheduling_data_list(sd_list: typing.List[SchedulingData]):
    for data in sd_list:
        print(data)


def verify_dataset(data: SchedulingData) -> bool:
    if data.t_matrix.shape != tuple([data.n_jobs, data.n_machines]):
        return False
    return True


#  tworzy macierz harmonogramu zadań, szeregując zadania rosnąco dla każdej maszyny (najprostszy algorytm)
def naive(data: SchedulingData):
    data.schedule = list(range(0, data.n_jobs, 1))


# to do
def johnson_rule_2(data: SchedulingData):
    if data.n_machines != 2:
        print("Number of machines in the dataset is not equal to 2!")
        return
    jobs_to_schedule = list(range(0, data.n_jobs, 1))
    tail_list, head_list = [], []
    working_matrix = np.array(data.t_matrix)  # kopia do pracy
    ignore_tag = np.amax(working_matrix) + 1
    while jobs_to_schedule:
        min_indices = np.unravel_index(np.argmin(working_matrix), data.t_matrix.shape)
        if min_indices[1] == 0:
            tail_list.append(min_indices[0])
        else:
            head_list = [min_indices[0]] + head_list
        jobs_to_schedule.remove(min_indices[0])
        for m in range(0, data.n_machines, 1):
            working_matrix[min_indices[0]][m] = ignore_tag
    data.schedule = tail_list + head_list


def johnson_rule_multiple(data: SchedulingData):
    pass


def permutation(data: SchedulingData):
    np.random.permutation()
    pass


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
    machine_block_height = 100/data.n_machines
    machine_block_offset = machine_block_height/2
    gantt.set_ylim(0, data.n_machines*machine_block_height + machine_block_offset*2)
    gantt.set_yticks([machine*machine_block_height + machine_block_offset*2 for machine in range(0, data.n_machines, 1)])
    gantt.set_yticklabels(str(machine) for machine in range(data.n_machines-1, -1, -1))
    job_colors = ["red", "blue", "pink", "green", "orange", "purple"]
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            job_duration = data.t_matrix[data.schedule[j]][m]
            job_beginning_time = timespan_matrix[j][m] - job_duration
            gantt.broken_barh([(job_beginning_time, job_duration)], (data.n_machines*machine_block_height-(machine_block_height*m+machine_block_offset), machine_block_height), facecolors=f"tab:{job_colors[j%len(job_colors)]}")
            gantt.text(x=job_beginning_time+job_duration/2, y=(data.n_machines*machine_block_height-(machine_block_height*m)), s=str(data.schedule[j]), horizontalalignment="center", verticalalignment="center")
    plt.show()


dummy = read_data_file("test.data.txt", 1)[0]
if verify_dataset(dummy):
    naive(dummy)
    gantt_chart(dummy)
else:
    print("Dataset is not in correct format!")
