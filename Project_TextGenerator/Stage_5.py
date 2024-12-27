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
    return random_tail[0]

def initial_chain(head):
    word = chain_word(head)
    while True:
        if word[-1] in ['.', '?', '!']:
            word = chain_word(head)
        else:
            break
    return word

def first_word():
    word = ''
    while True:
        if word == '' or word[-1] in ['.', '?', '!']\
                or word[0] != word[0].upper():
            word = random.choice(corpus)
        else:
            break
    return word

for i in range(10):
    phrase_list = []
    phrase_list.append(first_word())
    for _ in range(3):
        phrase_list.append(initial_chain(phrase_list[-1]))
    end_mark = False
    while not end_mark:
        phrase_list.append(chain_word(phrase_list[-1]))
        if phrase_list[-1][-1] in ['.', '?', '!']:
            end_mark = True
    #phrase_list[0] = phrase_list[0][0].upper() + phrase_list[0][1:]
    print(" ".join(phrase_list))
