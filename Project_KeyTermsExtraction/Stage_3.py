from lxml import etree
import string
import nltk
from nltk.corpus import stopwords

xml_file = 'news.xml'
root = etree.parse(xml_file).getroot()

#etree.dump(root)

articles_dict = {}

for news in root[0]:
    header = news[0].text
    text = news[1].text
    articles_dict[header] = text
    print(header + ":")

    tokenized_text = nltk.tokenize.word_tokenize(text.lower())

    stopwords = nltk.corpus.stopwords.words('english') + ['us'] + ['ha'] + ['wa']
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
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

    keyword_dict = {}
    for word in edited_text:
        keyword_dict.setdefault(word, 0)
        keyword_dict[word] += 1

    keyword_sorted = dict(sorted(keyword_dict.items(), key=lambda item: (item[1], item[0]), reverse=True))
    selected_keywords = list(keyword_sorted.items())[:10]

    keyword_string = ""
    for keyword, n in selected_keywords:
        keyword_string += keyword + " "
    print(keyword_string)
    print()
