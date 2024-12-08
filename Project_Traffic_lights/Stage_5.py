import time
from threading import Thread

class Traffic:

    def __init__(self):
        print("Welcome to the traffic management system!")
        self.state = 5 # initial menu
        self.road_names = []
        pre_input = str(input("Input the number of roads:"))
        while True:
            if pre_input.isdigit() and int(pre_input) > 0:
                self.road = int(pre_input)
                break
            else:
                pre_input = str(input("Incorrect input. Try again."))

        pre_input1 = str(input("Input the interval:"))
        while True:
            if pre_input1.isdigit() and int(pre_input1) > 0:
                self.interval = int(pre_input1)
                break
            else:
                pre_input1 = str(input("Incorrect input. Try again."))

        self.thread_system = Thread(target=self.system_state)
        self.thread_system.setName("QueueThread")
        self.thread_system.start()


    def system_state(self):
        self.start_time = time.time()
        while True:
            if self.state == 0:
                break
            time.sleep(1)
            new_cur_time = time.time()
            time_passed = int(new_cur_time - self.start_time)
            if self.state == 3:
                print("! {}s. have passed since system startup !".format(time_passed))
                print("! Number of roads: {} !".format(self.road))
                print("! Interval: {} !".format(self.interval))
                if len(self.road_names) > 0:
                    print("")
                    for road_name in self.road_names:
                        print(road_name)
                    print("")
                print('! Press "Enter" to open menu !')


    def app_menu(self):

        if self.state != 3:
            print("Menu:")              # initial menu (state 5)
            print("1. Add road")
            print("2. Delete road")
            print("3. Open system")
            print("0. Quit")

        pre_input2 = str(input())
        while True:
            if self.state == 3 and pre_input2 == "":
                menu_level = 5
                self.state = 5
                break
            if pre_input2.isdigit() and int(pre_input2) in [0, 1, 2, 3]:
                menu_level = int(pre_input2)
                self.state = menu_level
                break
            else:
                print("Incorrect option.")
                menu_level = 5
                input()
                break
        return menu_level

    def add_road(self):
        road_name = str(input("Input road name:"))
        if len(self.road_names) < self.road:
            self.road_names.append(road_name)
            print("{} Added!".format(road_name))
        else:
            print("Queue is full")
        input()

    def delete_road(self):
        if len(self.road_names) > 0:
            deleted_road = self.road_names.pop(0)
            print("{} deleted!".format(deleted_road))
        else:
            print("queue is empty")
        input()

def main():
    app = Traffic()

    while True:
        mode = app.app_menu()
        if mode == 0:
            print("Bye!")
            app.thread_system.join()
            break
        elif mode == 1:
            app.add_road()
        elif mode == 2:
            app.delete_road()

        elif mode == 3:
            #print("System opened")
            pass
        #input()

if __name__ == "__main__":
    main()
