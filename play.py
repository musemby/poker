import random
import time
import re

import click

from validators import validate_card_code
from utilities import count_down


ranks = ['A', 'K', 'Q', 'J'] + [str(num) for num in range(2, 11)]
suits = ['clubs', 'diamonds', 'hearts', 'spades']

class Card():
    """Definition of a card"""
    def __init__(self, rank=None, suit=None, joker=False):
        self.rank = rank
        self.suit = suit
        self.joker = joker

        if self.joker:
            self.code = 'JO'
        else:
            self.su = self.suit.split()[0][0].upper()
            self.code =  self.rank + self.su

        if self.joker and (self.suit or self.rank):
            raise Exception('A joker card cannot have a suit or rank')

        if self.rank and str(self.rank) not in ranks:
            raise Exception('The rank provided is invalid')

        if self.rank and str(self.suit) not in suits:
            raise Exception('The suit provided is invalid')

    def __repr__(self):
        return '{0} of {1} [{2}]'.format(self.rank, self.suit, self.code) if self.rank and self.suit else 'Joker [{}]'.format(self.code) # noqa


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

    def pick_card(self, game, number=None):
        if number:
            for _ in range(0, number):
                self.cards.append(game.pack.pick())
        else:
            self.cards.append(game.pack.pick())

    def give_card(self, card):
        self.cards.remove(card)


class Stage():
    def __init__(self):
        self.cards = []

    def add_starter(self, card):
        self.cards.append(card)

    def add(self, card, player):
        self.top = self.cards[-1]
        if card.joker or card.rank == 'A': # special cards
            player.give_card(card)
            self.cards.append(card)
            return True
        elif self.top.suit == card.suit or self.top.rank == card.rank: # normal matching
            player.give_card(card)
            self.cards.append(card)
            return True
        else:
            print('Sorry, placing this card is not a valid move')
            return False



class Game():
    def __init__(self):
        self.name = click.prompt('Welcome to the table. Let\'s start a new game.\nWhat shall we call it?')
        click.echo('\nWelcome to the {} game. Please have a seat.'.format(self.name))
        self.pack = Pack(54)
        self.stage = Stage()
        self.state = ''
        self.play()
        self.player_count = 0

    def __repr__(self):
        return self.name

    def play(self):
        self.player_count = click.prompt('\nHow many people are at the table?', type=int)

        self.players = []
        click.echo('\n')
        for num in range(self.player_count):
            num = num + 1
            name = click.prompt('Hello player {}, what is your name?'.format(num))
            self.players.append(Player(num, name))

        self.pick_starter()
        self.deal(self.pack, self.players)
        self.game_play()

    def deal(self, pack, players):
        for _ in range(4):
            for player in players:
                player.receive_card(self.pack.pick_random())
                time.sleep(0.3)
                click.echo('Dealt player {}'.format(player.name))


        click.clear()
        click.secho('\nAll players ready?',fg='blue')
        count_down(3)

    def pick_starter(self):
        card = random.choice(self.pack.cards)
        if card.rank in [str(r) for r in list(range(9,11)) + list(range(4,8))]:
            self.pack.remove(card)
            self.stage.add_starter(card)
            return
        self.pick_starter()

    def process_action(self, action, player):
        pick_sth = re.match('pick\-[\d]{1,}', action)

        if pick_sth:
            num=int(action.partition('-')[-1])
            player.pick_card(self, number=num)
            return True
        elif action == 'pick':
            player.pick_card(self)
            return True
        else:
            for code in action.split(','):
                if validate_card_code(code) or code.startswith('10'):
                    for card in player.cards:
                        card_code = card.code
                        if code == card_code or code == card_code.lower():
                            return self.stage.add(card, player)

        actions = action.split(' ')
        if len(actions) > 1:
            for act in actions:
                self.process_action(act, player)

    def game_play(self):
        self.top_card = self.stage.cards[len(self.stage.cards)-1:][0]
        self.current_suit = self.top_card.suit
        self.counter = 0
        self.round = 1
        while True:
            self.current_player = self.players[self.counter]
            click.secho("{}, it's your turn to play".format(self.current_player.name), fg='red')

            click.secho('\nYour current hand: ' + str(self.current_player.cards), fg='blue')
            click.secho('The current top card: [...' + str(str(self.stage.cards[-1])) +']',  fg='blue')

            picking = "Type 'pick' to pick one card or 'pick-N' where N is the number of cards to pick\n"
            placing = "Type 'X,Y,Z' where X, Y and Z are the codes of cards in your hand you want to place on the stage in the desired order e.g '6C'"
            action = click.prompt(picking + placing, type=str)
            okay = self.process_action(action, self.current_player)

            click.secho('\nYour current hand: ' + str(self.current_player.cards), fg='blue')
            click.secho('The current top card: ' + str(self.stage.cards[-1]),  fg='blue')
            if okay:
                self.round += 1
                if self.counter < self.player_count-1:
                    self.counter += 1
                else:
                    self.counter = 0


if __name__ == '__main__':
    game = Game()
