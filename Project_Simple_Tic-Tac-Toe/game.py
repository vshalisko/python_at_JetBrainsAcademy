def print_field(state):
    horizontal = "---------"
    st = list(state)
    print(horizontal)
    print("| {} {} {} |".format(st[0],st[1],st[2]))
    print("| {} {} {} |".format(st[3],st[4],st[5]))
    print("| {} {} {} |".format(st[6],st[7],st[8]))
    print(horizontal)

def check_row(s, p, i):
    r = False
    if s[i] == p and s[i+1] == p and s[i+2] == p:
        r = True
    return(r)

def check_col(s, p, i):
    r = False
    if s[i] == p and s[i+3] == p and s[i+6] == p:
        r = True
    return(r)

def check_diag(s, p):
    r = False
    if s[0] == p and s[4] == p and s[8] == p:
        r = True
    if s[2] == p and s[4] == p and s[6] == p:
        r = True        
    return(r)
    

def game_state(state):
    end_game = False
    s = list(state)
    if abs(s.count('X') - s.count('O')) > 1:
        print("Impossible")
        end_game = True
    elif check_row(s, "X", 0) or check_row(s, "X", 3) or check_row(s, "X", 6):
        if check_row(s, "O", 0) or check_row(s, "O", 3) or check_row(s, "O", 6):
            print("Impossible")
            end_game = True
        else:
            print("X wins")
            end_game = True
    elif check_col(s, "X", 0) or check_col(s, "X", 1) or check_col(s, "X", 2):
        if check_col(s, "O", 0) or check_col(s, "O", 1) or check_col(s, "O", 2):
            print("Impossible")
            end_game = True
        else:
            print("X wins")
            end_game = True
    elif check_row(s, "O", 0) or check_row(s, "O", 3) or check_row(s, "O", 6):
        if check_row(s, "X", 0) or check_row(s, "X", 3) or check_row(s, "X", 6):
            print("Impossible")
            end_game = True
        else:
            print("O wins")
            end_game = True
    elif check_col(s, "O", 0) or check_col(s, "O", 1) or check_col(s, "O", 2):
        if check_col(s, "X", 0) or check_col(s, "X", 1) or check_col(s, "X", 2):
            print("Impossible")
            end_game = True
        else:
            print("O wins")
            end_game = True
    elif check_diag(s, "X"):
        print("X wins")
        end_game = True
    elif check_diag(s, "O"):
        print("O wins")
        end_game = True
    elif s.count('X') + s.count('O') < 9:
        #print("Game not finished")
        end_game = False
    elif s.count('X') + s.count('O') == 9:
        print("Draw")
        end_game = True
    return(end_game)

def request_move(state, p):
    new_state = ""
    while True:
        move = str(input())
        try:
            move_list = move.split(" ")
        except Exception:
            print("You should enter numbers!")
            continue
        else:
            if len(move_list) == 2:
                try:
                    coord_x = int(move_list[1])
                    coord_y = int(move_list[0])
                except ValueError:
                    print("You should enter numbers!")
                    continue
                else:
                    if coord_x < 1 or coord_x > 3 or coord_y < 1 or coord_y > 3:
                        print("Coordinates should be from 1 to 3!")
                        continue
                    else:
                        ## check if cell is occupied
                        ind = 3 * (coord_y - 1) + (coord_x - 1)
                        s = list(state)
                        if s[ind] == "X" or s[ind] == "O":
                            print("This cell is occupied!")
                            continue
                        else:
                            s[ind] = p
                            new_state = "".join(s)
                            break
            else:
                print("You should enter numbers!")
                continue                
    return(new_state)                
    
state_input = "_________"
#state_input = str(input())
print_field(state_input)

fin = False
i = 0

while not fin:
    i += 1
    if i % 2:
        new_state = request_move(state_input, "O")
    else:
        new_state = request_move(state_input, "X")
    print_field(new_state)
    fin = game_state(new_state)
    state_input = new_state
