import math
import random

class ArithmeticExam:

    def __init__(self):
        pass

    def calculate(self, operation):
        return eval(operation)

    def generator(self):
        first_argument = str(random.randint(2, 9))
        second_argument = str(random.randint(2, 9))
        operation = random.choice(['+', '-', '*'])
        expression = first_argument + ' ' + operation + ' ' + second_argument
        return expression


exam = ArithmeticExam()
generated_expression = exam.generator()
print(generated_expression)
answer = str(input())
true_result = str(exam.calculate(generated_expression))
if (true_result == answer):
    print('Right!')
else:
    print('Wrong!')
