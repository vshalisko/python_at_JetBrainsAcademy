import nltk
from nltk import word_tokenize
import pandas as pd
nltk.download('punkt')

bot_name = 'Charles Kew'
data_name_json = '../jeopardy.json'

df = pd.read_json(data_name_json)
question_field = df.columns[2]

print(f"Hello! I'm {bot_name}, a question answering bot who knows answers to all questions from the 'Jeopardy!' game.")

def preprocessor(s):
    s_list = word_tokenize(s.lower())
    s_list_ok = [s for s in s_list if s not in ('.',',',':',';','!','?')]
    return(s_list_ok)

preprocessed_corpus = [preprocessor(line) for number, line in enumerate(df[question_field])]

#print(preprocessed_corpus[5])

while True:
    print('Ask me something!')
    question = str(input())
    tokenized_question = preprocessor(question)
    print("Let's play!")
    print(tokenized_question)
    break
