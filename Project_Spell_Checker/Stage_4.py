import os
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')


def levenshtein_distance(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_grade(errors):
    """Determines the grade based on the number of errors."""
    if 0 <= errors <= 1:
        return 'A'
    elif errors <= 3:
        return 'B'
    elif errors <= 5:
        return 'C'
    elif errors <= 7:
        return 'D'
    elif errors <= 10:
        return 'E'
    else:
        return 'F'


def main():
    vocabulary = set()
    bigram_counts = Counter()

    if os.path.exists("books.txt"):
        with open("books.txt", "r", encoding="utf-8") as file:
            corpus_text = file.read()
        corpus_tokens = word_tokenize(corpus_text)
        vocabulary = set(corpus_tokens)

        corpus_bigrams = zip(corpus_tokens[:-1], corpus_tokens[1:])
        bigram_counts = Counter(corpus_bigrams)
    else:
        print("Error: 'books.txt' file not found.")
        return

    user_input = input("Hello! Please, enter a text here:> ")
    tokens = word_tokenize(user_input)

    error_count = 0
    corrected_tokens = []

    for i, token in enumerate(tokens):
        if token in vocabulary or not token.isalnum():
            corrected_tokens.append(token)
            if token.isalnum():
                pass
            continue

        error_count += 1

        min_distance = float('inf')
        suggestions = []

        for word in vocabulary:
            dist = levenshtein_distance(token, word)
            if dist < min_distance:
                min_distance = dist
                suggestions = [word]
            elif dist == min_distance:
                suggestions.append(word)

        best_candidate = suggestions[0]
        max_frequency = -1

        prev_word = tokens[i - 1] if i > 0 else None
        next_word = tokens[i + 1] if i < len(tokens) - 1 else None

        for candidate in suggestions:
            freq = 0
            if prev_word:
                freq += bigram_counts[(prev_word, candidate)]
            if next_word:
                freq += bigram_counts[(candidate, next_word)]

            if freq > max_frequency:
                max_frequency = freq
                best_candidate = candidate

        corrected_tokens.append(best_candidate)

    grade = get_grade(error_count)
    print(f"Your grade is {grade}. Errors found in the text: {error_count}.")

    corrected_text = ""
    for token in corrected_tokens:
        if token.isalnum() or token in ["'", "`"]:
            if corrected_text and not corrected_text.endswith((".", "!", "?", "'", "`")):
                corrected_text += " " + token
            else:
                corrected_text += " " + token if corrected_text else token
        else:
            corrected_text += token

    print(corrected_text.strip())


if __name__ == "__main__":
    main()
