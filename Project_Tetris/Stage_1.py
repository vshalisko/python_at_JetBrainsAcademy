import numpy as np

class TetrisGame:

    def __init__(self):
        self.letters_dict = {
            "O": [[5, 6, 9, 10], [5, 6, 9, 10], [5, 6, 9, 10], [5, 6, 9, 10]],
            "I": [[1, 5, 9, 13], [4, 5, 6, 7], [1, 5, 9, 13], [4, 5, 6, 7]],
            "S": [[6, 5, 9, 8], [5, 9, 10, 14], [6, 5, 9, 8], [5, 9, 10, 14]],
            "Z": [[4, 5, 9, 10], [2, 5, 6, 9], [4, 5, 9, 10], [2, 5, 6, 9]],
            "L": [[1, 5, 9, 10], [5, 9, 10, 11], [1, 2, 6, 10], [4, 5, 6, 8]],
            "J": [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]],
            "T": [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
        }
        self.empty_grid()

    def empty_grid(self):
        self.grid = np.repeat(['-'], 16)

    def put_letter_in_grid(self, letter, rotation):
        for i in range(len(self.letters_dict[letter][rotation])):
            self.grid[self.letters_dict[letter][rotation][i]] = "0"

    def print_grid(self):
        for i in range(4):
            print("{} {} {} {}".format(
                self.grid[i * 4 + 0],
                self.grid[i * 4 + 1],
                self.grid[i * 4 + 2],
                self.grid[i * 4 + 3]
            ))

    def show_rotations(self, letter):

        ## empty grid
        self.empty_grid()
        self.print_grid()
        print()

        ## all grids in list
        for r in range(len(self.letters_dict[letter])):
            self.empty_grid()
            self.put_letter_in_grid(letter, r)
            self.print_grid()
            print()

        ## last grid as the first in list
        self.empty_grid()
        self.put_letter_in_grid(letter, 0)
        self.print_grid()

        return


def main():

    letter = str(input())
    if letter == "exit":
        exit()
    else:
        t1 = TetrisGame()
        t1.show_rotations(letter)


if __name__ == "__main__":
    main()
