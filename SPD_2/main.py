import scheduling_2
import csv
from timer import Timer
from dict import Dict

t = Timer()
data_dir = "data/"
default_data_file = "neh.data.txt"
fieldnames = ['name', 'johnson_c', 'johnson_t', 'neh_c', 'neh_t', 'neh1_c', 'neh1_t', 'neh2_c', 'neh2_t', 'neh3_c', 'neh3_t', 'neh4_c', 'neh4_t']
set_index2 = -1

menu = True
ans = True
while menu:
    if not default_data_file:
        file_name = "data/" + str(input("Enter name of the data file: "))
    else:
        file_name = data_dir + default_data_file
    print("""
        0.Exit/Quit
        1.Save to csv
        2.Old menu
        """)
    menu = int(input("What would you like to do? "))
    if menu == 0:
        print("/n Goodbye")
    elif menu == 1:
        dataList = []
        set_index = int(input("Enter number of sets: "))
        l_dummy = scheduling_2.read_data_file(file_name, set_index + 1, no_names=False)
        counter = 0
        for set_of_dummy in l_dummy:
            # setname = str(set_of_dummy.getname())
            setname = 'set' + str(counter)
            dataList.append(Dict(setname))

            # johnson
            if scheduling_2.verify_dataset(set_of_dummy):
                t.start()
                cmax = scheduling_2.johnson_rule_multiple(set_of_dummy)
                ctime = t.stop()
                dataList[counter].setJohnson(cmax, ctime)
                # print(dataList[counter].getdict())
                # print("Cmax: ", cmax)
                # print(ctime)
                # print(set_of_dummy.schedule)
                # scheduling_2.gantt_chart(set_of_dummy)
            else:
                print("Dataset is not in correct format!")

            # neh
            if scheduling_2.verify_dataset(set_of_dummy):
                t.start()
                cmaxn = scheduling_2.neh(set_of_dummy)
                ctimen = t.stop()
                t.start()
                cmaxn1 = scheduling_2.neh1(set_of_dummy)
                ctimen1 = t.stop()
                t.start()
                cmaxn2 = scheduling_2.neh2(set_of_dummy)
                ctimen2 = t.stop()
                t.start()
                cmaxn3 = scheduling_2.neh3(set_of_dummy)
                ctimen3 = t.stop()
                t.start()
                cmaxn4 = scheduling_2.neh4(set_of_dummy)
                ctimen4 = t.stop()
                dataList[counter].setNeh(cmaxn, ctimen, cmaxn1, ctimen1, cmaxn2, ctimen2, cmaxn3, ctimen3, cmaxn4,
                                         ctimen4)
            else:
                print("Dataset is not in correct format!")
            counter += 1

        counter = 0
        # save
        with open('table.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for number in range(0, set_index):
                #writer.writeheader()
                writer.writerow(dataList[number].getdict())

    elif menu == 2:
        while ans:
            if set_index2 == -1:
                set_index2 = int(input("Enter number of set: "))
                dataList2 = []
                setname = 'set' + str(set_index2)
                dataList2.append(Dict(setname))

            dummy = scheduling_2.read_data_file(file_name, set_index2 + 1, no_names=False)[set_index2]
            print("""
            0.Back to main menu
            1.Bruteforce
            2.Johnson rule
            3.Naive scheduling
            4.NEH
            5.Save to csv
            6.Enter set number
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
                    cmax = scheduling_2.johnson_rule_multiple(dummy)
                    ctime = t.stop()
                    dataList2[0].setJohnson(cmax, ctime)
                    print("Cmax: ", cmax)
                    print("Time: ", ctime)
                    print(dummy.schedule)
                    # scheduling_2.gantt_chart(dummy)
                    print(dataList2[0].getdict())
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
                    print("Time0: ", ctimen)
                    print(dummy.schedule)
                    # scheduling_2.gantt_chart(dummy)
                    t.start()
                    cmaxn1 = scheduling_2.neh1(dummy)
                    ctimen1 = t.stop()
                    print("Cmax1: ", cmaxn1)
                    print("Time1: ", ctimen1)
                    print(dummy.schedule)
                    # scheduling_2.gantt_chart(dummy)
                    t.start()
                    cmaxn2 = scheduling_2.neh2(dummy)
                    ctimen2 = t.stop()
                    print("Cmax2: ", cmaxn2)
                    print("Time2: ", ctimen3)
                    print(dummy.schedule)
                    # scheduling_2.gantt_chart(dummy)
                    t.start()
                    cmaxn3 = scheduling_2.neh3(dummy)
                    ctimen3 = t.stop()
                    print("Cmax3: ", cmaxn3)
                    print("Time3: ", ctimen3)
                    print(dummy.schedule)
                    # scheduling_2.gantt_chart(dummy)
                    t.start()
                    cmaxn4 = scheduling_2.neh4(dummy)
                    ctimen4 = t.stop()
                    print("Cmax4: ", cmaxn4)
                    print("Time4: ", ctimen4)
                    print(dummy.schedule)
                    dataList2[0].setNeh(cmaxn, ctimen, cmaxn1, ctimen1, cmaxn2, ctimen2, cmaxn3, ctimen3, cmaxn4,
                                       ctimen4)
                    print(dataList2[0].getdict())
                else:
                    print("Dataset is not in correct format!")

            elif ans == 5:
                with open('table.csv', mode='w') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(dataList2[0].getdict())
            elif ans == 6:
                set_index2 = int(input("Enter number of set: "))
                dataList2 = []
                setname = 'set' + str(set_index2)
                dataList2.append(Dict(setname))
            else:
                print("\n Not valid choice try again")
    else:
        print("\n Not valid choice try again")



    #ans = False
