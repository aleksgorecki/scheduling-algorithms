from scheduling_2 import *
import math
import random
from collections import deque
from itertools import combinations
import time


def generate_neighbour(schedule: list, lower_index: int, upper_index: int, method: str = "swap") -> list:
    neighbour = schedule.copy()
    if method == "swap":
        temp = neighbour[upper_index]
        neighbour[upper_index] = neighbour[lower_index]
        neighbour[lower_index] = temp
    elif method == "insert":
        lower = neighbour.pop(lower_index)
        neighbour.insert(upper_index-1, lower)
    elif method == "inverse":
        neighbour[lower_index:upper_index] = neighbour[lower_index:upper_index][::-1]
    else:
        raise Exception()
    return neighbour


def generate_n_neighbours(schedule: list, n_neighbours: int, method: str):
    n_possible_neighbours = math.factorial(len(schedule))
    if n_neighbours > n_possible_neighbours:
        n_neighbours = n_possible_neighbours
    possible_indices = list(range(0, len(schedule), 1))
    indices_combinations = list(combinations(possible_indices, 2))
    random.shuffle(indices_combinations)
    indices_combinations = indices_combinations[0:n_neighbours-1]
    neighbours = []
    for indices in indices_combinations:
        sorted_indices = sorted(indices)
        lower_index = sorted_indices[0]
        upper_index = sorted_indices[1]
        neighbours.append(generate_neighbour(schedule, lower_index, upper_index, method))
    return neighbours


def find_best_neighbour(data: SchedulingData, schedules: list, tabu) -> list:
    best_schedule = data.schedule
    lowest_cmax = makespan(data)
    for schedule in schedules:
        current_cmax = makespan(SchedulingData(name="tmp", n_jobs=data.n_jobs, n_machines=data.n_machines,
                                               t_matrix=data.t_matrix, schedule=schedule))
        if current_cmax < lowest_cmax and schedule not in tabu:
            lowest_cmax = current_cmax
            best_schedule = schedule
    return best_schedule


class StoppingCondition:
    class StateVariables:
        n_iterations: int = 0
        n_useless_iterations: int = 0
        time_passed: int = 0

    state: StateVariables

    def __init__(self):
        self.state = self.StateVariables()

    def update(self) -> None:
        return None

    def check(self) -> bool:
        return False


class IterationsCondition(StoppingCondition):
    max_iterations: int

    def __init__(self, max_iterations):
        StoppingCondition.__init__(self)
        self.max_iterations = max_iterations

    def update(self):
        self.state.n_iterations = self.state.n_iterations + 1

    def check(self) -> bool:
        if self.state.n_iterations >= self.max_iterations:
            return True
        else:
            return False


class UselessIterationsCondition(StoppingCondition):
    max_useless_iterations: int

    def __init__(self, max_useless_iterations):
        StoppingCondition.__init__(self)
        self.max_useless_iterations = max_useless_iterations

    def update(self):
        self.state.n_useless_iterations = self.state.n_useless_iterations + 1

    def check(self) -> bool:
        if self.state.n_useless_iterations >= self.max_useless_iterations:
            return True
        else:
            return False


class TimeCondition(StoppingCondition):
    finish_time: int

    def __init__(self, finish_time):
        StoppingCondition.__init__(self)
        self.finish_time = time.time_ns() + finish_time*1e9

    def update(self):
        self.state.time_passed = time.time_ns()

    def check(self) -> bool:
        if self.state.time_passed >= self.finish_time:
            return True
        else:
            return False


def tabu_search(data: SchedulingData,
                tabu_len: int = 8,
                n_neighbours: int = 8,
                neighbour_method: str = "swap",
                init_scheduling_func=johnson_rule_multiple,
                stopping_condition: StoppingCondition = IterationsCondition(50)) -> int:
    lowest_cmax = math.inf
    tabu = deque(maxlen=tabu_len)
    init_scheduling_func(data)
    current_schedule = data.schedule
    best_schedule = current_schedule
    while True:
        neighbours = generate_n_neighbours(data.schedule, n_neighbours=n_neighbours, method=neighbour_method)
        current_schedule = find_best_neighbour(data, neighbours, tabu)
        current_cmax = makespan(SchedulingData(name="tmp", n_jobs=data.n_jobs, n_machines=data.n_machines,
                                               t_matrix=data.t_matrix, schedule=current_schedule))
        tabu.append(current_schedule)
        if current_cmax < lowest_cmax:
            lowest_cmax = current_cmax
            best_schedule = current_schedule
        else:
            if type(stopping_condition) == UselessIterationsCondition:
                stopping_condition.update()
        if type(stopping_condition) == IterationsCondition or type(stopping_condition) == TimeCondition:
            stopping_condition.update()
        if stopping_condition.check():
            data.schedule = best_schedule
            return makespan(data)