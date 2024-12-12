import numpy as np

class Image:

    def __init__(self, letter, x=0, y=0):

        self.letters_dict = {
            "O": [[1, 2, 5, 6]], # OK
            "I": [[1, 5, 9, 13], [0, 1, 2, 3]], # OK
            "S": [[6, 5, 9, 8], [5, 9, 10, 14]],
            "Z": [[1, 2, 6, 7], [2, 5, 6, 9]], # OK
            "L": [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [3, 2, 1, 5]], # OK
            "J": [[2, 6, 9, 10], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]],
            "T": [[1, 5, 6, 9], [1, 4, 5, 6], [2, 5, 6, 10], [1, 2, 3, 6]] # OK
        }
        self.letter = letter
        self.rotation = 0
        self.x = x
        self.y = y

    def rotate(self):
        if self.rotation >= (len(self.letters_dict[self.letter]) - 1):
            self.rotation = 0
        else:
            self.rotation += 1

    def image(self):
        return self.letters_dict[self.letter][self.rotation]


class TetrisGame:

    def __init__(self, height=20, width=10):

        self.height = height
        self.width = width
        self.empty_grid()

    def empty_grid(self):
        self.grid = self.return_empty_grid()

    def return_empty_grid(self):
        pregrid = np.repeat(["-"], self.height * self.width)
        return pregrid.reshape(self.height, self.width)

    def put_letter_in_grid(self, image_obj):
        image_seq = image_obj.image()
        for i in range(len(image_seq)):

            x = int(image_seq[i] % 4)
            y = int(image_seq[i] // 4)
            #x = int(image_seq[i] % self.width)
            #y = int(image_seq[i] // self.width)
            x_r = x + image_obj.x
            y_r = y + image_obj.y

            if y_r < 0 or y_r >= self.height or x_r < 0 or x_r >= self.width:
                pass
            else:
                self.grid[y_r, x_r] = "0"

    def print_grid(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += self.grid[y, x] + " "
            print(line)

    def go_rotate(self, image_obj):
        image_obj.rotate()
        image_obj.y += 1

    def go_down(self, image_obj):
        image_obj.y += 1

    def go_left(self, image_obj):
        image_obj.y += 1
        image_obj.x += -1

    def go_right(self, image_obj):
        image_obj.y += 1
        image_obj.x += 1

    def show_grid(self, image_obj):
        ## empty grid
        self.empty_grid()
        self.print_grid()
        print()

    def show_letter(self, image_obj):
        ## last down moved grid as the first in list
        print()
        self.empty_grid()
        self.put_letter_in_grid(image_obj)
        self.print_grid()
        print()



def main():

    letter = str(input())
    w, h = str(input()).split()
    print()

    image = Image(letter, 3, 0)
    t1 = TetrisGame(int(h), int(w))

    t1.show_grid(image)
    t1.show_letter(image)

    while True:
        command = str(input())
        if command == "rotate":
            t1.go_rotate(image)
            t1.show_letter(image)
        elif command == "right":
            t1.go_right(image)
            t1.show_letter(image)
        elif command == "left":
            t1.go_left(image)
            t1.show_letter(image)
        elif command == "down":
            t1.go_down(image)
            t1.show_letter(image)
        elif command == "exit":
            break
    exit()


if __name__ == "__main__":
    main()
