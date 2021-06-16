from scheduling_5 import *
from ortools.sat.python import cp_model


def rpq_ortools(data: RPQSchedulingData or SchedulingData):
    if type(data) == SchedulingData:
        data = RPQSchedulingData(data)
    model = cp_model.CpModel()

    max_r = 0
    max_q = 0
    sum_p = 0

    for task_number in range (0, len(data.jobs)):
        sum_p += data.jobs[task_number].p
        max_r = max(max_r, data.jobs[task_number].r)
        max_q = max(max_q, data.jobs[task_number].q)
    variable_max_value = int(1 + max_r + sum_p + max_q)
    variable_min_value = 0

    model_start_vars = []
    model_end_vars = []
    model_interval_vars = []

    cmax_optimalization_objective = model.NewIntVar(variable_min_value, variable_max_value, 'cmax_makespan')

    for task_number in range (0, len(data.jobs)):
        suffix = f"t:{task_number}"
        start_var = model.NewIntVar(variable_min_value, variable_max_value, 'start_' + suffix)
        end_var = model.NewIntVar(variable_min_value, variable_max_value, 'end_' + suffix)
        interval_var = model.NewIntervalVar(start_var, int(data.jobs[task_number].p), end_var, 'interval_' + suffix)

        model_start_vars.append(start_var)
        model_end_vars.append(end_var)
        model_interval_vars.append(interval_var)

    model.AddNoOverlap(model_interval_vars)


    for task_number in range (0, len(data.jobs)):
        model.Add(model_start_vars[task_number] >= int(data.jobs[task_number].r))


    for task_number in range (0, len(data.jobs)):
        model.Add(cmax_optimalization_objective >= model_end_vars[task_number] + int(data.jobs[task_number].q))

    model.Minimize(cmax_optimalization_objective)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0
    status = solver.Solve(model)

    if (status is not cp_model.OPTIMAL):
        status_readable = "not optimal solution 🙁"
    else:
        status_readable = "optimum found!"

    pi_order = []

    for task_number in range(0, len(data.jobs)):
        pi_order.append((task_number, solver.Value(model_start_vars[task_number])))

    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order]

    dataset.schedule = pi_order

    return solver.ObjectiveValue()



def job_shob_ortools(data: SchedulingData):
    pass


def flowshop_ortools(data: SchedulingData):

    model = cp_model.CpModel()

    variable_max_value = 0
    for job in data.t_matrix:
        for operation in job:
            variable_max_value = variable_max_value + operation
    variable_min_value = 0

    model_start_vars = []
    model_end_vars = []
    model_interval_vars = []

    cmax_optimalization_objective = model.NewIntVar(variable_min_value, variable_max_value, 'cmax_makespan')

    for task_number in range (0, len(data.jobs)):
        suffix = f"t:{task_number}"
        start_var = model.NewIntVar(variable_min_value, variable_max_value, 'start_' + suffix)
        end_var = model.NewIntVar(variable_min_value, variable_max_value, 'end_' + suffix)
        interval_var = model.NewIntervalVar(start_var, int(data.jobs[task_number].p), end_var, 'interval_' + suffix)

        model_start_vars.append(start_var)
        model_end_vars.append(end_var)
        model_interval_vars.append(interval_var)

    model.AddNoOverlap(model_interval_vars)

    for task_number in range (0, len(data.jobs)):
        model.Add(model_start_vars[task_number] >= int(data.jobs[task_number].r))


    for task_number in range (0, len(data.jobs)):
        model.Add(cmax_optimalization_objective >= model_end_vars[task_number] + int(data.jobs[task_number].q))

    model.Minimize(cmax_optimalization_objective)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0
    status = solver.Solve(model)

    if (status is not cp_model.OPTIMAL):
        status_readable = "not optimal solution 🙁"
    else:
        status_readable = "optimum found!"

    pi_order = []

    for task_number in range(0, len(data.jobs)):
        pi_order.append((task_number, solver.Value(model_start_vars[task_number])))

    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order]

    dataset.schedule = pi_order

    return solver.ObjectiveValue()


if __name__ == "__main__":
    default_data_file = "data/t.txt"
    max_dataset_index = -2
    datasets = []
    for size in range(100, 1000, 100):
        dataset = custom_dataset(n_jobs=size, n_machines=3, name=str(size))
        datasets.append(dataset)

    dataset = datasets[0]
    dataset = read_data_file(filename=default_data_file, no_names=True, n_sets=1)[0]
    dataset = dataset = custom_dataset(n_jobs=100, n_machines=3, name=str(size))

    print(rpq_ortools(dataset))
    print(schrage_heap(dataset))

