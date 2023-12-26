def fib(n):

    # base case n = 0
    if (n == 0):    
        return 0
    # base case n = 1
    elif (n == 1):  
        return 1
    # case n > 1
    else:      
        return fib(n-2) + fib(n-1)

fib(10)
