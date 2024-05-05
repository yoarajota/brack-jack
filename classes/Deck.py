import random
from classes.Card import Card

class Deck:
    def __init__(self):
        # Initialize with all cards in a deck
        self.cards = []
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in range(1, 13):
                self.add_card(Card(rank, suit))

        print (self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)