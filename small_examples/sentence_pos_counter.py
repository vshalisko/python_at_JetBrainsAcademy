from nltk.tokenize import WhitespaceTokenizer
import nltk

#nltk.download('averaged_perceptron_tagger')
#nltk.download('averaged_perceptron_tagger_eng')

pst = WhitespaceTokenizer()

text = str(input())
token_db = pst.tokenize(text)

pos_db = nltk.pos_tag(token_db)

pos_dict = {}
for (word, pos) in pos_db:
        pos_dict[pos] = pos_dict.setdefault(pos, 0) + 1

#print(pos_dict)

print(max(pos_dict, key=pos_dict.get))
