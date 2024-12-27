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

bigrams = tuple(ngrams(corpus, 2))
trigrams = tuple(ngrams(corpus, 3))

n_token = len(corpus)
n_unique = len(unique)
n_bigrams = len(bigrams)

#print("Number of bigrams:", n_bigrams)

bigram_dict = {}
for bigram in bigrams:
    (head, tail) = bigram
    bigram_dict.setdefault(head, {}).setdefault(tail, 0)
    bigram_dict[head][tail] += 1

trigram_dict = {}
for trigram in trigrams:
    (head1, head2, tail) = trigram
    head = head1 + ' ' + head2
    trigram_dict.setdefault(head, {}).setdefault(tail, 0)
    trigram_dict[head][tail] += 1

def chain_word(head, dictionary):
    tails = []
    probs = []
    for tail in dictionary[head].keys():
        tails.append(tail)
        probs.append(dictionary[head][tail])
    random_tail = random.choices(tails, probs)
    return random_tail[0]

def final_word(head):
    word = chain_word(head, trigram_dict)
    return word

def initial_chain(head):
    word = chain_word(head, trigram_dict)
    #while True:
    #    if word[-1] in ['.', '?', '!']:
    #        word = chain_word(head, trigram_dict)
    #    else:
    #        break
    return word

def first_word():
    trigram = random.choice(trigrams)
    while True:
        (head1, head2, tail) = trigram
        if head1[-1] in ['-', '.', '?', '!', '"']\   # There may be some more unwanted symbols
                or head1[0] != head1[0].upper():
            trigram = random.choice(trigrams)
        else:
            break
    return (head1, head2)

for i in range(10):
    phrase_list = []
    (first, second) = first_word()
    phrase_list.append(first)
    phrase_list.append(second)
    for _ in range(2):
        phrase_list.append(initial_chain(phrase_list[-2] + ' ' + phrase_list[-1]))
    end_mark = False
    reset_counter = 0
    while not end_mark and reset_counter <= 50:        # reset counter is to prevent loop stuck if there are no end mark found
        reset_counter += 1
        phrase_list.append(final_word(phrase_list[-2] + ' ' + phrase_list[-1]))
        if phrase_list[-1][-1] in ['.', '?', '!']:
            end_mark = True
    #phrase_list[0] = phrase_list[0][0].upper() + phrase_list[0][1:]
    print(" ".join(phrase_list))
