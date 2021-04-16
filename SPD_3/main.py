from scheduling_3 import *
import csv
import timer

data_dir = "data/"
#default_data_file = "data002v.txt"
default_data_file = "neh.data.txt"
dataset_index = 0

data = read_data_file(data_dir+default_data_file, dataset_index+1, no_names=False)[dataset_index]


method = "swap"
tabu_len = 10
n_neighbours = 100
cond = IterationsCondition(100)

t = timer.Timer()

print("neh: ")
t.start()
print(neh(data))
print(t.stop())

print("johnson: ")
t.start()
print(johnson_rule_multiple(data))
print(t.stop())

print("tabu search: ")
t.start()
print(tabu_search(data,
                  init_scheduling_func=neh,
                  neighbour_method="swap",
                  tabu_len=4,
                  n_neighbours=100,
                  stopping_condition=IterationsCondition(120)))
print(t.stop())
