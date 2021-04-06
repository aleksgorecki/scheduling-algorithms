import scheduling_2
import csv
from timer import Timer
from dict import Dict


t = Timer()
set_index = 0
data_dir = "data/"
default_data_file = "neh.data.txt"
fieldnames = ['name', 'johnson_c', 'johnson_t', 'neh_c', 'neh_t', 'neh1_c', 'neh1_t', 'neh2_c', 'neh2_t', 'neh3_c', 'neh3_t', 'neh4_c', 'neh4_t']
dataList = []

setname = 'set' + str(set_index)
set = Dict(setname)
dataList.append(set)

ans = True
while ans:
    if not default_data_file:
        file_name = "data/" + str(input("Enter name of the data file: "))
    else:
        file_name = data_dir + default_data_file
    dummy = scheduling_2.read_data_file(file_name, set_index+1, no_names=False)[set_index]
    print("""
    0.Exit/Quit
    1.Bruteforce
    2.Johnson rule
    3.Naive scheduling
    4.NEH
    5.Save to csv
    """)
    ans = int(input("What would you like to do? "))
    if ans == 0:
        print("/n Goodbye")
    elif ans == 1:
        if scheduling_2.verify_dataset(dummy):
            print("Cmax: ", scheduling_2.bruteforce(dummy))
            print(dummy.schedule)
            scheduling_2.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 2:
        if scheduling_2.verify_dataset(dummy):
            t.start()
            cmax=scheduling_2.johnson_rule_multiple(dummy)
            ctime = t.stop()
            dataList[0].setJohnson(cmax, ctime)
            print(dataList[0].getdict())
            print("Cmax: ", cmax)
            print(ctime)
            print(dummy.schedule)
            #scheduling_2.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 3:
        if scheduling_2.verify_dataset(dummy):
            print("Cmax: ", scheduling_2.naive(dummy))
            print(dummy.schedule)
            scheduling_2.gantt_chart(dummy)
        else:
            print("Dataset is not in correct format!")
    elif ans == 4:
        if scheduling_2.verify_dataset(dummy):
            t.start()
            cmaxn = scheduling_2.neh(dummy)
            ctimen = t.stop()
            print("Cmax0: ", cmaxn)
            print(dummy.schedule)
            #scheduling_2.gantt_chart(dummy)
            t.start()
            cmaxn1 = scheduling_2.neh1(dummy)
            ctimen1 = t.stop()
            print("Cmax1: ", cmaxn1)
            print(dummy.schedule)
            #scheduling_2.gantt_chart(dummy)
            t.start()
            cmaxn2 = scheduling_2.neh2(dummy)
            ctimen2 = t.stop()
            print("Cmax2: ", cmaxn2)
            print(dummy.schedule)
            #scheduling_2.gantt_chart(dummy)
            t.start()
            cmaxn3 = scheduling_2.neh3(dummy)
            ctimen3 = t.stop()
            print("Cmax3: ", cmaxn3)
            print(dummy.schedule)
            #scheduling_2.gantt_chart(dummy)
            t.start()
            cmaxn4 = scheduling_2.neh4(dummy)
            ctimen4 = t.stop()
            print("Cmax3: ", cmaxn4)
            print(dummy.schedule)
            dataList[0].setNeh(cmaxn, ctimen, cmaxn1, ctimen1, cmaxn2, ctimen2, cmaxn3, ctimen3, cmaxn4, ctimen4)
            print(dataList[0].getdict())
        else:
            print("Dataset is not in correct format!")

    elif ans == 5:
        with open('table.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(dataList[0].getdict())
    else:
        print("\n Not valid choice try again")
    #ans = False
