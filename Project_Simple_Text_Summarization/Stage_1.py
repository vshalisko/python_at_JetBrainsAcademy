import math
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def summarize_news(file_path):
    # Parse the XML file
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

            summary_sentences = sentences[:num_sentences_to_extract]
            summary_text = "\n".join(summary_sentences)

            print(f"HEADER: {header}")
            print(f"TEXT: {summary_text}\n")

if __name__ == "__main__":
    summarize_news("news.xml")
