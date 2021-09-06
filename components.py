import random


# Simple card object, represented as a value which matches the image filenames
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        if self.suit == 1:
            s_rep = 'c'
        elif self.suit == 2:
            s_rep = 'd'
        elif self.suit == 3:
            s_rep = 'h'
        elif self.suit == 4:
            s_rep = 's'

        return f'{self.value}{s_rep}'


# Generates a list of cards with methods to draw and shuffle
class Deck(list):
    def __init__(self):
        super().__init__()

        suits = list(range(1, 5))
        values = list(range(1, 14))

        [[self.append(Card(s, v)) for s in suits] for v in values]

    # Randomize deck
    def shuffle(self):
        random.shuffle(self)

    # Add a card to the specified list
    def draw(self, location):
        location.append(self.pop(0))


# Player object to keep track of cards, wages, etc.
class Player:
    def __init__(self):
        self.cards = list()
        self.funds = 1000
        self.won = False
