from scheduling_5 import *
from ortools.sat.python import cp_model


def rpq_ortools(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    model = cp_model.CpModel()

    pass


def flowshop_ortools(data: SchedulingData):
    pass


if __name__ == "__main__":
    pass