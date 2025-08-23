import numpy as np
#import pandas as pd
import spacy

invalid_chars = {'>', '\\', '*', '<', '/', '_'}

filepath = str(input())

f = open(filepath, "r", encoding="utf-8")
text = f.read()
f.close()

nlp = spacy.load("en_core_web_sm")
tokens = nlp(text)

data = np.array(['Token','Lemma','POS'])
for ti in tokens:
    if ti.text == '' or ti.text == ' ' or ti.text == '\n':
        continue
    if any(c in invalid_chars for c in ti.text):
        continue
    data = np.vstack([data, [ti.text, ti.lemma_, ti.pos_]])

print(data)
print("Number of tokens:", data.shape[0])
