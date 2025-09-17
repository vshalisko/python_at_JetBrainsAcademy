import sys
import math
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

sen_len_sum = 0
for sentence in sentences:
    sentence_words = tokenizer.tokenize(sentence)
    sen_len_sum += len(sentence_words)

word_len_sum = 0
for word in words:
    word_len_sum += len(word)

symbol_count = word_len_sum
sentence_count = len(sentences)
word_count = sen_len_sum

ar_score = math.ceil(4.71 * symbol_count / word_count + 0.5 * word_count / sentence_count - 21.43)

print(f"Characters: {symbol_count}")
print(f"Sentences: {sentence_count}")
print(f"Words: {word_count}")
print(f"Automated Readability Index: {ar_score} (this text should be understood by {age_scores[str(ar_score)]} year olds).")
