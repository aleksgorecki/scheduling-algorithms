from scheduling_3 import *
import csv
import timer

data_dir = "data/"
default_data_file = "neh.data.txt"
dataset_index = 40

data = read_data_file(data_dir+default_data_file, dataset_index+1)[dataset_index]

t = timer.Timer()
t.start()
print(tabu_search(data,
                  init_scheduling_func=neh,
                  neighbour_method="swap",
                  tabu_len=10,
                  n_neighbours=100,
                  stopping_condition=IterationsCondition(100)))
print(t.stop())
