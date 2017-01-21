import random 


ranks = ['ace', 'king', 'queen', 'jack'] + [str(num) for num in range(2, 10)]
suits = ['clubs', 'diamonds', 'hearts', 'spades']

class Card():
    """Definition of a card"""
    def __init__(self, rank, suit, joker=False):
        self.rank = str(rank)
        self.suit = str(suit)
        self.joker = joker

        if self.joker and (self.suit or self.rank):
            raise Exception('A joker card cannot have a suit or rank')

        if self.rank not in ranks:
            raise Exception('The rank provided is invalid')

        if self.suit not in suits:
            raise Exception('The suit provided is invalid')


class Pack():
    """Definition of a pack of cards"""
    cards = []
    def __init__(self, type):
        for rank in ranks:
            for suit in suits:
                self.cards.append(Card(rank, suit))
