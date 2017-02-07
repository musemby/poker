import random
import time

import click


ranks = ['A', 'K', 'Q', 'J'] + [str(num) for num in range(2, 11)]
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
                    self.add(Card(rank=rank, suit=suit))
            if self.size == 54:
                self.add(Card(joker=True), quantity=2)
        self.shuffle()

    def __repr__(self):
        return '{0} Pack with {1} cards'.format(self.size, len(self.cards))

    @property
    def count(self):
        return len(self.cards)

    def add(self, card, quantity=1):
        if not isinstance(card, Card):
            raise Exception('You can only add a card to the pack')

        self.cards.append(card)
        if card.joker:
            for _ in range(quantity-1):
               self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def pick(self):
        return self.cards.pop()

    def pick_random(self):
        card = random.choice(self.cards)
        self.remove(card)
        return card


class Player():
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.cards = []

    def __repr__(self):
        return self.name

    def receive_card(self, card):
        self.cards.append(card)

    def pick_card(self, game, card=None):
        if not card:
            self.cards.append(game.pack.pick())
        else:
            self.cards.append()

class Stage():
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)


def count_down(num):
    for num in reversed(range(num)):
        print(num, end='\r')
        time.sleep(0.5)


class Game():
    def __init__(self):
        self.name = click.prompt('Welcome to the table. Let\'s start a new game.\nWhat shall we call it?')
        click.echo('\nWelcome to the {} game. Please have a seat.'.format(self.name))
        self.pack = Pack(54)
        self.stage = Stage()
        self.state = ''
        self.play()

    def __repr__(self):
        return self.name

    def play(self):
        player_count = click.prompt('\nHow many people are at the table?', type=int)

        self.players = []
        click.echo('\n')
        for num in range(player_count):
            num = num + 1
            name = click.prompt('Hello player {}, what is your name?'.format(num))
            self.players.append(Player(num, name))

        self.pick_starter()
        self.deal(self.pack, self.players)

    def deal(self, pack, players):
        for _ in range(4):
            for player in players:
                player.receive_card(self.pack.pick_random())
                time.sleep(0.5)
                click.echo('Dealt player {}'.format(player.name))


        click.clear()
        click.secho('\nAll players ready?',fg='blue')
        count_down(3)

    def pick_starter(self):
        card = random.choice(self.pack.cards)
        if card.rank in [str(r) for r in list(range(9,11)) + list(range(4,8))]:
            self.pack.remove(card)
            self.stage.add(card)
            return
        self.pick_starter()

    def process_action(self, action, player):
        if action == 'pick':
            self.pick         

    

    def game_play(self):
        self.top_card = self.stage.cards[len(self.stage.cards)-1:][0]
        self.current_suit = self.top_card.suit

        while True:
            self.turn = self.players[0]
            click.echo("{}, it's your turn to play".format(self.turn.name))
            picking = "Type 'pick' to pick one card or 'pick(N)' where N is the number of cards to pick\n"
            placing = "Type 'place(X,Y,Z)' where X, Y and Z are the cards in your hand you want to place on the stage in the desired order"
            action = click.prompt(picking + placing, type=str)
            self.process_action(action, self.turn)

if __name__ == '__main__':
    game = Game()
    import pdb; pdb.set_trace()
