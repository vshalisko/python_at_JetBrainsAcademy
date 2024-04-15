import random
import re

class ArithmeticExam:

    def __init__(self):
        self.correct_answers = 0
        self.questions = 5
        pass

    def calculate(self, operation):
        return eval(operation)

    def generator(self, type):
        expression = ''
        if type == '1':
            first_argument = str(random.randint(2, 9))
            second_argument = str(random.randint(2, 9))
            operation = random.choice(['+', '-', '*'])
            expression = first_argument + ' ' + operation + ' ' + second_argument
            print(expression)
        elif type == '2':
            first_argument = str(random.randint(11, 29))
            expression = first_argument + ' ** 2'
            print(first_argument)
        return expression

    def format_check(self, text):
        pattern = re.compile(r'[^0-9-]')
        if re.findall(pattern, text):
            return True
        elif text == '':
            return True
        return False

print('''Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29''')

description = ['simple operations with numbers 2-9',
               'integral squares of 11-29']

while 1:
    level = str(input())
    if level == '1' or level == '2':
        break
    else:
        print('Incorrect format.')


exam = ArithmeticExam()

for i in range(exam.questions):
    generated_expression = exam.generator(level)
    answer_wait = True
    answer = []
    while answer_wait:
        answer = str(input())
        answer_check = exam.format_check(answer)
        if answer_check:
            print('Incorrect format.')
        else:
            answer_wait = False
    true_result = str(exam.calculate(generated_expression))
    if true_result == answer:
        print('Right!')
        exam.correct_answers += 1
    else:
        print('Wrong!')

print("Your mark is {}/5. Would you like to save the result? Enter yes or no.".format(exam.correct_answers))

save_option = str(input())
if save_option in ['yes', 'YES', 'y', 'Yes']:
    ## file save
    print('What is your name?')
    name = str(input())
    file = open('results.txt', 'a', encoding='utf-8')
    file_line = name + ": " + str(exam.correct_answers) + "/5 in level " + level + " (" + str(description[int(level) - 1]) + ")."
    file.write(file_line)
    file.close()
    print('The results are saved in "results.txt".')
