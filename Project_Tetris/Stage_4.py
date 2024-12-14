import numpy as np

class Image:

    def __init__(self, letter, x=0, y=0):

        self.letters_dict = {
            "NO": [[]],
            "O": [[1, 2, 5, 6]],
            "I": [[1, 5, 9, 13], [0, 1, 2, 3]],
            "S": [[1, 2, 4, 5], [1, 5, 6, 10]],
            "Z": [[1, 2, 6, 7], [2, 5, 6, 9]],
            "L": [[1, 5, 9, 10], [2, 4, 5, 6], [1, 2, 6, 10], [3, 2, 1, 5]],
            "J": [[2, 6, 9, 10], [0, 1, 2, 6], [1, 2, 5, 9], [1, 5, 6, 7]],
            "T": [[1, 5, 6, 9], [1, 4, 5, 6], [2, 5, 6, 10], [1, 2, 3, 6]]
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
        self.next = True

        ## temporal grid for moving piece
        self.empty_grid()
        ## permanent grid for fixed pieces
        self.empty_memory_grid()

    def empty_grid(self):
        self.grid = self.return_empty_grid()

    def test_grid(self):
        self.test_grid = self.return_empty_grid()

    def empty_memory_grid(self):
        self.memory_grid = self.return_empty_grid()

    def return_empty_grid(self):
        pre_grid = np.repeat(["-"], self.height * self.width)
        return pre_grid.reshape(self.height, self.width)

    def put_letter_in_grid(self, image_obj, memory=False):
        image_seq = image_obj.image()
        for i in range(len(image_seq)):

            x = int(image_seq[i] % 4)
            y = int(image_seq[i] // 4)
            x_r = x + image_obj.x
            y_r = y + image_obj.y

            if y_r < 0 or y_r >= self.height or x_r < 0 or x_r >= self.width:
                pass
            else:
                if memory:
                    self.memory_grid[y_r, x_r] = "0"
                else:
                    self.grid[y_r, x_r] = "0"

    def test_letter_conflict(self, image_obj, dx, dy):
        conflict = False
        image_seq = image_obj.image()
        for i in range(len(image_seq)):

            x = int(image_seq[i] % 4)
            y = int(image_seq[i] // 4)
            x_r = x + image_obj.x + dx
            y_r = y + image_obj.y + dy

            if self.memory_grid[y_r, x_r] == "0":
                conflict = True
        return conflict

    def print_grid(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width - 1):
                if self.memory_grid[y, x] == "0":
                    line += self.memory_grid[y, x] + " "
                else:
                    line += self.grid[y, x] + " "
            if self.memory_grid[y, self.width - 1] == "0":
                line += self.memory_grid[y, self.width - 1]
            else:
                line += self.grid[y, self.width - 1]
            print(line)

    def go_rotate(self, image_obj):
        if self.border_down(image_obj):
            ## stuck in bottom
            self.put_letter_in_grid(image_obj, True)
            self.next = True
        else:
            image_obj.rotate()
            if self.test_letter_conflict(image_obj, 0, 1):
                ## chock with other pieces -> turn to memory_grid & erase piece
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                image_obj.y += 1

    def go_down(self, image_obj):
        if self.border_down(image_obj):
            ## stuck in bottom
            self.put_letter_in_grid(image_obj, True)
            self.next = True
        else:
            if self.test_letter_conflict(image_obj, 0, 1):
                ## chock with other pieces -> turn to memory_grid & erase piece
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                image_obj.y += 1


    def go_left(self, image_obj):
        if self.border_left(image_obj):
            if self.border_down(image_obj):
                ## stuck in bottom
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                if self.test_letter_conflict(image_obj, 0, 1):
                    ## chock with other pieces -> turn to memory_grid & erase piece
                    self.put_letter_in_grid(image_obj, True)
                    self.next = True
                else:
                    image_obj.y += 1
        else:
            if self.border_down(image_obj):
                ## stuck in bottom
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                if self.test_letter_conflict(image_obj, -1, 1):
                    ## chock with other pieces -> turn to memory_grid & erase piece
                    self.put_letter_in_grid(image_obj, True)
                    self.next = True
                else:
                    image_obj.y += 1
                    image_obj.x += -1

    def go_right(self, image_obj):
        if self.border_right(image_obj):
            if self.border_down(image_obj):
                ## stuck in bottom
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                if self.test_letter_conflict(image_obj, 0, 1):
                    ## chock with other pieces -> turn to memory_grid & erase piece
                    self.put_letter_in_grid(image_obj, True)
                    self.next = True
                else:
                    image_obj.y += 1
        else:
            if self.border_down(image_obj):
                ## stuck in bottom
                self.put_letter_in_grid(image_obj, True)
                self.next = True
            else:
                if self.test_letter_conflict(image_obj, 1, 1):
                    ## chock with other pieces -> turn to memory_grid & erase piece
                    self.put_letter_in_grid(image_obj, True)
                    self.next = True
                else:
                    image_obj.y += 1
                    image_obj.x += 1

    def show_grid(self):
        ## empty grid
        self.empty_grid()
        self.print_grid()
        print()

    def show_letter(self, image_obj):
        print()
        self.empty_grid()
        self.put_letter_in_grid(image_obj)
        self.print_grid()
        print()

    def border_left(self, image_obj):

        border_touch = False
        image_seq = image_obj.image()
        for i in range(len(image_seq)):
            x = int(image_seq[i] % 4)
            x_r = x + image_obj.x
            if x_r < 1:
                border_touch = True
        return border_touch

    def border_right(self, image_obj):

        border_touch = False
        image_seq = image_obj.image()
        for i in range(len(image_seq)):
            x = int(image_seq[i] % 4)
            x_r = x + image_obj.x
            if x_r >= (self.width - 1):
                border_touch = True
        return border_touch

    def border_down(self, image_obj):

        border_touch = False
        image_seq = image_obj.image()
        for i in range(len(image_seq)):
            y = int(image_seq[i] // 4)
            y_r = y + image_obj.y
            if y_r >= (self.height - 1):
                border_touch = True
        return border_touch

    def check_end_game(self):
        end_game = False
        for i in range(self.width):
            if self.memory_grid[0, i] == "0":
                end_game = True
        return end_game

    def remove_full_lines(self):
        for y in range(self.height):
            counter = 0
            for x in range(self.width):
                if self.memory_grid[y, x] == "0":
                    counter += 1
            if counter == self.width:
                ## line to remove
                for y_above in range(1, y):
                    self.memory_grid[y - y_above + 1, ] = self.memory_grid[y - y_above,]
                for i in range(self.width):
                    self.memory_grid[0, i] = "-"
                #print()
                #self.print_grid()




def main():
    w, h = str(input()).split()
    print()

    t1 = TetrisGame(int(h), int(w))
    t1.show_grid()

    image = Image("NO", 3, 0)

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
        elif command == "piece":
            letter = str(input())
            image = Image(letter, 3, 0)
            t1.next = False
            t1.show_letter(image)
        elif command == "break":
            t1.remove_full_lines()
            t1.print_grid()
        elif command == "exit":
            break

        if t1.next:
            ## generate empty image
            t1.empty_grid()
            image = Image("NO", 3, 0)

        if t1.check_end_game():
            print("Game Over!")
            break

    exit()


if __name__ == "__main__":
    main()
