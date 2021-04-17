from scheduling_3 import *
import csv
import timer


default_data_file = "data/neh.data.txt"
csv_filename = "algorytmy.csv"
csv_file = open(csv_filename, mode="w")
max_dataset_index = 2

datasets = read_data_file(default_data_file, max_dataset_index+1, no_names=False)


class AlgorithmCall:
    func = None
    additional_parameters = None

    def __init__(self, func, params=None):
        self.func = func
        if params is not None:
            self.additional_parameters = params


tabu_search_options = ()
timer = timer.Timer()
csv_handle = csv.writer(csv_file, dialect="excel")
calls = [AlgorithmCall(johnson_rule_multiple), AlgorithmCall(neh)]
time_stats = {}
cmax_stats = {}
for dataset in datasets:
    dataset.name.replace("\n", "")
for dataset in datasets:
    cmax_inner_dictionary = {}
    time_inner_dictionary = {}
    for call in calls:
        timer.start()
        if call.additional_parameters is None:
            cmax = call.func(dataset)
        else:
            cmax = call.func(dataset, call.additional_parameters)
        execution_time = timer.stop()
        algorithm_name = call.func.__name__
        cmax_inner_dictionary.update({call.func.__name__: cmax})
        time_inner_dictionary.update({call.func.__name__: execution_time})
    cmax_stats.update({dataset.name: cmax_inner_dictionary})
    time_stats.update({dataset.name: time_inner_dictionary})




for dataset in datasets:
    row = ""
    csv_handle.writerow([dataset.name, cmax_stats[dataset.name].items()])

csv_file.close()

# data = read_data_file(default_data_file, 21, no_names=False)[20]
# timer.start()
# print(tabu_search(data,
#                   tabu_len=30,
#                   n_neighbours=100,
#                   neighbour_method="swap",
#                   init_scheduling_func=johnson_rule_multiple,
#                   stopping_condition=IterationsCondition(100)))
# print(timer.stop())
