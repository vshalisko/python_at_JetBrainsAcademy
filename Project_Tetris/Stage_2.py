import numpy as np

class TetrisGame:

    def __init__(self, height=20, width=10):
        self.letters_dict = {
            "O": [[4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5]],
            "I": [[4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34], [3, 4, 5, 6]],
            "S": [[5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13], [4, 14, 15, 25]],
            "Z": [[4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16], [5, 15, 14, 24]],
            "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
            "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
            "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        }
        self.height = height
        self.width = width
        self.empty_grid()

    def empty_grid(self):
        pregrid = np.repeat(['-'], self.height * self.width)
        self.grid = pregrid.reshape(self.height, self.width)

    def put_letter_in_grid(self, letter, rotation):
        for i in range(len(self.letters_dict[letter][rotation])):
            x = int(self.letters_dict[letter][rotation][i] % self.width)
            y = int(self.letters_dict[letter][rotation][i] // self.width)
            self.grid[y, x] = "0"

    def print_grid(self):
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += self.grid[i, j]
            print(line)

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
        print(self.grid)

        return


def main():

    letter = str(input())
    if letter == "exit":
        exit()
    else:
        t1 = TetrisGame(5, 10)
        t1.show_rotations(letter)


if __name__ == "__main__":
    main()
