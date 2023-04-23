# write your code here
import string

msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):" 
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

equation_result = ""
memory = 0

def check(v1, v2, v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg += msg_6
    if (v1 == 1 or v2 == 1) and v3 == "*":
        msg += msg_7
    if (v1 == 0 or v2 == 0) and (v3 == "+" or v3 == "-" or v3 == "*"):
        msg += msg_8
    if msg != "":
        msg = msg_9 + msg
    #else:
    #    print("No message")
    return(msg)

def is_one_digit(v):
    v = float(v)
    if v > -10 and v < 10 and v.is_integer():
        output = True
    else:
        output = False
    return(output)

while True:
    print(msg_0)
    equation = str(input())
    equation_list = equation.split(" ")
    if equation_list[0] == "M":
        x = memory
    else:
        try:
            x = float(equation_list[0])
        except ValueError:
            print(msg_1)
            continue
    if equation_list[2] == "M":
        y = memory
    else:
        try:
            y = float(equation_list[2])
        except ValueError:
            print(msg_1)
            continue
    if (equation_list[1] not in ["+","*","-","/"]):
        print(msg_2)
        continue
    else:
        oper = equation_list[1]

    check_msg = check(x, y, oper)
    if check_msg != "":
        print(check_msg)
    
    if oper == "+":
        equation_result = x + y
    if oper == "-":
        equation_result = x - y
    if oper == "*":
        equation_result = x * y
    if oper == "/":
        if y == 0:
            print(msg_3)
            continue
        else:
            equation_result = x / y    
    
    print(equation_result)

    next_question = True
    store_question = True
    while store_question:
        print(msg_4)
        want_store = str(input())
        if want_store == "y":
            ## save memory block
            if is_one_digit(equation_result):
                ## one digit
                msg_index = 10
                memory_question = True
                while memory_question:
                    print(msg_10)
                    want_memory = str(input())
                    if want_memory == "y":
                        memory_question = False
                        memory_question_2 = True
                        while memory_question_2:
                            print(msg_11)
                            want_memory_2 = str(input())
                            if want_memory_2 == "y":
                                memory_question_2 = False
                                memory_question_3 = True
                                while memory_question_3:
                                    print(msg_12)
                                    want_memory_3 = str(input())
                                    if want_memory_3 == "y":
                                        memory_question_3 = False
                                        memory = equation_result
                                    elif want_menory_3 == "n":
                                        memory_question_3 = False
                            elif want_memory_2 == "n":
                                memory_question_2 = False
                    elif want_memory == "n":
                        memory_question = False
            else:
                memory = equation_result
            store_question = False
        elif want_store == "n":
            store_question = False

    while next_question:
        print(msg_5)
        want_next = str(input())
        if want_next == "y":
            next_question = False
        elif want_next == "n":
            next_question = False

    if want_next == "y":
        print("")
        continue
    else:
        break
