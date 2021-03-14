import typing


# struktura przechowujaca dane o zestawie danych wykorzystywanych do testowania algorytmow szeregowania zadan
class SchedulingData:
    name: str  # nazwa zestawu
    n_jobs: int  # ilosc zadan
    n_machines: int  # ilosc maszyn
    execution_time: typing.List[typing.List[int]]  # macierz o wymiarach n_jobs x n_machines,
    # zawiera czasy wykonania zadan na maszynach

    def __init__(self, name: str, n_jobs: int, n_machines: int, execution_time: typing.List[typing.List[int]]):
        self.name = name
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.execution_time = execution_time

    def __str__(self):
        execution_time_str = ""
        for row in self.execution_time:
            for column in row:
                execution_time_str = execution_time_str + str(column) + " "
            execution_time_str = execution_time_str + "\n"
        return self.name + str(self.n_jobs) + " " + str(self.n_machines) + execution_time_str

    def __repr__(self):
        return str(self)


def read_scheduling_data_file(filename: str, n_sets: int) -> typing.List[SchedulingData]:
    file_iter = open(filename)
    read_data_list = []  # lista do ktorej beda dodawane wczytywane zestawy danych
    sets_read = 0  # licznik wczytanych zestawow
    while sets_read != n_sets:  # dopoki nie wczytano
        line = file_iter.readline()  # wczytany wiersz
        if not line:  # jesli nie udaje sie dalej wczytac wieszy, przerwij petle (np. EOF)
            break
        if line[0:4] == "data":  # jesli linia zaczyna sie od 'data' to rozpoznano poczatek zestawu
            name = line
            [n_jobs, n_machines] = [int(item) for item in file_iter.readline().split(' ')]  # konwersja na inty 2 wpisow
            execution_time = [[]]
            for row in range(0, n_jobs, 1):
                # konwersja na inty wiersza czasow
                execution_time.append([int(column) for column in file_iter.readline().split(' ')])
            sets_read = sets_read + 1  # inkrementacja licznika wczytanych zestawow
            read_data_list.append(SchedulingData(name, n_jobs, n_machines, execution_time))
    file_iter.close()
    return read_data_list


def draw_gantt_plot(s_d: SchedulingData):
    pass


def naive(s_d: SchedulingData):
    pass


def johnson_rule(s_d: SchedulingData):
    pass


print(read_scheduling_data_file("neh.data.txt", 3))
