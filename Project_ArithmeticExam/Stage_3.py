import random
import re

class ArithmeticExam:

    def __init__(self):
        self.correct_answers = 0
        self.questions = 5
        pass

    def calculate(self, operation):
        return eval(operation)

    def generator(self):
        first_argument = str(random.randint(2, 9))
        second_argument = str(random.randint(2, 9))
        operation = random.choice(['+', '-', '*'])
        expression = first_argument + ' ' + operation + ' ' + second_argument
        return expression

    def format_check(self, text):
        pattern = re.compile(r'[^0-9-]')
        if re.findall(pattern, text):
            return True
        elif text == '':
            return True
        return False

exam = ArithmeticExam()

for i in range(exam.questions):
    generated_expression = exam.generator()
    print(generated_expression)
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

print("Your mark is {}/5".format(exam.correct_answers))
