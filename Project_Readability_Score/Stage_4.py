import sys
import math
import re
import nltk
from nltk.tokenize import RegexpTokenizer

age_scores = {
    '1': '5-6',
    '2': '6-7',
    '3': '7-8',
    '4': '8-9',
    '5': '9-10',
    '6': '10-11',
    '7': '11-12',
    '8': '12-13',
    '9': '13-14',
    '10': '14-15',
    '11': '15-16',
    '12': '16-17',
    '13': '17-18',
    '14': '18-22'
}

vowels = ("a", "e", "i", "o", "u", "y")

filename = sys.argv[1]

text = ''
with open(filename, 'r') as f:
  text = f.read()
print(f"Text: {text}")

pattern = "[0-9A-z']+"
tokenizer = RegexpTokenizer(pattern)
sentences = nltk.sent_tokenize(text)
words = nltk.word_tokenize(text)

sentence_count = len(sentences)

word_count = 0
for sentence in sentences:
    sentence_words = tokenizer.tokenize(sentence)
    word_count += len(sentence_words)

def syllables(word):
    ## from https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4
    syllable_count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

def count_syllables(text):
    word = text.lower()
    pattern = r"[aeiouy]{2}|[^aiouy][aiouy][^aiouy]|e\B"
    #pattern = r"([aeiouyAEIOUY]+[^e.\s])|([aiouyAEIOUY]+\b)|(\b[^aeiouy0-9.']+e\b)"
    x = re.findall(pattern, word)
    return len(x) or 1

symbol_count = 0
syllable_count = 0
for word in words:
    symbol_count += len(word)
    syllable_count += count_syllables(word)

ar_score = math.ceil(4.71 * symbol_count / word_count + 0.5 * word_count / sentence_count - 21.43)
fk_score = math.ceil(0.39 * word_count / sentence_count + 11.8 * syllable_count / word_count - 15.59)

low_age0, top_age0 = age_scores[str(ar_score)].split("-")
low_age1, top_age1 = age_scores[str(fk_score)].split("-")
average_age = (int(low_age0) + int(low_age1) + int(top_age0) + int(top_age1)) / 4

print(f"Characters: {symbol_count}")
print(f"Sentences: {sentence_count}")
print(f"Words: {word_count}")
print(f"Syllables: {syllable_count}")
print(f"\nAutomated Readability Index: {ar_score} (about {age_scores[str(ar_score)]} year olds).")
print(f"Flesch–Kincaid Readability Test: {ar_score} (about {age_scores[str(ar_score)]} year olds).")
print(f"\nThis text should be understood in average by {average_age} year olds.")
