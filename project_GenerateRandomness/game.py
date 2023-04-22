# stage 4
import random

print("Please provide AI some data to learn...")
print("The current data length is 0, 100 symbols left")

final_string = ""
while len(final_string) < 100:
    print("Print a random string containing 0 or 1:")
    my_string = str(input())
    my_string = ''.join(c for c in my_string if c in ["0","1"])
    final_string += my_string
    my_string_len = len(final_string)
    if (my_string_len < 100):
        print("Current data length is {}, {} symbols left".format(my_string_len, 100 - my_string_len))
    
print("Final data string:")
print(final_string)

print("\nYou have $1000. Every time the system successfully predicts your next press, you lose $1.")
print("Otherwise, you earn $1. Print \"enough\" to leave the game. Let's go!")

triade_0_dict = {}
triade_1_dict = {}
for i in range(0, 8):
    triade = str(bin(i)).lstrip("0b").zfill(3)
    triade_0 = triade + "0"
    triade_1 = triade + "1"
    triade_0_count = 0
    triade_1_count = 0
    for j in range(len(final_string)):
        if final_string[j:j+4] == triade_0:
            triade_0_count += 1
        if final_string[j:j+4] == triade_1:
            triade_1_count += 1
    #print("{}: {},{}".format(triade, triade_0_count, triade_1_count))
    triade_0_dict[triade] = triade_0_count
    triade_1_dict[triade] = triade_1_count

#print(triade_0_dict)
#print(triade_1_dict)

balance = 1000
new_string = ""
break_flag = False

while not break_flag and balance >= 0:
    new_string = ""
    while len(new_string) < 4:
        print("\nPrint a random string containing 0 or 1:")
        new_string = str(input())
        if new_string == "enough":
            break_flag = True
            break
        new_string = ''.join(c for c in new_string if c in ["0","1"])

    if break_flag == True:
        break

    predicted_string = new_string[0:3]

    coincidence_counter = 0
    for k in range(3, len(new_string)):
        predict_triade = new_string[k - 3:k]
        #print(predict_triade)
        prediction_symbol = ""
        if triade_0_dict[predict_triade] > triade_1_dict[predict_triade]:
            prediction_symbol = "0"
        elif triade_0_dict[predict_triade] < triade_1_dict[predict_triade]:
            prediction_symbol = "1"
        else:
            prediction_symbol = str(random.randint(0, 1))
        predicted_string += prediction_symbol
        if prediction_symbol == new_string[k]:
            coincidence_counter += 1

    print("\npredictions:")
    print(predicted_string)

    suitable_counter = len(new_string) - 3
    accuracy = round(100 * coincidence_counter / suitable_counter, 2)
    error_counter = suitable_counter - coincidence_counter
    balance_modifier = error_counter - coincidence_counter
    balance += balance_modifier

    print("\nComputer guessed {} out of {} symbols ({} %)".format(coincidence_counter, suitable_counter, accuracy))
    print("Your balance is now ${}".format(balance))

print("Game over!")
