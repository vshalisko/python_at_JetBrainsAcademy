import nltk
from nltk.tokenize import word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')


def main():
    user_input = input("Hello! Please, enter a text here:\n> ")
    tokens = word_tokenize(user_input)
    print(tokens)

if __name__ == "__main__":
    main()
