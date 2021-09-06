from components import *


# Initializes all game components, shuffles deck and draws cards
class Game:
    min_bet = 20

    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.computer = Player()
        self.community = list()
        self.pot = 0
        self.stage = 'opening'
        self.draw = False

        self.deck.shuffle()

        for _ in range(2): self.deck.draw(self.player.cards)
        for _ in range(2): self.deck.draw(self.computer.cards)
        for _ in range(5): self.deck.draw(self.community)

    # Re-initialize self
    def new_game(self):
        self.__init__()

    # Start the next round
    def new_round(self):
        self.deck = Deck()
        self.stage = 'next'
        self.player.won = False
        self.computer.won = False

        self.player.cards.clear()
        self.computer.cards.clear()
        self.community.clear()
        self.deck.shuffle()

        for _c in range(2): self.deck.draw(self.player.cards)
        for _c in range(2): self.deck.draw(self.computer.cards)
        for _c in range(5): self.deck.draw(self.community)

    # Update pot and player banks after each round, reset pot
    def update_banks(self):
        if self.player.won:
            self.player.funds += self.pot
        elif self.computer.won:
            self.computer.funds += self.pot
        elif self.draw:
            self.player.funds += int(self.pot / 2)
            self.computer.funds += int(self.pot / 2)

        self.pot = 0

    # Method for determining a player's hand
    def check_hand(self, hand):
        suits = ['c', 'd', 'h', 's']

        # Utility function for generating winning hands
        def hand_gen(suit, start, stop):
            return [f'{num}{suit}' for num in range(start, stop)]

        # Utility function for comparing player hands to winning hands
        def check_subset(hand, winning_hands):
            for wh in winning_hands:
                if set(wh).issubset(set(hand)):
                    return True

            return False

        def royal_flush():
            winning_hands = [hand_gen(suit, 10, 14) + [f'1{suit}'] for suit in suits]
            return check_subset(hand, winning_hands)

        def straight_flush():
            winning_hands = [hand_gen(suit, num, num + 5) for num in range(1, 10) for suit in suits]
            return check_subset(hand, winning_hands)

        def four_of_a_kind():
            winning_hands = [[str().join(hand_gen(suit, num, num + 1)) for suit in suits] for num in range(1, 14)]
            return check_subset(hand, winning_hands)

        def full_house():
            values = [str(card)[:-1] for card in hand]
            counts = [values.count(v) for v in values]

            return True if 2 in counts and 3 in counts else False

        def flush():
            suits = [str(card)[-1] for card in hand]
            counts = [suits.count(s) for s in suits]

            return True if 5 in counts else False

        def straight():
            values = [int(str(card)[:-1]) for card in hand]
            winning_hands = [hand_gen(str(), num, num + 5) for num in range(1, 10)]
            winning_hands.append(['10', '11', '12', '13', '1'])

            for wh in winning_hands:
                if set(list(map(int, wh))).issubset(set(values)):
                    return True

            return False

        def three_of_a_kind():
            values = [str(card)[:-1] for card in hand]
            counts = [values.count(v) for v in values]

            return True if 3 in counts else False

        def two_pairs():
            values = [str(card)[:-1] for card in hand]
            counts = [values.count(v) for v in values]

            return True if counts.count(2) >= 4 else False

        def pair():
            values = [str(card)[:-1] for card in hand]
            counts = [values.count(v) for v in values]

            return True if counts.count(2) >= 2 else False

        def highcard():
            values = sorted([int(str(card)[:-1]) for card in hand])
            return 14 if 1 in values else values[-1]

        if royal_flush():
            return (10, 'Royal Flush')
        elif straight_flush():
            return (9, 'Straight Flush')
        elif four_of_a_kind():
            return (8, 'Four of a Kind')
        elif full_house():
            return (7, 'Full House')
        elif flush():
            return (6, 'Flush')
        elif straight():
            return (5, 'Straight')
        elif three_of_a_kind():
            return (4, 'Three of a Kind')
        elif two_pairs():
            return (3, 'Two Pairs')
        elif pair():
            return (2, 'Pair')
        else:
            return (1, 'Highcard', highcard())

    # Test all check_hand() submethods
    def run_tests(self):
        royal_flush = self.check_hand(['10s', '13s', '1c', '1d', '11s', '12s', '1s'])[1]
        straight_flush = self.check_hand(['8c', '6h', '3h', '1d', '2h', '4h', '5h'])[1]
        four_of_a_kind = self.check_hand(['1c', '1d', '1h', '1s', '2s', '3s', '4s'])[1]
        full_house = self.check_hand(['6c', '4d', '2h', '2s', '3c', '3d', '3h'])[1]
        flush = self.check_hand(['4c', '5d', '1c', '10c', '12c', '3h', '7c'])[1]
        straight_ace_low = self.check_hand(['2d', '3c', '1c', '7d', '4d', '5s', '10h'])[1]
        straight_ace_high = self.check_hand(['1c', '2d', '13d', '3c', '11d', '10s', '12h'])[1]
        three_of_a_kind = self.check_hand(['6c', '2d', '4c', '2s', '10d', '11h', '2h'])[1]
        two_pairs = self.check_hand(['9c', '2d', '3c', '2s', '3h', '8c', '6c'])[1]
        pair = self.check_hand(['7c', '4d', '2c', '9s', '5h', '4s', '10c'])[1]
        highcard_ace = self.check_hand(['1c', '3d', '5c', '6s', '7h', '11h', '13c'])[1]
        highcard_ten = self.check_hand(['2c', '3d', '5c', '6s', '7h', '9h', '10c'])[1]

        assert royal_flush == 'Royal Flush'
        assert straight_flush == 'Straight Flush'
        assert four_of_a_kind == 'Four of a Kind'
        assert full_house == 'Full House'
        assert flush == 'Flush'
        assert straight_ace_low == 'Straight'
        assert straight_ace_high == 'Straight'
        assert three_of_a_kind == 'Three of a Kind'
        assert two_pairs == 'Two Pairs'
        assert pair == 'Pair'
        assert highcard_ace == 'Highcard'
        assert highcard_ten == 'Highcard'

    # Simulate a player vs. AI game in the terminal - doesn't account for betting, only draws cards and determines a winner
    def simulate(self):
        self.__init__()
        player_card_values = [int(str(self.player.cards[0])[:-1]), int(str(self.player.cards[1])[:-1])]
        computer_card_values = [int(str(self.computer.cards[0])[:-1]), int(str(self.computer.cards[1])[:-1])]

        player_kicker = 14 if 1 in player_card_values else max(player_card_values)
        computer_kicker = 14 if 1 in computer_card_values else max(computer_card_values)

        player_hand = self.check_hand(self.player.cards + self.community)
        computer_hand = self.check_hand(self.computer.cards + self.community)

        print(f'Player cards: {self.player.cards}\n'
              f'Computer cards: {self.computer.cards}\n'
              f'Community cards: {self.community}\n\n'

              f'Player has {player_hand[1]}\n'
              f'Computer has {computer_hand[1]}\n')

        if player_hand[0] > computer_hand[0]:
            print('Player wins!')
        elif player_hand[0] == computer_hand[0] == 1:
            if player_hand[2] > computer_hand[2]:
                print('Player wins!')
            elif player_hand[2] < computer_hand[2]:
                print('Computer wins!')
            else:
                if player_kicker > computer_kicker:
                    print('Player wins by kicker!')
                elif player_kicker < computer_kicker:
                    print('Computer wins by kicker!')
                else:
                    print('Draw!')
        elif player_hand[0] == computer_hand[0]:
            if player_kicker > computer_kicker:
                print('Player wins by kicker!')
            elif player_kicker < computer_kicker:
                print('Computer wins by kicker!')
            else:
                print('Draw!')
        else:
            print('Computer wins!')
