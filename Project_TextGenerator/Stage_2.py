from nltk.tokenize import WhitespaceTokenizer

filename = str(input())
f = open(filename, "r", encoding="utf-8")
text = f.read()
f.close()

wst = WhitespaceTokenizer()

corpus = wst.tokenize(text)
unique = list(dict.fromkeys(corpus))

bigrams = tuple(zip(corpus, corpus[1:]))

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
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
            continue
