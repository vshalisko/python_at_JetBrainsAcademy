import nltk
from nltk import word_tokenize
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

nltk.download('punkt')

bot_name = 'Charles Kew'
data_name_json = '../jeopardy.json'

df = pd.read_json(data_name_json)
question_field = df.columns[2]

print(f"Hello! I'm {bot_name}, a question answering bot who knows answers to all questions from the 'Jeopardy!' game.")

def preprocessor(s):
    s_list = word_tokenize(s.lower())
    s_list_ok = [s for s in s_list if s not in ('.',',',':',';','!','?','"')]
    return(s_list_ok)

preprocessed_corpus = [TaggedDocument(preprocessor(line), [number]) for number, line in enumerate(df[question_field])]

#print(preprocessed_corpus[5])

model = Doc2Vec(vector_size=124,
                window=2,
                min_count=2,
                workers=2,
                epochs=10)
model.build_vocab(preprocessed_corpus)
model.train(preprocessed_corpus, total_examples=model.corpus_count, epochs=model.epochs)


while True:
    print('Ask me something!')
    question = str(input())
    tokenized_question = preprocessor(question)
    print("Let's play!")
    response = model.dv.most_similar([model.infer_vector(tokenized_question)], topn=1)
    question_number = response[0][0]
    question_certainty = round(response[0][1] * 100)
    print(f"I know this question: its number is {question_number}. I'm {question_certainty}% sure of this.")
    break
