import os
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

    if os.path.exists("books.txt"):
        with open("books.txt", "r", encoding="utf-8") as file:
            corpus_text = file.read()

        corpus_tokens = word_tokenize(corpus_text)
        unique_vocabulary = set(corpus_tokens)

        print(f"The vocabulary consists of {len(unique_vocabulary)} words.")
    else:
        print("Error: 'books.txt' file not found. Please place it in the project directory.")

if __name__ == "__main__":
    main()
