from scheduling_1 import *

def neh(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans, schedules = [], []
        for p in range(0, position+1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=p, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    data.schedule = best_schedule.tolist()
    return makespan(data)


def neh_second_insertion_loop(data: SchedulingData, job_position: int) -> list:
    x_job = data.schedule[job_position]
    makespans, schedules = [], []
    data.schedule = np.delete(data.schedule, job_position)
    data.schedule = np.delete(data.schedule, job_position)
    for x in range(0, job_position + 1, 1):
        tmp_schedule = np.insert(arr=data.schedule, obj=x, values=x_job)
        cmax = makespan(SchedulingData(name="tmp", n_jobs=data.n_jobs, n_machines=data.n_machines,
                                       t_matrix=data.t_matrix, schedule=tmp_schedule))
        makespans.append(cmax)
        schedules.append(tmp_schedule)
    best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
    return best_schedule.tolist()


# Reprezentacja ścieżki krytycznej w postaci listy par zadanie-maszyna
def critical_path(data: SchedulingData) -> list:
    makespan_matrix = makespan(data, return_value_picker="matrix")
    start_matrix = np.array(makespan_matrix, dtype=int)
    ret = []
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            start_matrix[j][m] = makespan_matrix[j][m] - data.t_matrix[data.schedule[j]][m]
    for j in range(0, data.n_jobs - 1, 1):
        for m in range(0, data.n_machines, 1):
            if makespan_matrix[j][m] == start_matrix[j + 1][m]:
                ret.append([data.schedule[j], m])
    ret.append([data.schedule[data.n_jobs-1], data.n_machines-1])  # ostatnie zadanie na ostatnie macierzy (?)
    return ret


# Reprezentacja ścieżki krytycznej jako macierzy (analogicznie do macierzy sąsiedztwa w grafach)
# czas operacji jesli operacja jest na scieżce oraz 0 jeśli operacji na ścieżc0e nie ma (idealnie byłoby None, lub NULL,
# ale konwersja typów na to nie pozwala). Taki zapis ułatwia szukanie maksimów, sumowanie itp.
def critical_path_matrix(data: SchedulingData) -> np.array:
    makespan_matrix = makespan(data, return_value_picker="matrix")
    start_matrix = np.array(makespan_matrix, dtype=int)
    path_matrix = np.empty(shape=(data.n_jobs, data.n_machines), dtype=int)
    for j in range(0, data.n_jobs, 1):
        for m in range(0, data.n_machines, 1):
            start_matrix[j][m] = makespan_matrix[j][m] - data.t_matrix[data.schedule[j]][m]
    for j in range(0, data.n_jobs - 1, 1):
        for m in range(0, data.n_machines, 1):
            if makespan_matrix[j][m] == start_matrix[j + 1][m]:
                path_matrix[j][m] = data.t_matrix[data.schedule[j]][m]
            else:
                path_matrix[j][m] = 0
    # ostatnie zadanie na ostatnie macierzy (?)
    for m in range(0, data.n_machines, 1):
        if m == data.n_machines - 1:
            path_matrix[data.n_jobs - 1][m] = data.t_matrix[data.n_jobs - 1][m]
        else:
            path_matrix[data.n_jobs - 1][m] = 0
    return path_matrix


# Zadanie zawierające najdłuższą operację na ścieżce krytycznej
def neh1(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans, schedules = [], []
        for k in range(0, position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=k, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
        path_matrix = critical_path_matrix(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                                          t_matrix=data.t_matrix, schedule=schedule))
        # ignorowanie zadania, które było dopasowywane w poprzednim kroku
        for m in range(0, data.n_machines, 1):
            path_matrix[schedule.tolist().index(job)][m] = 0
        # zadanie o najdłuższej operacji na s. krytycznej
        x_position = np.unravel_index(np.argmax(path_matrix), shape=path_matrix.shape)[0]
        x_job = schedule[x_position]
        makespans, schedules = [], []
        schedule = np.delete(schedule, x_position)
        for x in range(0, x_position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=x, values=x_job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    data.schedule = best_schedule.tolist()
    return makespan(data)


# Zadanie zawierające największą liczbę operacji wchodzących w ścieżkę krytyczną
def neh2(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans, schedules = [], []
        for k in range(0, position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=k, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
        path_matrix = critical_path_matrix(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                                          t_matrix=data.t_matrix, schedule=schedule))
        # ignorowanie zadania, które było dopasowywane w poprzednim kroku
        for m in range(0, data.n_machines, 1):
            path_matrix[schedule.tolist().index(job)][m] = 0
        # zadanie o największej sumie
        x_position = np.argmax(np.sum(a=path_matrix, axis=1, dtype=int))
        x_job = schedule[x_position]
        makespans, schedules = [], []
        schedule = np.delete(schedule, x_position)
        for x in range(0, x_position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=x, values=x_job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    data.schedule = best_schedule.tolist()
    return makespan(data)


# Zadanie zawierające największą liczbę operacji wchodzących w ścieżkę krytyczną
def neh3(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = np.array([], dtype=int)
    for position, job in enumerate(sorted_jobs):
        tmp_schedule = sorted_jobs.copy()[0:position + 1]
        makespans, schedules = [], []
        for k in range(0, position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=k, values=job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
        path_matrix = critical_path_matrix(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                                          t_matrix=data.t_matrix, schedule=schedule))
        # ignorowanie zadania, które było dopasowywane w poprzednim kroku
        for m in range(0, data.n_machines, 1):
            path_matrix[schedule.tolist().index(job)][m] = 0
        # zadanie o największej ilosci operacji
        x_position = np.argmax(np.count_nonzero(a=path_matrix, axis=1))
        x_job = schedule[x_position]
        makespans, schedules = [], []
        schedule = np.delete(schedule, x_position)
        for x in range(0, x_position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=x, values=x_job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule
    data.schedule = best_schedule.tolist()
    return makespan(data)

#Zadanie, ktorego usuniecie spowoduje najwieksze zmniejszenie wartosci Cmax
def neh4(data: SchedulingData) -> int:
    priority = np.sum(a=data.t_matrix, axis=1, dtype=int)  # suma każdego wiersza (axis=1)
    sorted_jobs = np.argsort(a=-priority, kind="stable")  # sortowanie malejąco, bo minus i sortuje liczby ujemne
    schedule = np.array([], dtype=int)
    best_schedule = sorted_jobs  # inicjalizacja, "w razie czego", w sytuacji gdyby lista miała być pusta
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
        best_schedule = schedules[np.argmin(makespans)]
        schedule = best_schedule
        #################################
        makespans_x = []
        removed = []
        for p in range(0, position+1, 1):
            tmp_schedule_x = best_schedule
            smaller_tmp = tmp_schedule_x
            current_job = sorted_jobs[position]
            if tmp_schedule_x[p] == current_job: #pominiecie operacji dla zadania dla ktorego wlasnie znalezlismy uszeregowanie
                continue
            tmp_diff = smaller_tmp[p]
            smaller_tmp = smaller_tmp[~np.isin(tmp_schedule_x, tmp_diff)] #tmp pomniejszone o zadanie dla ktorego bedziemy liczyc Cmax
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=smaller_tmp))
            makespans_x.append(cmax)
            removed.append(tmp_schedule_x[p])
        if position == 0: #pominiecie reszty petli dla pierwszej iteracji
            continue
        x_job = removed[np.argmin(makespans_x)]
        x_position = list(best_schedule).index(x_job)
        #################################
        makespans, schedules = [], []
        schedule = np.delete(schedule, x_position)
        for x in range(0, x_position + 1, 1):
            tmp_schedule = np.insert(arr=schedule, obj=x, values=x_job)
            cmax = makespan(SchedulingData(name="tmp", n_jobs=position+1, n_machines=data.n_machines,
                                           t_matrix=data.t_matrix, schedule=tmp_schedule))
            makespans.append(cmax)
            schedules.append(tmp_schedule)
        best_schedule = schedules[np.argmin(makespans)]  # zgodnie z dokumentacją argmin zwróci pierwsze wystąpienie
        schedule = best_schedule

    data.schedule = best_schedule
    return makespan(data)
