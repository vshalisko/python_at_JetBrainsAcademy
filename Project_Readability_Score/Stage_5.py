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

pattern = "[0-9A-z']+"

filename = sys.argv[1]
longman_file = sys.argv[2]

text = ''
with open(filename, 'r') as f:
  text = f.read()
print(f"Text: {text}")

longman_text = ''
with open(longman_file, 'r') as f:
  longman_text = f.read()

tokenizer = RegexpTokenizer(pattern)
sentences = nltk.sent_tokenize(text)
words = tokenizer.tokenize(text)
words_for_character_count = nltk.word_tokenize(text)

sentence_count = len(sentences)
word_count = 0
for sentence in sentences:
    sentence_words = tokenizer.tokenize(sentence)
    word_count += len(sentence_words)

symbol_count = sum(len(word) for word in words_for_character_count)

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

longman = set(longman_text.split())
difficult_count = sum(w not in longman for w in words)

ar_score = math.ceil(4.71 * symbol_count / word_count + 0.5 * word_count / sentence_count - 21.43)
fk_score = math.ceil(0.39 * word_count / sentence_count + 11.8 * syllable_count / word_count - 15.59)
dc_score = 100 * 0.1579 * difficult_count / word_count + 0.0496 * word_count / sentence_count
if dc_score >= 5:
    dc_score += 3.6365
dc_score = math.ceil(dc_score)

low_age0, top_age0 = age_scores[str(ar_score)].split("-")
low_age1, top_age1 = age_scores[str(fk_score)].split("-")
low_age2, top_age2 = age_scores[str(dc_score)].split("-")
average_age0 = (int(low_age0) + int(top_age0)) / 2
average_age1 = (int(low_age1) + int(top_age1)) / 2
average_age2 = (int(low_age2) + int(top_age2)) / 2
average_age = (average_age0 + average_age1 + average_age2) / 3

print(f"Characters: {symbol_count}")
print(f"Sentences: {sentence_count}")
print(f"Words: {word_count}")
print(f"Difficult words: {difficult_count}")
print(f"Syllables: {syllable_count}")
print(f"\nAutomated Readability Index: {ar_score}. The text can be understood by {age_scores[str(ar_score)]} year olds.")
print(f"Flesch–Kincaid Readability Test: {fk_score}. The text can be understood by {age_scores[str(fk_score)]} year olds.")
print(f"Dale-Chall Readability Index: {dc_score}. The text can be understood by {age_scores[str(dc_score)]} year olds.")
print(f"\nThis text should be understood in average by {average_age} year olds.")
