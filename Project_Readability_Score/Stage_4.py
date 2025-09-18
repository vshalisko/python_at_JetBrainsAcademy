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

symbol_count = 0
for word in words:
    symbol_count += len(word)

def countSyllables(text):
    ## The following function was taken from Joydeep Chatterjee solution
    syllables = 0
    words = text.lower().split(" ")
    vowels = ["a", "e", "i", "o", "u", "y"]
    for word in words:
        count = 0
        i = 0
        j = 1
        while j < len(word):
            if word[i] in vowels:
                if word[j] not in vowels:
                    if j - i > 2:
                        count += 2
                    else:
                        count += 1
                    i = j
                    j = i + 1
                else: j += 1
            else:
                i += 1
                j += 1
        if count == 0:
            count += 1
        syllables += count
    return syllables

syllable_count = countSyllables(text)

ar_score = math.ceil(4.71 * symbol_count / word_count + 0.5 * word_count / sentence_count - 21.43)
fk_score = math.ceil(0.39 * word_count / sentence_count + 11.8 * syllable_count / word_count - 15.59)

low_age0, top_age0 = age_scores[str(ar_score)].split("-")
low_age1, top_age1 = age_scores[str(fk_score)].split("-")
average_age0 = (int(low_age0) + int(top_age0)) / 2
average_age1 = (int(low_age1) + int(top_age1)) / 2
average_age = (average_age0 + average_age1) / 2

print(f"Characters: {symbol_count}")
print(f"Sentences: {sentence_count}")
print(f"Words: {word_count}")
print(f"Syllables: {syllable_count}")
print(f"\nAutomated Readability Index: {ar_score} (about {age_scores[str(ar_score)]} year olds).")
print(f"Flesch–Kincaid Readability Test: {fk_score} (about {age_scores[str(fk_score)]} year olds).")
print(f"\nThis text should be understood in average by {average_age} year olds.")
