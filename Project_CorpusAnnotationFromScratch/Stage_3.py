import numpy as np
import pandas as pd
import spacy

invalid_chars = {'>', '\\', '*', '<', '/', '_'}

filepath = str(input())

f = open(filepath, "r", encoding="utf-8")
text = f.read()
f.close()

nlp = spacy.load("en_core_web_sm")
tokens = nlp(text)

data = np.array(['Token','Lemma','POS','entity_type','IOB'])
for ti in tokens:
    if ti.text == '' or ti.text == ' ' or ti.text == '\n' or ti.pos_ == 'SPACE':
        continue
    if any(c in invalid_chars for c in ti.text):
        continue
    data = np.vstack([data, [ti.text, ti.lemma_, ti.pos_, ti.ent_type_, ti.ent_iob_]])

df = pd.DataFrame(data[1:,:], columns=data[0,:])

print(df.iloc[:20,:])
