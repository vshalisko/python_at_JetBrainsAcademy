import string

print("How many pencils would you like to use:")
while True:
    number = str(input())
    if not number.isnumeric():
        print("The number of pencils should be numeric")
        continue
    number = int(number)    
    if number <= 0:
        print("The number of pencils should be positive")
        continue
    break

name_1 = "Slava"
name_2 = "Bot"
print("Who will be the first ({},{})".format(name_1, name_2))
while True:
    name = str(input())
    if name not in [name_1,name_2]:
        print("Choose between '{}' and '{}'".format(name_1, name_2))
        continue
    break

if name == name_1:
    candidate_winner = name_2
else:
    candidate_winner = name_1

def bot_turn(remaining_pencils):
    if remaining_pencils == 1:
        ## losing
        return "1"
    elif remaining_pencils == 5:
        ## losing
        return "2"        
    elif remaining_pencils == 9:
        ## losing
        return "3"
    elif remaining_pencils % 4 == 0:
        return "3"    
    elif (remaining_pencils + 1) % 4 == 0:
        return "2"          
    elif (remaining_pencils + 2) % 4 == 0:
        return "1"          
    else:
        return "1"

while True:
    pencils = "|" * number    
    print(pencils)
    print("{}'s turn:".format(name))
    remove_pencils = 0
    while True:
        if name == name_2:
            ## bot turn
            remove_pencils = bot_turn(number)
            print(remove_pencils)
        else:
            ## user turn
            remove_pencils = str(input())
        if remove_pencils not in ["1","2","3"]:
            print("Possible values: '1', '2' or '3'")
            continue
        remove_pencils = int(remove_pencils)
        if remove_pencils > number:
            print("Too many pencils were taken")
            continue
        break
    number = number - remove_pencils
    if number <= 0:
        print("{} won!".format(candidate_winner))
        break
    else:
        if name == name_1:
            name = name_2
            candidate_winner = name_1
        else:
            name = name_1
            candidate_winner = name_2
