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
#bigrams = tuple(zip(corpus, corpus[1:]))
bigrams = tuple(ngrams(corpus, n))

n_token = len(corpus)
n_unique = len(unique)
n_bigrams = len(bigrams)

#print("Corpus statistics")
#print("All tokens:", n_token)
#print("Unique tokens:", n_unique)
print("Number of bigrams:", n_bigrams)

#print(bigrams[4])

while True:
    k = str(input())
    if k == "exit":
        break
    else:
        try:
            val = int(k)
            print("Head:", bigrams[val][0], "\tTail:", bigrams[val][1])
        except ValueError:
            print("Type Error. Please input an integer.")
            continue
