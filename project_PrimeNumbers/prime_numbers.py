## solution "Create a list of all prime numbers up to 1000 in the code below. Just save this list into a variable prime_numbers"
n = 1000
candidates = list(range(3, n+1, 2))
#print(candidates)
#print(range(len(candidates)))
prime_numbers = [2]
for i in range(len(candidates)):
    #print(candidates[i])
    #print([d for d in range(2, candidates[i]) if d < candidates[i]])
    if not all([candidates[i] % d for d in range(2, candidates[i]) if d < candidates[i]]):
        not_prime = 1
        #print(not_prime)
        #print([candidates[i] % d for d in range(1,candidates[i]) if d < candidates[i]])
    else:
        prime_numbers.append(candidates[i])
print(prime_numbers)
