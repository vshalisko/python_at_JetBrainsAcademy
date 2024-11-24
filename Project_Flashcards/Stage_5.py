class Card:

    def __init__(self, card, definition):
        self.card = card
        self.definition = definition

class Flashcards:

    def __init__(self):
        self.cards = []

    def init_number(self):
        self.number = int(input('Input the number of cards:\n'))

    def init_test_number(self):
        self.test_number = int(input('How many times to ask?\n'))


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

    def make_set(self):
        for i in range(0, self.number):
            self.request_card(i)

    def request_card(self, j):
        card_check = True
        definition_check = True
        print('The term for card #{}:'.format(j + 1))
        while card_check:
            card = str(input())
            if self.check_card(card):
                print('The term "{}" already exists. Try again:'.format(card))
            else:
                card_check = False
        print('The definition for card #{}:'.format(j + 1))
        while definition_check:
            definition = str(input())
            if self.check_definition(definition):
                print('The definition "{}" already exists. Try again:'.format(definition))
            else:
                definition_check = False
        self.add_card(Card(card, definition))

    def request_single_card(self):
        card_check = True
        definition_check = True
        print('The card')
        while card_check:
            card = str(input())
            if self.check_card(card):
                print('The term "{}" already exists. Try again:'.format(card))
            else:
                card_check = False
        print('The definition of the card')
        while definition_check:
            definition = str(input())
            if self.check_definition(definition):
                print('The definition "{}" already exists. Try again:'.format(definition))
            else:
                definition_check = False
        self.add_card(Card(card, definition))
        print('The pair ("{}":"{}") has been added.'.format(card, definition))


    def examen_card(self, card):
        print('Print the definition of "{}":'.format(card.card))
        answer = str(input())
        if answer == card.definition:
            print('Correct!')
        else:
            ok_definition = self.get_definition(card.card)
            ok_card = self.get_card(answer)
            if ok_card:
                print('Wrong. The right answer is "{}", but your definition is correct for "{}".'.format(ok_definition,ok_card))
            else:
                print('Wrong. The right answer is "{}".'.format(ok_definition))

    def remove_card(self):
        card_to_remove = str(input('Which card?\n'))
        if self.check_card(card_to_remove):
            for i in range(0,len(self.cards)):
                if self.cards[i].card == card_to_remove:
                    del self.cards[i]
                    print('The card has been removed.')
                    break
        else:
            print('Can\'t remove "{}": there is no such card.'.format(card_to_remove))

def main():

    flashcards = Flashcards()
    while True:
        menu = str(input('Input the action (add, remove, import, export, ask, exit):\n'))
        if menu == 'set':
            flashcards.init_number()
            flashcards.make_set()
        elif menu == 'exit':
            print('Bye bye!')
            break
        elif menu == 'add':
            flashcards.request_single_card()
        elif menu == 'ask':
            flashcards.init_test_number()
            #for test_card in flashcards.cards:
            for i in range(0,flashcards.test_number):
                test_card = flashcards.cards[i]
                flashcards.examen_card(test_card)
        elif menu == 'remove':
            flashcards.remove_card()
        elif menu == 'import':
            file_name = str(input('File name:\n'))
            pass
        elif menu == 'export':
            file_name = str(input('File name:\n'))
            pass


if __name__ == "__main__":
    main()
