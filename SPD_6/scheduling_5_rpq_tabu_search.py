from scheduling_5 import *
import math
import random
from collections import deque
from itertools import combinations
import time



def makespan_rpq(data: RPQSchedulingData):
    cmax_candidates = []
    for job in data.schedule:
        cmax_candidates.append(rpq_finish_time(data, data.schedule[len(data.schedule)-1]) + job.q)
    return max(cmax_candidates)


class StoppingCondition:
    class StateVariables:
        n_iterations: int = 0
        n_useless_iterations: int = 0
        time_passed: int = 0
        n_useful_iterations: int = 0

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
            self.state.n_iterations = 0
            return True
        else:
            return False

    def __str__(self):
        return str(self.__class__.__name__ + "(" + str(self.max_iterations) + ")")


class UselessIterationsCondition(StoppingCondition):
    max_useless_iterations: int

    def __init__(self, max_useless_iterations):
        StoppingCondition.__init__(self)
        self.max_useless_iterations = max_useless_iterations

    def update(self):
        self.state.n_useless_iterations = self.state.n_useless_iterations + 1

    def check(self) -> bool:
        if self.state.n_useless_iterations >= self.max_useless_iterations:
            self.state.n_useless_iterations = 0
            return True
        else:
            return False

    def __str__(self):
        return str(self.__class__.__name__ + "(" + str(self.max_useless_iterations) + ")")

# niewykorzystane
class UsefulIterationsCondition(StoppingCondition):
    max_useful_iterations: int

    def __init__(self, max_useful_iterations):
        StoppingCondition.__init__(self)
        self.max_useless_iterations = max_useful_iterations

    def update(self):
        self.state.n_useful_iterations = self.state.n_useless_iterations + 1

    def check(self) -> bool:
        if self.state.n_useful_iterations >= self.max_useful_iterations:
            self.state.n_useful_iterations = 0
            return True
        else:
            return False


class TimeCondition(StoppingCondition):
    finish_time: int
    duration: int

    def __init__(self, finish_time):
        StoppingCondition.__init__(self)
        self.finish_time = time.time_ns() + finish_time*1e9
        self.duration = finish_time

    def update(self):
        self.state.time_passed = time.time_ns()

    def check(self) -> bool:
        if self.state.time_passed >= self.finish_time:
            self.state.time_passed = 0
            return True
        else:
            return False

    def __str__(self):
        return str(self.__class__.__name__ + "(" + str(self.duration) + ")")


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
    possible_indices = list(range(0, len(schedule), 1))
    indices_combinations = list(combinations(possible_indices, 2))
    random.shuffle(indices_combinations)
    if n_neighbours < len(indices_combinations) and n_neighbours > 0:
        indices_combinations = indices_combinations[0:n_neighbours-1]
    neighbours = []
    for i, indices in enumerate(indices_combinations):
        sorted_indices = sorted(indices)
        lower_index = sorted_indices[0]
        upper_index = sorted_indices[1]
        neighbours.append(generate_neighbour(schedule, lower_index, upper_index, method))
    return neighbours


class NeighbourMoves:
    @staticmethod
    def swap(schedule: list, lower_index: int, upper_index: int) -> None:
        temp = schedule[upper_index]
        schedule[upper_index] = schedule[lower_index]
        schedule[lower_index] = temp

    @staticmethod
    def insert(schedule: list, lower_index: int, upper_index: int) -> None:
        lower = schedule.pop(lower_index)
        schedule.insert(upper_index - 1, lower)

    @staticmethod
    def inverse(schedule: list, lower_index: int, upper_index: int) -> None:
        schedule[lower_index:upper_index] = schedule[lower_index:upper_index][::-1]


def get_next_candidate_rpq(data: RPQSchedulingData, schedule: list, tabu: deque, method) -> list:
    best_neighbour = []
    best_neighbour_cmax = math.inf
    for lower in range(0, len(schedule), 1):
        for upper in range(lower+1, len(schedule), 1):
            neighbour = schedule.copy()
            method(neighbour, lower, upper)
            if neighbour not in tabu:
                neighbour_cmax = makespan_rpq(data)
                if neighbour_cmax < best_neighbour_cmax:
                    best_neighbour = neighbour
                    best_neighbour_cmax = neighbour_cmax
    return best_neighbour


def tabu_search_all_rpq(data: RPQSchedulingData,
                    tabu_len: int = 10,
                    method = NeighbourMoves.swap,
                    init_scheduling = schrage,
                    condition: StoppingCondition = IterationsCondition(50)):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    tabu = deque(maxlen=tabu_len)
    data_copy = data.copy()
    init_scheduling(data_copy)
    candidate = data_copy.schedule
    best = data_copy.schedule
    lowest_cmax = makespan_rpq(data_copy)
    while True:
        candidate = get_next_candidate_rpq(data_copy, candidate, tabu, method)
        if len(candidate) == 0:
            break
        tabu.append(candidate)
        candidate_cmax = makespan_rpq(data_copy)
        if candidate_cmax < lowest_cmax:
            best = candidate
            lowest_cmax = candidate_cmax
        else:
            if type(condition) == UselessIterationsCondition:
                condition.update()
        if type(condition) == IterationsCondition or type(condition) == TimeCondition:
            condition.update()
        if condition.check():
            break
    data.schedule = best
    return makespan_rpq(data)