from nltk.tokenize import WhitespaceTokenizer

filename = str(input())
f = open(filename, "r", encoding="utf-8")
text = f.read()
f.close()

wst = WhitespaceTokenizer()

corpus = wst.tokenize(text)
unique = list(dict.fromkeys(corpus))
n_token = len(corpus)
n_unique = len(unique)


print("Corpus statistics")
print("All tokens:", n_token)
print("Unique tokens:", n_unique)

while True:
    k = str(input())
    if k == "exit":
        break
    else:
        try:
            val = int(k)
        except ValueError:
            print("Type Error. Please input an integer.")
            continue
        try:
            print(corpus[val])
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
            continue
