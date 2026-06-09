import math
import string
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def summarize_news(file_path):

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    punctuation_set = set(string.punctuation)

    tree = ET.parse(file_path)
    root = tree.getroot()

    news_items = root.findall('.//news')

    for news in news_items:
        header = ""
        text = ""

        for value in news.findall('value'):
            attribute_name = value.get('name')

            if attribute_name == 'head':
                header = value.text.strip()
            elif attribute_name == 'text':
                text = value.text.strip()

        if header and text:
    
            sentences = sent_tokenize(text)
            N = len(sentences)

            num_sentences_to_extract = round(math.sqrt(N))

            selected_sentences = sentences[:num_sentences_to_extract]

            cleaned_sentences = []
            for sentence in selected_sentences:

                words = word_tokenize(sentence)

                cleaned_words = []
                for word in words:

                    lower_word = word.lower()

                    if lower_word in punctuation_set:
                        continue

                    if lower_word in stop_words:
                        continue

                    lemmatized_word = lemmatizer.lemmatize(lower_word, pos='n')

                    cleaned_words.append(lemmatized_word)

                cleaned_sentences.append(" ".join(cleaned_words))

            summary_text = "\n".join(cleaned_sentences)

            print(f"HEADER: {header}")
            print(f"TEXT: {summary_text}\n")

if __name__ == "__main__":
    summarize_news("news.xml")
