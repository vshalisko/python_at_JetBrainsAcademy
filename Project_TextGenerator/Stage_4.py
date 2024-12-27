import random
from nltk.tokenize import WhitespaceTokenizer
from nltk import ngrams

filename = str(input())
f = open(filename, "r", encoding="utf-8")
text = f.read()
f.close()

wst = WhitespaceTokenizer()
corpus = wst.tokenize(text)
unique = list(dict.fromkeys(corpus))

n = 2
bigrams = tuple(ngrams(corpus, n))

n_token = len(corpus)
n_unique = len(unique)
n_bigrams = len(bigrams)

#print("Number of bigrams:", n_bigrams)

bigram_dict = {}
for bigram in bigrams:
    (head, tail) = bigram
    bigram_dict.setdefault(head, {}).setdefault(tail, 0)
    bigram_dict[head][tail] += 1

def chain_word(head):
    tails = []
    probs = []
    for tail in bigram_dict[head].keys():
        tails.append(tail)
        probs.append(bigram_dict[head][tail])
    random_tail = random.choices(tails, probs)
    return random_tail

## Test chain_word() function with one start word
#start = "sister"
#print(*chain_word(start))

for i in range(10):
    phrase_list = []
    phrase_list.append(random.choice(corpus))
    for j in range(9):
        phrase_list.append(*chain_word(phrase_list[-1]))
    print(" ".join(phrase_list))
