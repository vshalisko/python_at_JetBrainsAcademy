## Stage 3/6:Create a Markov chain model
## This model contain probabilistic information
## that will tell us what the next word in a chain might be
## from the bigrams approach

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

print("Number of bigrams:", n_bigrams)

bigram_dict = {}
for bigram in bigrams:
    (head, tail) = bigram
    bigram_dict.setdefault(head, {}).setdefault(tail, 0)
    bigram_dict[head][tail] += 1

while True:
    k = str(input())
    if k == "exit":
        break
    else:
        try:
             print("Head:", k)
             for tail in bigram_dict[k].keys():
                print("Tail:", tail, "\tCount:", bigram_dict[k][tail])
        #except ValueError:
        #    print("Type Error. Please input an integer.")
        #    continue
        #except IndexError:
        #    print("Index Error. Please input an integer that is in the range of the corpus.")
        #    continue
        except KeyError:
            print("Key Error. The requested word is not in the model. Please input another word.")
            continue
