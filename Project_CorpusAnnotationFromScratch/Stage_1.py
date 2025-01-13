## note 1: use spacy 3.4.4
## note 2: downgrade numpy to 1.26.4
## note 3: install en_core_web_sm by following command python -m spacy download en_core_web_sm

import numpy as np
#import pandas as pd
import spacy

filepath = str(input())

f = open(filepath, "r", encoding="utf-8")
text = f.read()
f.close()

nlp = spacy.load("en_core_web_sm")
token = nlp(text)

data = np.array(['Token'])
for ti in token:
    data = np.vstack([data, ti.text])

print(data)
print("Number of tokens:", data.shape[0])
