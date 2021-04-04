import scheduling_1

set_index = 0
data_dir = "data/"
default_data_file = "data002v.txt"


ans = True
while ans:
    if not default_data_file:
        file_name = "data/" + str(input("Enter name of the data file: "))
    else:
        file_name = data_dir + default_data_file
    dummy = scheduling_1.read_data_file(file_name, set_index+1, no_names=True)[set_index]
    print("""
    0.Exit/Quit
    1.Bruteforce
    2.Johnson rule
    3.Naive scheduling
    """)
    ans = int(input("What would you like to do? "))
    if ans == 0:
        print("/n Goodbye")
    elif ans == 1:
        if scheduling_1.verify_dataset(dummy):
            print("Cmax: ", scheduling_1.bruteforce(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 2:
        if scheduling_1.verify_dataset(dummy):
            print("Cmax: ", scheduling_1.johnson_rule_multiple(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 3:
        if scheduling_1.verify_dataset(dummy):
            print("Cmax: ", scheduling_1.naive(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    else:
        print("\n Not valid choice try again")
