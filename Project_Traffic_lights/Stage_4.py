
class Traffic:

    def __init__(self):
        print("Welcome to the traffic management system!")
        pre_input = str(input("Input the number of roads:"))
        while True:
            if pre_input.isdigit() and int(pre_input) > 0:
                self.road = pre_input
                break
            else:
                pre_input = str(input("Incorrect input. Try again."))

        pre_input1 = str(input("Input the interval:"))
        while True:
            if pre_input1.isdigit() and int(pre_input1) > 0:
                self.interval = pre_input1
                break
            else:
                pre_input1 = str(input("Incorrect input. Try again."))

    def menu(self):

        print("Menu:")
        print("1. Add road")
        print("2. Delete road")
        print("3. Open system")
        print("0. Quit")

        pre_input2 = str(input())
        while True:
            if pre_input2.isdigit() and int(pre_input2) in [0, 1, 2, 3]:
                menu_level = int(pre_input2)
                break
            else:
                print("Incorrect option.")
                menu_level = 5
                break

        return menu_level



def main():
    app = Traffic()

    while True:
        mode = app.menu()
        if mode == 0:
            print("Bye!")
            break
        elif mode == 1:
            print("Road added")
        elif mode == 2:
            print("Road deleted")
        elif mode == 3:
            print("System opened")
        input()

if __name__ == "__main__":
    main()
