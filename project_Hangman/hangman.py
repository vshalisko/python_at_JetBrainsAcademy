import random
import string
random.seed()

def string_masking(previous_mask, selected_word, letter):
    new_finding = 0
    old_findong = 0
    incorrect_letter = 1
    new_mask_list = []
    previous_mask_list = list(previous_mask)
    selected_word_list = list(selected_word)
    #print(selected_word_list)
    letter_length = range(len(selected_word))
    for i in letter_length:
        if letter == selected_word_list[i]:
            incorrect_letter = 0
            if letter == previous_mask_list[i]:
                old_finding = 1
                print("No improvements.")
            else:
                new_finding = 1
                #print("")
            new_mask_list.append(letter)
        else:
            new_mask_list.append(previous_mask_list[i])
            #if previous_mask_list[i] == "-":
                
    new_mask = "".join(new_mask_list)
    if (incorrect_letter == 1):
        print("That letter doesn't appear in the word.")
    return(new_mask)

def check_input(inp):
    inp_ok = False
    if len(inp) > 1 or len(inp) < 1:
        print("Please, input a single letter.")
    elif inp not in string.ascii_letters:
        print("Please, enter a lowercase letter from the English alphabet.")
    elif inp not in string.ascii_lowercase:
        print("Please, enter a lowercase letter from the English alphabet.")
    else:
        inp_ok = True
    return(inp_ok)

def game():
    global won_counter
    global loss_counter
    global word_options
    selected_word = random.choice(word_options)
    word_mask = "-" * len(selected_word)

    attempt_counter = 8
    letter_set = set()

    while attempt_counter > 0:
        print(word_mask)
        letter = str(input("Input a letter:"))
        if not check_input(letter):
            continue
        if letter in letter_set:
            print("You've already guessed this letter.")
            continue
        new_word_mask = string_masking(word_mask, selected_word, letter)
        if word_mask == new_word_mask:
            ## unsuccessfull attempt
            letter_set.add(letter)
            attempt_counter -= 1
        else:
            ## succesfull attempt, store letter
            letter_set.add(letter)
        word_mask = new_word_mask
        if word_mask == selected_word:
            print("\n","You guessed the word {}!".format(selected_word),"You survived!")
            won_counter += 1
            #break
            attempt_counter = 0
    
    if word_mask != selected_word:
        print("\n","You lost!")
        loss_counter += 1

print("H A N G M A N")

won_counter = 0
loss_counter = 0
word_options = ["python", "java", "swift", "javascript"]

while True:
    print('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:',"\n")
    menu_input = str(input())
    if menu_input == "exit":
        break
    elif menu_input == "results":
        print("You won: {} times.".format(str(won_counter)))
        print("You lost: {} times.".format(str(loss_counter)))
    elif menu_input == "play":
        ## game
        game()
        
