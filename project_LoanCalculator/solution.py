import math
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--type", choices=["diff", "annuity"])
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")

args = parser.parse_args()

selector = ""

P = 0
n = 0
i = 0
A = 0

if args.principal:
    P = float(args.principal)
if args.periods:
    n = int(args.periods)
if args.interest:
    loan_interest = float(args.interest)
    i = loan_interest / (12 * 100)
if args.payment:
    A = float(args.payment)

if args.type == "diff" and i > 0:
    ## pago diferenciado
    if P > 0 and n > 0:
        selector = "d"
    else:
        print("Incorrect parameters")
elif args.type == "annuity" and i > 0:
    ## pago de annuidad
    if P > 0 and n > 0:
        selector = "a"
    elif P > 0 and A > 0:
        selector = "n"
    elif n > 0 and A > 0:
        selector = "p"
    else:
        print("Incorrect parameters")
else:
    print("Incorrect parameters")

if selector == "n":
    ## number of months unknown
    n = math.ceil(math.log(A / (A - i * P), 1 + i))
    n_years = n // 12
    n_restantes = math.ceil(n - n_years * 12)
    print("It will take {} years and {} months to repay this loan!".format(n_years, n_restantes))
    total = n * A
    overpayment = total - P
    print("Overpayment = {}".format(overpayment))    
    
elif selector == "a":
    ## annuity unknown
    i = loan_interest / (12 * 100)
    r = math.pow(i + 1, n)
    A = math.ceil(P * (i * r / (r - 1)))
    print("Your monthly payment = {}!".format(A))
    total = n * A
    overpayment = total - P
    print("Overpayment = {}".format(overpayment))        
    
elif selector == "p":
    ## loan principal unknown
    i = loan_interest / (12 * 100)
    r = math.pow(i + 1, n)
    P = math.ceil(A / (i * r / (r - 1)))
    print("Your loan principal = {}!".format(P))
    total = n * A
    overpayment = total - P
    print("Overpayment = {}".format(overpayment))        

elif selector == "d":
    ## differential payments
    i = loan_interest / (12 * 100)
    total = 0
    for m in range(1, n + 1):
        d = math.ceil((P / n) + i * (P - P * (m - 1) / n))
        total += d
        print("Month {}: payment is {}".format(m, d))
    overpayment = total - P
    print("Overpayment = {}".format(overpayment))
    
else:
    pass

