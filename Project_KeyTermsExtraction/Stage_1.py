from lxml import etree
import nltk

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
    keyword_dict = {}
    for word in tokenized_text:
        keyword_dict.setdefault(word, 0)
        keyword_dict[word] += 1
    keyword_sorted = dict(sorted(keyword_dict.items(), key=lambda item: (item[1], item[0]), reverse=True))
    selected_keywords = list(keyword_sorted.items())[:5]

    keyword_string = ""
    for keyword, n in selected_keywords:
        keyword_string += keyword + " "
    print(keyword_string)
    print()
