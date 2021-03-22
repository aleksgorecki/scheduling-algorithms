import scheduling_1


dummy = scheduling_1.read_data_file("data/test.data.txt", 2)[1]
if scheduling_1.verify_dataset(dummy):
    print(scheduling_1.johnson_rule_multiple(dummy))
    scheduling_1.gantt_chart(dummy)
else:
    print("Dataset is not in correct format!")
