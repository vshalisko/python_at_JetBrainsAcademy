class Flashcards:

    def __init__(self):
        self.cards = []

    def init_number(self):
        self.number = int(input("Input the number of cards:\n"))

    def add_card(self, card):
        self.cards.append(card)

    def check_card(self, card):
        found = any(map(lambda one_cards: one_cards.card == card, self.cards))
        return(found)

    def check_definition(self, definition):
        found = any(map(lambda one_cards: one_cards.definition == definition, self.cards))
        return(found)

    def get_definition(self, card_to_check):
        ok_definition = []
        for one_card in self.cards:
            if one_card.card == card_to_check:
                ok_definition = one_card.definition
                break
        return(ok_definition)

    def get_card(self, definition_to_check):
        ok_card = []
        for one_card in self.cards:
            if one_card.definition == definition_to_check:
                ok_card = one_card.card
                break
        return(ok_card)

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
        flashcards.init_number()

        for i in range(0,flashcards.number):
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

    elif stage == 4:
        flashcards.init_number()

        for i in range(0,flashcards.number):
            card_check = True
            definition_check = True
            print('The term for card #{}:'.format(i + 1))
            while card_check:
                card = str(input())
                if flashcards.check_card(card):
                    print('The term "{}" already exists. Try again:'.format(card))
                else:
                    card_check = False
            print('The definition for card #{}:'.format(i + 1))
            while definition_check:
                definition = str(input())
                if  flashcards.check_definition(definition):
                    print('The definition "{}" already exists. Try again:'.format(definition))
                else:
                    definition_check = False
                    flashcards.add_card(Card(card, definition))

        for test_card in flashcards.cards:
            print('Print the definition of "{}":'.format(test_card.card))
            answer = str(input())
            if answer == test_card.definition:
                print('Correct!')
            else:
                ok_definition = flashcards.get_definition(test_card.card)
                ok_card = flashcards.get_card(answer)
                if ok_card:
                    print('Wrong. The right answer is "{}", but your definition is correct for "{}".'.format(ok_definition,ok_card))
                else:
                    print('Wrong. The right answer is "{}".'.format(ok_definition))



if __name__ == "__main__":
    main(4)
