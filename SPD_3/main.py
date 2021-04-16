from scheduling_3 import *
import csv
import timer

data_dir = "data/"
#default_data_file = "data002v.txt"
default_data_file = "neh.data.txt"
dataset_index = 20

data = read_data_file(data_dir+default_data_file, dataset_index+1, no_names=False)[dataset_index]


method = "inverse"
tabu_len = 10
n_neighbours = 50
cond = IterationsCondition(1000)

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
                  init_scheduling_func=johnson_rule_multiple,
                  neighbour_method="swap",
                  tabu_len=15,
                  n_neighbours=100,
                  stopping_condition=IterationsCondition(50)))
print(t.stop())
