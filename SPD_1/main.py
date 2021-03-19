from scheduling1 import *


dummy = read_data_file("test.data.txt", 2)[1]
if verify_dataset(dummy):
    print(bruteforce(dummy))
    gantt_chart(dummy)
    print(johnson_rule_multiple(dummy))
    gantt_chart(dummy)
else:
    print("Dataset is not in correct format!")
