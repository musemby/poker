import random 


ranks = ['ace', 'king', 'queen', 'jack'] + [str(num) for num in range(2, 11)]
suits = ['clubs', 'diamonds', 'hearts', 'spades']

class Card():
    """Definition of a card"""
    def __init__(self, rank=None, suit=None, joker=False):
        self.rank = rank
        self.suit = suit
        self.joker = joker

        if self.joker and (self.suit or self.rank):
            raise Exception('A joker card cannot have a suit or rank')

        if self.rank and str(self.rank) not in ranks:
            raise Exception('The rank provided is invalid')

        if self.rank and str(self.suit) not in suits:
            raise Exception('The suit provided is invalid')

    def __repr__(self):
        return '{0} of {1}'.format(self.rank, self.suit) if self.rank and self.suit else 'Poker' # noqa


class Pack():
    """Definition of a pack of cards"""
    def __init__(self, size):
        self.size = int(size)
        self.cards = []

        if self.size not in [52, 54]:
            raise Exception('Only 52 and 54 card decks are accepted')

        if len(self.cards) < self.size:
            for rank in ranks:
                for suit in suits:
                    self.add_to_pack(Card(rank=rank, suit=suit))
            if self.size == 54:
                self.add_to_pack(Card(joker=True), quantity=2)
        self.shuffle()

    def __repr__(self):
        return '{0} Pack with {1} cards'.format(self.size, len(self.cards))

    def add_to_pack(self, card, quantity=1):
        if not isinstance(card, Card):
            raise Exception('You can only add a card to the pack')
        self.cards.append(card)

        if card.joker:
            for _ in xrange(quantity-1):
               self.cards.append(card)

    def shuffle(self):
        return random.shuffle(self.cards)


class Player():
    def __init__(self, name):
        self.name = name


class Game():
    def __init__(self, pack, players):
        self.pack = pack
        self.players = players


pak=Pack(54)

import pdb
pdb.set_trace()