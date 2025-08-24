import numpy as np
import pandas as pd
import spacy
from nltk.corpus import words
from scipy.stats import pearsonr

invalid_chars = {'>', '\\', '*', '<', '/', '_'}

filepath = str(input())

f = open(filepath, "r", encoding="utf-8")
text = f.read()
f.close()

nlp = spacy.load("en_core_web_sm")
tokens = nlp(text)

data = np.array(['token','lemma','POS','entity_type','IOB'])
for ti in tokens:
    if ti.text == '' or ti.text == ' ' or ti.text == '\n' or ti.pos_ == 'SPACE':
        continue
    if any(c in invalid_chars for c in ti.text):
        continue
    data = np.vstack([data, [ti.text, ti.lemma_, ti.pos_, ti.ent_type_, ti.ent_iob_]])

df = pd.DataFrame(data[1:,:], columns=data[0,:])

#print(df.iloc[:20,:])

## Following code modified from https://github.com/syyynth/hyperskill/blob/main/python/0317%20-%20Corpus%20Annotation%20from%20Scratch/task/corpus_annotation.py

num_multiword_entities = len([w for w in tokens.ents if len(w) > 1])
num_devotchka_lemmas = df.query('lemma == "devotchka"').shape[0]
num_milk_stem_tokens = df.query('lemma == "milk"').shape[0]
freq_entity_type = df.entity_type.value_counts().index[1]
freq_entity_token = df.query('entity_type != ""').token.value_counts().index[0]
english_words = words.words()
valid_pos_tags = {'ADJ', 'ADV', 'NOUN', 'VERB'}
non_english_query = 'lemma.str.len() > 4 and lemma not in @english_words and POS in @valid_pos_tags'
top_non_english_tokens = df.query(non_english_query).value_counts('token').head(10).to_dict()
noun_or_propn = df.POS.isin(['NOUN', 'PROPN'])
num_ner = df['entity_type'].str.len() != 0
correlation, pvalue = pearsonr(noun_or_propn, num_ner)

ans = f"""
Number of multi-word named entities: {num_multiword_entities}
Number of lemmas 'devotchka': {num_devotchka_lemmas}
Number of tokens with the stem 'milk': {num_milk_stem_tokens}
Most frequent entity type: {freq_entity_type}
Most frequent named entity token: {freq_entity_token}
Most common non-English words: {top_non_english_tokens}
Correlation between NOUN and PROPN and named entities: {correlation:.2f}
"""
print(ans)
