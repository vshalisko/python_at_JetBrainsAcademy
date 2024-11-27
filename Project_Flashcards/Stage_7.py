import pickle
import os
from io import StringIO
import argparse

streamer = StringIO()

parser = argparse.ArgumentParser()
parser.add_argument("--export_to")
parser.add_argument("--import_from")
args = parser.parse_args()

def prints(text):
    streamer.write(text)
    streamer.write("\n")
    print(text)

def inputs(text=''):
    inp = input(text)
    streamer.write(text)
    streamer.write("\n")
    streamer.write(inp)
    streamer.write("\n")
    return inp

class Card:

    def __init__(self, card, definition, mistakes = 0):
        self.card = card
        self.definition = definition
        self.mistakes = mistakes

class Flashcards:

    def __init__(self):
        self.cards = []
        self.tested = 0

    def init_number(self):
        self.number = int(inputs('Input the number of cards:\n'))

    def init_test_number(self):
        self.test_number = int(inputs('How many times to ask?\n'))

    def add_card(self, card):
        self.cards.append(card)

    def check_card(self, card):
        found = any(map(lambda one_cards: one_cards.card == card, self.cards))
        return found

    def check_definition(self, definition):
        found = any(map(lambda one_cards: one_cards.definition == definition, self.cards))
        return found

    def get_definition(self, card_to_check):
        ok_definition = []
        for one_card in self.cards:
            if one_card.card == card_to_check:
                ok_definition = one_card.definition
                break
        return ok_definition

    def get_card(self, definition_to_check):
        ok_card = []
        for one_card in self.cards:
            if one_card.definition == definition_to_check:
                ok_card = one_card.card
                break
        return ok_card

    def add_mistake(self, card_to_add):
        for one_card in self.cards:
            if one_card.card == card_to_add:
                one_card.mistakes += 1
                break

    def make_set(self):
        for i in range(0, self.number):
            self.request_card(i)

    def reset_stats(self):
        for one_card in self.cards:
            one_card.mistakes = 0
        prints('Card statistics have been reset.')

    def hardest(self):
        highest_score = 0
        term_list = []
        if self.tested == 0:
            prints('There are no cards with errors.')
        for one_card in self.cards:
            if one_card.mistakes > highest_score:
                highest_score = one_card.mistakes
                term_list = []
                term_list.append(one_card.card)
            elif one_card.mistakes == highest_score:
                term_list.append(one_card.card)
            else:
                pass
            if highest_score == 0:
                prints('There are no cards with errors.')
            else:
                if len(term_list) == 1:
                    prints('The hardest card is "{}". You have {} errors answering it.'.format(term_list[0],highest_score))
                else:
                    term_string = ', '.join(['"' + str(item) + '"' for item in term_list if item])
                    prints('The hardest cards are {}. You have {} errors answering it.'.format(term_string,highest_score))

    def request_card(self, j):
        card_check = True
        definition_check = True
        j1 = j + 1
        prints('The term for card #{}:'.format(j1))
        while card_check:
            card = str(inputs())
            if self.check_card(card):
                prints('The term "{}" already exists. Try again:'.format(card))

            else:
                card_check = False
        prints('The definition for card #{}:'.format(j + 1))
        while definition_check:
            definition = str(inputs())
            if self.check_definition(definition):
                prints('The definition "{}" already exists. Try again:'.format(definition))
            else:
                definition_check = False
        self.add_card(Card(card, definition))

    def request_single_card(self):
        card_check = True
        definition_check = True
        prints('The card')
        while card_check:
            card = str(inputs())
            if self.check_card(card):
                prints('The term "{}" already exists. Try again:'.format(card))
            else:
                card_check = False
        prints('The definition of the card')
        while definition_check:
            definition = str(inputs())
            if self.check_definition(definition):
                prints('The definition "{}" already exists. Try again:'.format(definition))
            else:
                definition_check = False
        self.add_card(Card(card, definition))
        prints('The pair ("{}":"{}") has been added.'.format(card, definition))

    def examen_card(self, card):
        prints('Print the definition of "{}":'.format(card.card))
        answer = str(inputs())
        if answer == card.definition:
            prints('Correct!')
        else:
            ok_definition = self.get_definition(card.card)
            ok_card = self.get_card(answer)
            if ok_card:
                prints('Wrong. The right answer is "{}", but your definition is correct for "{}".'.format(ok_definition,ok_card))
            else:
                self.add_mistake(card.card)
                prints('Wrong. The right answer is "{}".'.format(ok_definition))

    def remove_card(self):
        card_to_remove = str(inputs('Which card?\n'))
        if self.check_card(card_to_remove):
            for i in range(0,len(self.cards)):
                if self.cards[i].card == card_to_remove:
                    del self.cards[i]
                    prints('The card has been removed.')
                    break
        else:
            prints('Can\'t remove "{}": there is no such card.'.format(card_to_remove))

    def replace_card(self, card_to_replace, description, mistakes):
        if self.check_card(card_to_replace):
            for i in range(0,len(self.cards)):
                if self.cards[i].card == card_to_replace:
                    self.cards[i].description = description
                    self.cards[i].mistakes = mistakes
                    break
        else:
            prints('Can\'t remove "{}": there is no such card.'.format(card_to_replace))

    def save_pickle(self, file_name=''):
        if not file_name:
            file_name = str(inputs('File name:\n'))
        pickle_dict = {}
        for one_card in self.cards:
            pickle_dict[one_card.card] = [one_card.definition, one_card.mistakes]
        with open(file_name, 'wb') as f:
            pickle.dump(pickle_dict, f)
        prints('{} cards have been saved.'.format(len(self.cards)))

    def load_pickle(self, file_name=''):
        if not file_name:
            file_name = str(inputs('File name:\n'))
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                cards_to_parse = pickle.load(f)
            for new_card, new_content in cards_to_parse.items():
                new_desc = new_content[0]
                new_mistakes = new_content[1]
                if self.check_card(new_card):
                    self.replace_card(new_card, new_desc, new_mistakes)
                else:
                    self.add_card(Card(new_card, new_desc, new_mistakes))
            prints('{} cards have been loaded.'.format(len(cards_to_parse.keys())))
        else:
            prints('File not found.')

def main():

    flashcards = Flashcards()

    if args.import_from:
        flashcards.load_pickle(args.import_from)

    while True:
        menu = str(inputs('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n'))
        if menu == 'log':
            file_name = str(inputs('File name:\n'))
            with open(file_name, "w") as log:
                log.write(streamer.getvalue())
            prints('The log has been saved.')
        elif menu == 'hardest card':
            flashcards.hardest()
        elif menu == 'reset stats':
            flashcards.reset_stats()
        elif menu == 'set':
            flashcards.init_number()
            flashcards.make_set()
        elif menu == 'add':
            flashcards.request_single_card()
        elif menu == 'ask':
            flashcards.init_test_number()
            stack = flashcards.cards
            for i in range(0,flashcards.test_number):
                test_card = stack.pop()
                stack.insert(0,test_card)
                flashcards.examen_card(test_card)
        elif menu == 'remove':
            flashcards.remove_card()
        elif menu == 'import':
            flashcards.load_pickle()
        elif menu == 'export':
            flashcards.save_pickle()
        elif menu == 'exit':
            if args.export_to:
                flashcards.save_pickle(args.export_to)
            prints('Bye bye!')
            break


if __name__ == "__main__":
    main()
