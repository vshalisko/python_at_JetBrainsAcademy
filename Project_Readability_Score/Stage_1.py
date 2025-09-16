import nltk

text = str(input())
sentences = nltk.sent_tokenize(text)
symbol_count = len(text)
sentence_count = len(sentences)

if symbol_count > 100 or sentence_count > 3:
    print("Difficulty: HARD")
else:
    print("Difficulty: EASY")
