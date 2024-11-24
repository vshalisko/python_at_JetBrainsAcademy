class Flashcards:

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


class Card:

    def __init__(self, card, definition):
        self.card = card
        self.definition = definition


def main(stage):
    flashcards = Flashcards()
    if stage == 1:
        card = str(input("Card:\n"))
        print(card)
        definition = str(input("Definition:\n"))
        print(definition)
        flashcards.add_card(Card(card, definition))

    elif stage == 2:
        card = str(input())
        definition = str(input())
        flashcards.add_card(Card(card, definition))
        answer =  str(input())
        if answer == flashcards.cards[0].definition:
            print('Your answer is right!')
        else:
            print('Your answer is wrong...')

    elif stage == 3:
        number = int(input("Input the number of cards:\n"))

        for i in range(0,number):
            print('The term for card #{}'.format(i+1))
            card = str(input())
            print('The definition for card #{}'.format(i+1))
            definition = str(input())
            flashcards.add_card(Card(card, definition))

        for test_card in flashcards.cards:
            print('Print the definition of "{}"'.format(test_card.card))
            answer = str(input())
            if answer == test_card.definition:
                print('Correct!')
            else:
                print('Wrong. The right answer is "{}".'.format(test_card.definition))

if __name__ == "__main__":
    main(3)
