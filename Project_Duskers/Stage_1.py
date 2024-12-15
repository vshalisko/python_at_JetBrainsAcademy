class Game:

    def __init__(self):
        print("""
+=======================================================================+
  ######*   ##*   ##*  #######*  ##*  ##*  #######*  ######*   #######*
  ##*  ##*  ##*   ##*  ##*       ##* ##*   ##*       ##*  ##*  ##*
  ##*  ##*  ##*   ##*  #######*  #####*    #####*    ######*   #######*
  ##*  ##*  ##*   ##*       ##*  ##* ##*   ##*       ##*  ##*       ##*
  ######*    ######*   #######*  ##*  ##*  #######*  ##*  ##*  #######*
                      (Survival ASCII Strategy Game)
+=======================================================================+
        """)

    def menu(self):
        print("[Play]")
        print("[Exit]")

        command = ""
        Temporary = True
        #while True:
        while Temporary:
            print("\nYour command:")
            Temporary = False
            command = str(input())
            if command not in {"play", "exit"}:
                print("Invalid input")
            if command == "exit":
                self.exit()
                break
            if command == "play":
                self.play()
                break

    def play(self):
        print("\nEnter your name:")
        name = str(input())
        print("\nGreetings, commander {}!".format(name))

        while True:
            print("Are you ready to begin?")
            print("    [Yes] [No]")
            print("\nYour command:")
            g_command = str(input())
            if g_command not in {"you", "no"}:
                print("Invalid input")
            if g_command == "yes":
                print("\nGreat, now let's go code some more ;)")
                break
            if g_command == "no":
                print("\nHow about now.")

    def exit(self):
        print("Thanks for playing, bye!")

def main():
    g1 = Game()
    g1.menu()
    exit()


if __name__ == "__main__":
    main()
