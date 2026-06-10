import math
import string
import numpy as np
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

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
    # Initialize the lemmatizer and stopword list
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    punctuation_set = set(string.punctuation)

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    news_items = root.findall('.//news')

    for news in news_items:
        header = ""
        text = ""

        # Look at each <value> tag inside the current <news> element
        for value in news.findall('value'):
            attribute_name = value.get('name')

            if attribute_name == 'head':
                header = value.text.strip()
            elif attribute_name == 'text':
                text = value.text.strip()

        if header and text:
            # Tokenize the text into sentences
            sentences = sent_tokenize(text)
            N = len(sentences)
            num_sentences_to_extract = round(math.sqrt(N))

            cleaned_sentences = []
            for sentence in sentences:
                # Tokenize into words
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

            vectorizer = TfidfVectorizer(tokenizer=word_tokenize)

            try:
                tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
                tfidf_array = tfidf_matrix.toarray()
            except ValueError:
                # Fallback 
                continue

            sentence_scores = []
            for doc_vector in tfidf_array:
                non_zero_weights = doc_vector[doc_vector > 0]

                if len(non_zero_weights) > 0:
                    score = np.mean(non_zero_weights)
                else:
                    score = 0.0
                sentence_scores.append(score)

            indexed_scores = list(enumerate(sentence_scores))
            top_indexed_scores = sorted(indexed_scores, key=lambda x: x[1], reverse=True)[:num_sentences_to_extract]
            final_chosen_indices = sorted([item[0] for item in top_indexed_scores])

            summary_sentences = [sentences[idx] for idx in final_chosen_indices]

            summary_text = "\n".join(summary_sentences)

            print(f"HEADER: {header}")
            print(f"TEXT: {summary_text}\n")

if __name__ == "__main__":
    summarize_news("news.xml")
