from scheduling_5 import *
import scheduling_5_rpq_tabu_search
import csv
import timer


default_data_file = "data/in50.txt"
csv_filename = "1000-3"
max_dataset_index = -2
excel_lang = "pl"  # "eng"
mode = 1  # 2


#datasets = read_data_file(default_data_file, max_dataset_index+1, no_names=True)
#datasets = read_data_file_rpq(default_data_file, max_dataset_index+1, no_names=False)
#datasets = datasets[0:len(datasets)]
#datasets = [datasets[max_dataset_index]]
# datasets = datasets[0:30]

#datasets = [custom_dataset(n_jobs=3000, n_machines=3, name=n_jobs)]

datasets = []
for size in range(100, 1000, 100):
     dataset = custom_dataset(n_jobs=size, n_machines=3, name=str(size))
     datasets.append(dataset)


class TabuSearchParams:
    def __init__(self, tabu_len: int = 10, neighbour_move=NeighbourMoves.swap,
                 init_scheduling=johnson_rule_multiple, stopping_condition=IterationsCondition(20)):
        self.tabu_len = tabu_len
        self.neighbour_move = neighbour_move
        self.init_scheduling = init_scheduling
        self.stopping_condition = stopping_condition

    def __str__(self):
        return ";tabu" + str(self.tabu_len) + "_" + self.neighbour_move.__name__ + "_" +\
               self.init_scheduling.__name__ + "_" + str(self.stopping_condition)

    def __iter__(self):
        return iter([self.tabu_len, self.neighbour_move, self.init_scheduling, self.stopping_condition])


class AlgorithmCall:
    func = None
    additional_parameters = None

    def __init__(self, func, params=None):
        self.func = func
        if params is not None:
            self.additional_parameters = params


if mode == 1:
    timer = timer.Timer()
    calls = [AlgorithmCall(carlier), AlgorithmCall(carlier_heap)]
             # AlgorithmCall(scheduling_5_rpq_tabu_search.tabu_search_all_rpq,
             #               TabuSearchParams(10, scheduling_5_rpq_tabu_search.NeighbourMoves.swap, schrage,
             #                                scheduling_5_rpq_tabu_search.IterationsCondition(20)))]
    time_stats = {}
    cmax_stats = {}
    for dataset in datasets:
        dataset.name = dataset.name.replace(":\n", "")
    for dataset in datasets:
        print(dataset.name)
        cmax_inner_dictionary = {}
        time_inner_dictionary = {}
        for call in calls:
            timer.start()
            if call.additional_parameters is None:
                cmax = call.func(dataset)
            else:
                cmax = call.func(dataset, *call.additional_parameters)
            execution_time = timer.stop()
            if call.additional_parameters is None:
                algorithm_name = call.func.__name__
            else:
                algorithm_name = call.func.__name__ + str(call.additional_parameters)
            cmax_inner_dictionary.update({algorithm_name: cmax})
            time_inner_dictionary.update({algorithm_name: execution_time})
        cmax_stats.update({dataset.name: cmax_inner_dictionary})
        time_stats.update({dataset.name: time_inner_dictionary})
    if excel_lang == "pl":
        delimiter = ";"
    else:
        delimiter = ","
    csv_file = open(csv_filename + "_cmax.csv", mode="w", newline="")
    csv_handle = csv.writer(csv_file, dialect="excel", delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header_row = list(cmax_stats[datasets[0].name].keys())
    header_row.insert(0, "dataset_name")
    csv_handle.writerow(header_row)
    for dataset in datasets:
        row = [dataset.name]
        for value in cmax_stats[dataset.name].values():
            row.append(value)
        csv_handle.writerow(row)
    csv_file = open(csv_filename + "_time.csv", mode="w", newline="")
    csv_handle = csv.writer(csv_file, dialect="excel", delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header_row = list(time_stats[datasets[0].name].keys())
    header_row.insert(0, "dataset_name")
    csv_handle.writerow(header_row)
    for dataset in datasets:
        row = [dataset.name]
        for value in time_stats[dataset.name].values():
            row.append(value)
        csv_handle.writerow(row)
    csv_file.close()

elif mode == 2:
    print_schedule = False
    calls = [AlgorithmCall(schrage), AlgorithmCall(schrage_heap), AlgorithmCall(pmtn_schrage), AlgorithmCall(pmtn_schrage_heap)]
    timer = timer.Timer()
    for dataset in datasets:
        print(dataset.name)
        for call in calls:
            timer.start()
            if call.additional_parameters is None:
                cmax = call.func(dataset)
            else:
                cmax = call.func(dataset, *call.additional_parameters)
            execution_time = timer.stop()
            print("  ", call.func.__name__, str(call.additional_parameters), ":", sep="")
            print("    cmax: ", cmax)
            print("    time: ", execution_time)
            if print_schedule:
                print("    schedule: ", dataset.schedule)
