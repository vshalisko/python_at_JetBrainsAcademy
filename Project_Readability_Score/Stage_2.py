from nltk.tokenize import RegexpTokenizer

filename = sys.argv[1]

text = ''
with open(filename, 'r') as f:
  text = f.read()
print(f"Text: {text}")

pattern = "[0-9A-z']+"
tokenizer = RegexpTokenizer(pattern)
sentences = nltk.sent_tokenize(text)

sen_len_sum = 0
for sentence in sentences:
    sentence_words = tokenizer.tokenize(sentence)
    print(sentence_words)
    sen_len_sum += len(sentence_words)

mean_word_count = sen_len_sum / len(sentences)

if mean_word_count > 10:
    print("Difficulty: HARD")
else:
    print("Difficulty: EASY")
