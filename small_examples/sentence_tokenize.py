## Example 1
from nltk.tokenize import PunktSentenceTokenizer
pst = PunktSentenceTokenizer()

text = str(input())
print(pst.tokenize(text))
