from lxml import etree
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
vectorizer = TfidfVectorizer(input='content', lowercase=True, ngram_range=(1, 1), min_df=0.1, max_df=0.6)
stopwords = nltk.corpus.stopwords.words('english') + ['us'] + ['ha'] + ['wa']

xml_file = 'news.xml'
root = etree.parse(xml_file).getroot()

#etree.dump(root)

all_texts = []
articles_dict = {}

for news in root[0]:
    header = news[0].text
    text = news[1].text

    tokenized_text = nltk.tokenize.word_tokenize(text.lower())

    lemmatized_text = []
    for word in tokenized_text:
        if word in string.punctuation or word in stopwords:
            pass
        elif word.startswith("'"):
            pass
        else:
            lemmatized_text.append(lemmatizer.lemmatize(word))

    edited_text = []


    for word in lemmatized_text:
        if len(word) < 2:
            pass
        elif nltk.pos_tag([word])[0][1] != 'NN':
            pass
        else:
            edited_text.append(word)

    edited_text_string = " ".join(edited_text)

    articles_dict[header] = edited_text_string
    all_texts.append(edited_text_string)

vectorizer.fit(all_texts)

for header, text in articles_dict.items():
    print(header + ":")

    vector = vectorizer.transform([text])
    terms = vectorizer.get_feature_names_out()
    vector_array = vector.toarray()[0]

    keyword_dict = {}
    for j in range(len(vector_array)):
        keyword_dict[terms[j]] = vector_array[j]

    keyword_sorted = dict(sorted(keyword_dict.items(), key=lambda item: (item[1], item[0]), reverse=True))
    selected_keywords = list(keyword_sorted.items())[:5]

    keyword_string = ""
    for keyword, n in selected_keywords:
        keyword_string += keyword + " "
    print(keyword_string)
    print()
