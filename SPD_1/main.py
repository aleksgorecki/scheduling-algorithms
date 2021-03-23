import scheduling_1

ans = True
while ans:
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
        file_name = "data/" + str(input("Enter name of the data file: "))
        dummy = scheduling_1.read_data_file(file_name, 1)[0]
        if scheduling_1.verify_dataset(dummy):
            print(scheduling_1.bruteforce(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 2:
        file_name = "data/" + str(input("Enter name of the data file: "))
        dummy = scheduling_1.read_data_file(file_name, 1)[0]
        if scheduling_1.verify_dataset(dummy):
            print(scheduling_1.johnson_rule_multiple(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 3:
        file_name = "data/" + str(input("Enter name of the data file: "))
        dummy = scheduling_1.read_data_file(file_name, 1)[0]
        if scheduling_1.verify_dataset(dummy):
            print(scheduling_1.naive(dummy))
            scheduling_1.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    else:
        print("\n Not valid choice try again")
