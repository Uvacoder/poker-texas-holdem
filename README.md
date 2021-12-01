# Texas-Holdem
![alt-text](https://github.com/adamjamestorres/Texas-Holdem/blob/master/Texas%20Hold'em.gif)

# Texas Hold 'em 

#### _Built with Python/Tkinter_

### Overview 

---

This poker app was built with [**Python**](https://www.python.org/) (v. 3.8.3) using no external dependencies. It utilizes three built-in libraries: [**random**](https://docs.python.org/3/library/random.html), [**time**](https://docs.python.org/3/library/time.html), and [**tkinter**](https://docs.python.org/3/library/tkinter.html).

The game uses a standard 52-card deck and follows the general standard rules of [**Texas Hold 'em**](https://en.wikipedia.org/wiki/Texas_hold_'em). It supports one human player vs. one AI player. The AI is programmed to always Check or Match the human player's bet. Only the human player can take the Raise and Fold actions.

The program is structured into 4 Python modules:
- `app.py` -- Contains the `App` class, which houses all elements of the Tkinter GUI.
- `components.py` -- Contains the building blocks of the game: the `Card`, `Deck`, and `Player` classes.
- `game.py` -- Contains the `Game` class, which houses the core poker logic.
- `main.py` -- Combines the `App` and `Game` classes to initialize the program.

The program also contains an `images` directory which houses all of the card image assets. All image assets are `.gif` files and the majority of them follow a `{value}{suit}` naming convention. For example, the **Ten of Hearts** card has a filename of `10h.gif`. The exceptions to this rule are the Joker (`j.gif`), the rear side of card (`b.gif`), and the empty tile (`empty.gif`).

### Base Components (`components.py`) 

---

There are three primary classes which act as building blocks for the rest of the game: `Card`, `Deck`, and `Player`.

---

##### **Imports** 

- This module imports the [**random**](https://docs.python.org/3/library/random.html) library in order to utilize its `shuffle()` function within the `Deck` class.
    ```py
    import random
    ```

##### `Card()` 

 - A `Card` object is initialized with two arguments, `suit` and `value`, both of which are passed as integers. Suits are identified with digits 1 thru 4. See the `__repr__` method below for the value mappings. Cards are identified with digits 1 thru 13, where 1 is the Ace and 13 is the King.
    ```py
    class Card:
        def __init__(self, suit, value):
            self.suit  = suit
            self.value = value
    ```

- The `__repr__` method  converts the suit integer to a single-character string, then returns an f-string which concatenates the card value with the string representation of the suit.
    ```py
        def __repr__(self):
            if   self.suit == 1: s_rep = 'c'  # clove
            elif self.suit == 2: s_rep = 'd'  # diamond
            elif self.suit == 3: s_rep = 'h'  # heart
            elif self.suit == 4: s_rep = 's'  # spade
            
            return f'{self.value}{s_rep}'
    ```

- The final string representation of the card matches the filename structure of the card image assets.
    ```py
    >>> seven_of_hearts = Card(3, 7)
    >>> print(seven_of_hearts)
    7h
    ```

##### `Deck()` 

- The `Deck` object is a `list` subclass. Upon initialization, it calls the `super().__init__()` method to inherit the default `list` methods.
    ```py
    class Deck(list):
        def __init__(self):
            super().__init__()
    ```

- Then, with the help of the `range()` function, two lists of integers are generated to represent every possible suit and value combination.
    ```py
            suits  = list(range(1, 5))   # ==> [1, 2, 3, 4]
            values = list(range(1, 14))  # ==> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    ```

- Finally, we iterate through each suit/value combination and generate a `Card` object. Since the `Deck` object is a `list`, it can simply `append` each `Card` object to itself.
    ```py
            [[self.append(Card(s, v)) for s in suits] for v in values]
    ```

- If we initialize and `print` a new `Deck` object, we can see that it returns a list containing all of the unique card values.
    ```py
    >>> deck = Deck()
    >>> print(deck)
    [1c, 1d, 1h, 1s, 2c, 2d, 2h, 2s, 3c, 3d, 3h, 3s, 4c, 4d, 4h, 4s, 5c, 5d, 5h, 5s, 6c, 6d, 6h, 6s, 7c, 7d, 7h, 7s, 8c, 8d, 8h, 8s, 9c, 9d, 9h, 9s, 10c, 10d, 10h, 10s, 11c, 11d, 11h, 11s, 12c, 12d, 12h, 12s, 13c, 13d, 13h, 13s]
    ```

The `Deck` class also contains two methods: `shuffle` and `draw`.

##### `shuffle()` 

- The `shuffle` method utilizes the built-in `shuffle` function from the [**random**](https://docs.python.org/3/library/random.html) module in order to randomize the order of cards in the deck.
    ```py
        def shuffle(self):
            random.shuffle(self)
    ```

- If we `print` our deck again after using the `shuffle` method, we can see that it exhibits the expected behavior:
    ```py
    >>> deck = Deck()
    >>> deck.shuffle()
    >>> print(deck)
    [2s, 9s, 13h, 3s, 10s, 3h, 10h, 10c, 8c, 5s, 10d, 6h, 2h, 12h, 12c, 6s, 1c, 13d, 2d, 9c, 9d, 12d, 5d, 7h, 6c, 8s, 1h, 4d, 1d, 5h, 4c, 2c, 8h, 4s, 11s, 7d, 11d, 5c, 9h, 6d, 12s, 13s, 7s, 3d, 7c, 11h, 11c, 3c, 8d, 13c, 1s, 4h]
    ```

##### `draw()` 

- The `draw` method uses the inherited `pop` and `append` methods from the `list` class to remove the first card from the deck while simultaneously adding it to a new `location`, such as a player's hand.
    ```py
        def draw(self, location):
            location.append(self.pop(0))
    ```

---

##### `Player()` 

- The `Player` object is used to keep track of attributes for both human and AI players.
    ```py
    class Player:
        def __init__(self):
            self.cards = list()
            self.funds = 1000
            self.won   = False
    ```
- The `cards` variable defaults to an empty `list`, which will contain the player's hand once the game begins. 
- The `funds` variable defaults to an `int` of `1000`, which will be modified as the player places bets or gains a winning hand. 
- The `won` variable defaults to a `bool` of `False`. This flag is switched to `True` when the player wins a round. 

### Game Structure (`game.py`) 

---

Most of the core game logic is structured within the `Game` class.

---

##### **Imports** 
- This module imports all of the classes from the `components` module.
    ```py
    from components import *
    ```

##### `Game()` 

- The `Game` class contains a static class variable for the minimum bet value.
    ```py
    class Game:
        min_bet = 20
    ```

- Upon initialization, several instance variables are defined:
    ```py
        def __init__(self):
            self.deck = Deck()        # a new instance of the Deck class
            self.player = Player()    # a new instance of the Player class, representing the human player
            self.computer = Player()  # a new instance of the Player class, representing the AI player
            self.community = list()   # an empty list which will hold the community cards
            self.pot = 0              # an integer which will represent the community pot value
            self.stage = 'opening'    # a string which represents the current stage of the game
            self.draw = False         # when set to True, this indicates that the current round has ended in a draw
    ```

- Next, the deck is shuffled:
    ```py
            self.deck.shuffle()
    ```
    
- Finally, the first two cards are drawn for each player, as well as the five community cards. These loops use the wildcard variable of `_` since the variable itself is not referenced during the loop.
    ```py
            for _ in range(2): self.deck.draw(self.player.cards)
            for _ in range(2): self.deck.draw(self.computer.cards)
            for _ in range(5): self.deck.draw(self.community)
    ```

##### `new_game()` 

- The `new_game` method re-initalizes the current instance of `Game`, resetting all instance variables to their default values.
    ```py
        def new_game(self):
            self.__init__()
    ```

##### `new_round()` 

- The `new_round` method is called at the conclusion of each round. First, it generates a new instance of `Deck`, sets the `stage` flag, and resets the `won` status for both players to `False`.
    ```py
        def new_round(self):
            self.deck = Deck()
            self.stage = 'next'
            self.player.won = False
            self.computer.won = False
    ```

- Next, all player hands are emptied as well as the community hand, then the new deck is shuffled.
    ```py
            self.player.cards.clear()
            self.computer.cards.clear()
            self.community.clear()
            self.deck.shuffle()
    ```

- Finally, new cards are drawn for both players and the community pool.
    ```py
            for _c in range(2): self.deck.draw(self.player.cards)
            for _c in range(2): self.deck.draw(self.computer.cards)
            for _c in range(5): self.deck.draw(self.community)
    ```

##### `update_banks()` 

- The `update_banks` method adds the `pot` to the winning player's `funds` at the end of the round. If the round is a draw, the `pot` is split between both players. The pot is reset to `0` after being distributed.
    ```py
        def update_banks(self):
            if self.player.won:
                self.player.funds += self.pot
            elif self.computer.won:
                self.computer.funds += self.pot
            elif self.draw:
                self.player.funds += int(self.pot/2)
                self.computer.funds += int(self.pot/2)
    
            self.pot = 0
    ```

##### `check_hand()` 

- The `check_hand` method iterates through all possible winning hands and compares them to the player's hand until it finds a match. It requires one argument, which is the `hand` to be checked. A list of `suits` is defined within this method to be referenced by its many submethods.
    ```py
        def check_hand(self, hand):
            suits = ['c', 'd', 'h', 's']
    ```

##### `hand_gen()`

- This submethod of `check_hand` is used to generate a `list` which contains a winning hand. It requires a single-letter `suit` argument, as well as `start` and `stop` points for the `range` function. It combines the `suit` with each number in the `range` iteration to generate a `list` of card IDs. This submethod can be seen in action below as we take a look into submethods for each winning hand.
    ```py
            def hand_gen(suit, start, stop):
                return [f'{num}{suit}' for num in range(start, stop)]
    ```

##### `check_subset()` 

- This submethod requires two arguments: `hand`, the player's hand, and `winning_hands`, a "superlist" of winning hands. It iterates through each winning hand and compares it to the player's hand. If there is a match it returns `True`, otherwise it returns `False`. For each iteration, it converts both hands to `sets`. This allows us to use the built-in `issubset` method for comparing hands without having to worry about each `list` being identically ordered.
    ```py
            def check_subset(hand, winning_hands):
                for wh in winning_hands:
                    if set(wh).issubset(set(hand)):
                        return True
                
                return False
    ```

##### `royal_flush()` 

- The first of the winning hand submethods, the `royal_flush` submethod utilizes the `hand_gen` and `check_subset` submethods to determine if the player is holding a Royal Flush. It iterates through each `suit`, using `hand_gen` to produce a 4-card hand with values 10-13 (10 thru King) before appending the Ace to the end of the `list`. Once the "superlist" of winning hands is generated, it is passed into the `check_subset` submethod along with the player's `hand` to determine if there is a match.
    ```py
            def royal_flush():
                winning_hands = [hand_gen(suit, 10, 14) + [f'1{suit}'] for suit in suits]
                return check_subset(hand, winning_hands)
    ```

- By adding a `print` statement inside of this submethod, we can see that the hand generator behaves as expected by producing a "superlist" of every possible Royal Flush combination.
    ```py
    print(winning_hands)
    [['10c', '11c', '12c', '13c', '1c'],
     ['10d', '11d', '12d', '13d', '1d'],
     ['10h', '11h', '12h', '13h', '1h'],
     ['10s', '11s', '12s', '13s', '1s']]
    ```

##### `straight_flush()` 

- The `straight_flush` submethod is very similar to `royal_flush`, with a small difference in the process for generating `winning_hands`. Once again iterating through every `suit`, then iterating through numbers 1-9, it takes that `num` and passes it to the `hand_gen` submethod with a `start` of `num` and a `stop` of `num+5`. For instance, while the `num` is 1, it will generate a hand of 1 (Ace) thru 5 for the current `suit`. Continuing on to the next iteration, it will produce 2-6, then 3-7, et cetera, ending at range 9-13 for each `suit`.
    ```py
            def straight_flush():
                winning_hands = [hand_gen(suit, num, num+5) for num in range(1, 10) for suit in suits]
                return check_subset(hand, winning_hands)
    ```

##### `four_of_a_kind()` 

- The `four_of_a_kind` submethod takes a similar approach to the previous two submethods. It loops through the full range of possible card values (1-13) to generate one matching set of values for each `suit`. Since the `hand_gen` submethod will only return one item per iteration, we use `str().join()` to convert the contents of the returned `list` to a `str`. Calling `hand_gen(suit, num, num+1)[0]` would produce an identical result.
    ```py
            def four_of_a_kind():
                winning_hands = [[str().join(hand_gen(suit, num, num+1)) for suit in suits] for num in range(1, 14)]
                return check_subset(hand, winning_hands)
    ```

##### `full_house()` 

- The `full_house` submethod takes a different approach than the previous submethods. It doesn't rely on the `hand_gen` and `check_subset` submethods. Instead, it generates a list of `values` by iterating through each card in the player's hand and stripping out the `suit` identifier, leaving only the numerical value for the card. Then it generates a `list` of `counts` by using the `list` method `count()` for each value in `values`. If `counts` contains values of `2` and `3` simultaneously, this indicates that the player has a Full House and the submethod returns `True`.
    ```py
            def full_house():
                values = [str(card)[:-1] for card in hand]
                counts = [values.count(v) for v in values]
    
                return True if 2 in counts and 3 in counts else False 
    ```

- By generating a mock `hand` of seven cards and printing out both lists, we can see that `values` returns the `hand` with the `suit` identifiers stripped out; while `counts` returns a `list` of the same length where each card value is replaced with the `count()` of that value in the `hand`.
    ```py
    >>> hand = ['5h', '5c', '1c', '5d', '12s', '3s', '3d']
    >>> values = [str(card)[:-1] for card in hand]
    >>> counts = [values.count(v) for v in values]
    >>> print(values, counts)
    ['5', '5', '1', '5', '12', '3', '3']
    [3, 3, 1, 3, 1, 2, 2]
    ```


##### `flush()` 

- The `flush` submethod is very similar to `full_house`. However, it strips out the numerical value for each card and generates a `list` of `suits` instead of a `list` of `values`. It then counts the number of times that each `suit` appears in the `hand` and returns `True` if the count of any `suit` is equal to `5`.
    ```py
            def flush():
                suits = [str(card)[-1] for card in hand]
                counts = [suits.count(s) for s in suits]
    
                return True if 5 in counts else False
    ```

##### `straight()` 

- The `straight` submethod generates a list of `values` in a similar fashion to the `full_house` method, except it converts each value within the `list` to an `int`. It also generates a "superlist" of  `winning_hands`, much like our first three submethods, the only difference being that it disregards the `suit` type as we only care about the numerical card values in this case. After the initial "superlist" of `winning_hands` is generated, an additional `list` is appended to it in order to account for an Ace-high Straight. Next we iterate through each winning hand and check for matching subsets in the same fashion as the `check_subset` submethod. The only difference here is that we're comparing a `list` of integers to a `list` of strings. In order to do this, we use the `map()` function to convert each winning hand to integers, before converting it back into a `list`, then into a `set`, where we again use the `issubset()` method to check for matches and return `True`.
    ```py
            def straight():
                values = [int(str(card)[:-1]) for card in hand]
                winning_hands = [hand_gen(str(), num, num+5) for num in range(1, 10)]
                winning_hands.append(['10', '11', '12', '13', '1'])
    
                for wh in winning_hands:
                    if set(list(map(int, wh))).issubset(set(values)):
                        return True
                
                return False 
    ```

##### `three_of_a_kind()` 

- The `three_of_a_kind` submethod is nearly identical to our previous submethods which rely on `counts` and `values`, except that it returns `True` any time `counts` includes a value of `3`.
    ```py
            def three_of_a_kind():
                values = [str(card)[:-1] for card in hand]
                counts = [values.count(v) for v in values]
    
                return True if 3 in counts else False
    ```

##### `two_pairs()` 

- The `two_pairs` submethod once again relies on `counts` and `values`. The `return` statement searches the `list` of `counts` specifically for a `count()` of `2`. If `counts.count(2)` is greater than or equal to `4`, this indicates that the player's hand contains at least two pairs of cards and the submethod returns `True`.
    ```py
            def two_pairs():
                values = [str(card)[:-1] for card in hand]
                counts = [values.count(v) for v in values]
    
                return True if counts.count(2) >= 4 else False
    ```

##### `pair()` 

- The `pair` submethod is almost identical to `two_pairs`, except it only expects `counts.count(2)` to be greater than or equal to `2` instead of `4`.
    ```py
            def pair():
                values = [str(card)[:-1] for card in hand]
                counts = [values.count(v) for v in values]
    
                return True if counts.count(2) >= 2 else False
    ```

##### `highcard()` 

- The final submethod of the `check_hand` method, `highcard` converts the numerical value of each card to an `int`, then sorts that `list` of `values` in ascending order. If there is a `1` (Ace) in the `list` of `values`, then the submethod returns `14` to represent the Ace as the highest possible numerical card value. If there is no Ace in `values`, the submethod simply returns the highest value from the sorted values `list`.
    ```py
            def highcard():
                values = sorted([int(str(card)[:-1]) for card in hand])
                return 14 if 1 in values else values[-1]
    ```

##### `check_hand()` (continued...) 
- Finally, the `check_hand` method executues a conditional statement, calling each of the submethod until it finds a match for the player's hand. When a match is found, the method returns a tuple containing an `int` which represents the hierarchal value of the hand, as well as a `str` which displays the name of the hand that the player is holding. The `highcard` tuple contains an additional item, which is the numerical value of the highcard that the player is holding.
    ```py
            if   royal_flush():     return (10, 'Royal Flush')
            elif straight_flush():  return (9,  'Straight Flush')
            elif four_of_a_kind():  return (8,  'Four of a Kind')
            elif full_house():      return (7,  'Full House')
            elif flush():           return (6,  'Flush')
            elif straight():        return (5,  'Straight')
            elif three_of_a_kind(): return (4,  'Three of a Kind')
            elif two_pairs():       return (3,  'Two Pairs')
            elif pair():            return (2,  'Pair')
            else:                   return (1,  'Highcard', highcard())
    ```

##### `run_tests()` 

- For debugging purposes, the `run_tests` method ensures that the `check_hand` method is correctly identifying each type of hand. A mock hand of each type is passed to the `check_hand` method and a variable containing the `str` representation of each hand is set by specifying the second item in each `tuple`.
    ```py
        def run_tests(self):
            royal_flush       = self.check_hand(['10s', '13s', '1c', '1d', '11s', '12s', '1s'])[1]
            straight_flush    = self.check_hand(['8c', '6h', '3h', '1d', '2h', '4h', '5h'])[1]
            four_of_a_kind    = self.check_hand(['1c', '1d', '1h', '1s', '2s', '3s', '4s'])[1]
            full_house        = self.check_hand(['6c', '4d', '2h', '2s', '3c', '3d', '3h'])[1]
            flush             = self.check_hand(['4c', '5d', '1c', '10c', '12c', '3h', '7c'])[1]
            straight_ace_low  = self.check_hand(['2d', '3c', '1c', '7d', '4d', '5s', '10h'])[1]
            straight_ace_high = self.check_hand(['1c', '2d', '13d', '3c', '11d', '10s', '12h'])[1]
            three_of_a_kind   = self.check_hand(['6c', '2d', '4c', '2s', '10d', '11h', '2h'])[1]
            two_pairs         = self.check_hand(['9c', '2d', '3c', '2s', '3h', '8c', '6c'])[1]
            pair              = self.check_hand(['7c', '4d', '2c', '9s', '5h', '4s', '10c'])[1]
            highcard_ace      = self.check_hand(['1c', '3d', '5c', '6s', '7h', '11h', '13c'])[1]
            highcard_ten      = self.check_hand(['2c', '3d', '5c', '6s', '7h', '9h', '10c'])[1]
    ```
    
- Next, we use the `assert` statement before each previously defined variable to ensure that the variable matches the expected `str` for each type of hand.
    ```py
            assert royal_flush       == 'Royal Flush'
            assert straight_flush    == 'Straight Flush'
            assert four_of_a_kind    == 'Four of a Kind'
            assert full_house        == 'Full House'
            assert flush             == 'Flush'
            assert straight_ace_low  == 'Straight'
            assert straight_ace_high == 'Straight'
            assert three_of_a_kind   == 'Three of a Kind'
            assert two_pairs         == 'Two Pairs'
            assert pair              == 'Pair'
            assert highcard_ace      == 'Highcard'
            assert highcard_ten      == 'Highcard'
    ```

##### `simulate()` 

- The `simulate` method initializes a new game and compares the hands of both players to determine a winner, printing the results to the terminal. This method uses a simplified version of the logic for determining a winner that is present within the `App` class.

### App Structure (`app.py`) 

---

All elements of the GUI are contained within the `App` class, as well as some of the game logic.

---

##### **Imports** 
- This module imports the entire [**tkinter**](https://docs.python.org/3/library/tkinter.html) library. Note that the Tkinter `messagebox` is imported separately as it does not function properly otherwise. We also import the `askinteger` function from Tkinter's `simpledialog` submodule, as well as the `sleep` function from the [**time**](https://docs.python.org/3/library/time.html) module.
    ```py
    from tkinter import *
    from tkinter import messagebox
    from tkinter.simpledialog import askinteger
    from time import sleep
    ```

##### `App()` 
- The `App` class requires one argument, a single instance of the `Game` class. All sub-elements of the `App` class are contained within the `__init__` method.
    ```py
    class App:
        def __init__(self, game):
            ...
    ```

##### `CardFrame()` 

- The `CardFrame` class is a subclass of Tkinter's `Frame` widget. Instances of this class act as containers in which card images can be placed. It presets several of the `Frame` arguments in order to reduce duplicated code.
    ```py
            class CardFrame(Frame):
                def __init__(self, master=None, bg='green', bd='2', relief='solid', relx=1, rely=1, width=75, height=99, anchor='c'):
                    super().__init__(master=master, bg=bg, bd=bd, relief=relief)
                    self.place(relx=relx, rely=rely, width=width, height=height, anchor=anchor)
    ```

##### `GameButton()` 

- The `GameButton` class is a subclass of Tkinter's `Button` widget. Much like the `CardFrame` class, its purpose is to reduce duplicated code when generating buttons with similar properties.
    ```py
            class GameButton(Button):
                def __init__(self, master=None, state='normal', text=str(), font="Terminal", bg="black", fg="orange", bd=5, relief="ridge", activebackground="orange", activeforeground="black", command=None, relx=0, rely=0, relwidth=0.1):
                    super().__init__(master=master, state=state, text=text, font=font, bg=bg, fg=fg, bd=bd, relief=relief, activebackground=activebackground, activeforeground=activeforeground,command=command)
                    self.place(relx=relx, rely=rely, relwidth=relwidth)
    ```

##### `draw_card_on_screen()` 

- The `draw_card_on_screen` method requires two arguments: `card`, a Tkinter `Label` object; `image`, the card ID string which matches the corresponding image asset filename. An additional argument, `pause`, is supported, and defaults to `True`.
- First, the `image` argument is mapped and configured to the `card.image` attribute as as a Tkinter `PhotoImage` before being placed on the screen with the `pack()` method. When `pause` is `True`, a 100ms `sleep()` timer is executed after the card is drawn on the screen in order to aid the visual effect of drawing cards. Finally, we call `root.update()` to ensure that our current card appears on-screen when executing this method within a loop.
    ```py
            def draw_card_on_screen(card, image, pause=True):
                card.image = PhotoImage(file=f'./images/{image}.gif')
                card.configure(image=card.image)
                card.pack()
                if pause: sleep(0.1)
                self.root.update()
    ```

##### `update_banks()` 

- The `update_banks` method is responsible for updating monetary values on each relative Tkinter `Label` after bets are placed. This includes the `funds` for each player as well as the `pot` value.
    ```py
            def update_banks():
                self.player_funds_label['text'] = f'My Funds: ${game.player.funds}'
                self.computer_funds_label['text'] = f'AI Funds: ${game.computer.funds}'
                self.pot_label['text'] = f'Pot: ${game.pot}'
    ```

##### `configure_buttons()` 

- The `configure_buttons` method enables or disables Tkinter `Button` states depending on which phase the game is currently in. If a players funds reach zero, it disables the Raise button regardless of the current phase.
```py
        def configure_buttons(status='default'):
            if status == 'pre-bet':
                self.deal_button.configure(state='disabled')
                self.check_button.configure(state='normal')
                self.raise_button.configure(state='normal')
                self.fold_button.configure(state='normal')
                self.reveal_button.configure(state='disabled')
            elif status == 'river':
                ...
            elif status == 'end':
                ...
            else:
                ...
            
            if game.player.funds == 0 or game.computer.funds == 0: self.raise_button.configure(state='disabled')
```

##### `deal()` 

- The `deal` method is mapped to the Deal button. When executed, it resets button configurations to the `pre-bet` phase and deals cards appropriately depending on the round before updating the `stage` flag.
- First, it prompts the player to make a bet:
    ```py
            def deal():
                self.player_status['text'] = 'Awaiting player bet...'
                self.computer_status['text'] = str()
    ```
- Next, it checks the current `stage` of the game. During the `opening` stage, pocket cards are drawn face up for the player and face down for the computer. Minimum bets are automatically placed and the game enters the next phase.
    ```py
                if game.stage == 'opening':
                    configure_buttons('pre-bet')
    
                    for card in player_pocket:   draw_card_on_screen(card, game.player.cards[player_pocket.index(card)])
                    for card in computer_pocket: draw_card_on_screen(card, 'b')
    
                    game.player.funds   -= game.min_bet
                    game.computer.funds -= game.min_bet
                    game.pot            += game.min_bet * 2
    
                    game.stage = 'pre-flop'
                    update_banks()
    ```
- When the Deal button is pressed from the `pre-flop` stage, the first three community cards are drawn on the screen and the game immediately enters the `flop` stage.
    ```py
                elif game.stage == 'pre-flop':
                    configure_buttons('pre-bet')
                    for card in flops: draw_card_on_screen(card, game.community[flops.index(card)])
                    game.stage = 'flop'
    ```
- When the Deal button is pressed from the `flop` stage, the fourth community card is drawn on the screen as the game immediately enters the `turn` phase.
    ```py
                elif game.stage == 'flop':
                    configure_buttons('pre-bet')
                    draw_card_on_screen(turn, game.community[3])
                    game.stage = 'turn'
    ```
- When the Deal button is pressed from the `turn` stage, the final community card is drawn on the screen as the game enters the `river` phase.
    ```py
                elif game.stage == 'turn':
                    configure_buttons('pre-bet')
                    draw_card_on_screen(river, game.community[4])
                    game.stage = 'river'
    ```
- Finally, when the Deal button is pressed from the `next` stage, all cards and player statuses are erased from the screen, all banks are updated, and the `stage` is reset to `opening`.
    ```py
                elif game.stage == 'next':
                    for card in all_cards: draw_card_on_screen(card, 'empty', False)
                    game.stage = 'opening'
                    self.player_status['text'] = str()
                    self.computer_status['text'] = str()
                    self.deal_button.configure(text='Deal')
                    update_banks()
    ```

##### `check()` 

- The `check` method mapped to the Check button. When executed, it updates both player status labels appropriately (since the computer player always mimics the human player's check). If the game is entering the `river` stage, the buttons are configured for that stage and the `stage` flag is set to `end`. In all other cases, the buttons are reset to the their default state.
    ```py
            def check():
                self.player_status['text']   = 'Player checked...'
                self.computer_status['text'] = 'Computer checked...'
    
                if game.stage == 'river':
                    configure_buttons('river')
                    game.stage = 'end'
                else:
                    configure_buttons()
    ```

##### `raize()` 

- The `raize` method (spelled with a "z" to avoid conflict with the native `raise` keyword) is mapped to the Raise button. This method initiates a `while` loop in which we call Tkinter's `askinteger()` function, prompting the player to enter a numerical value for their Raise. 
    ```py
            def raize():
                while True:
                    try:
                        amount = askinteger('Raise', 'How much would you like to raise?')
    ```
- After the player enters a Raise value, we check to see if the if the human player's current `funds` are greater than or equal to the `amount` that they've entered. We also ensure that the `amount` entered is greater than zero. Note that we use [**chained comparison operators**](https://www.tutorialspoint.com/chaining-comparison-operators-in-python) to achieve this a minimal fashion. If all of these checks pass, we continue to another set of nested conditions (we'll get back to those in a bit), but if any of the initial conditions return `False`, we use [**recursion**](https://www.w3schools.com/python/gloss_python_function_recursion.asp) to recall the `raize()` function and repeat the Raise prompt.
    ```py
                        if game.player.funds >= amount > 0:
                            ...  # This set of nested conditions is explained below...
                        else:
                            raize()
    ```
- Backing up to the above `if` statement, our first nested condition checks to see if the computer player's `funds` are also greater than or equal to the `amount` that was raised by the human player. If this check passes, we remove the `amount` value from each player's `funds` and add the `amount` value doubled to the `pot`. Next, we update the status labels for both players. If the player has expended all of their `funds`, they go all-in. Otherwise, they raise, and in either case the computer matches.
    ```py
                            if game.computer.funds >= amount:
                                game.pot += amount * 2
                                game.player.funds -= amount
                                game.computer.funds -= amount
    
                                if game.player.funds == 0:
                                    self.player_status['text'] = 'Player went all-in...'
                                    self.computer_status['text'] = 'Computer matched...'
                                else:
                                    self.player_status['text'] = 'Player raised...'
                                    self.computer_status['text'] = 'Computer matched...'
    ```
- If the computer player's `funds` cannot match the `amount` entered by the player, the Raise amount is capped and the computer is forced to go all-in. Finally, once the nested conditional statement has resolved, we update the banks for both players and return `False` to interrupt the `while` loop.
    ```py
                            else:
                                game.pot += game.computer.funds * 2
                                game.player.funds -= game.computer.funds
                                game.computer.funds = 0
    
                                self.player_status['text'] = 'Player capped the pot...'
                                self.computer_status['text'] = 'Computer went all-in...'
                            
                            update_banks()
                            return False
    ```
- An exception will occur if the player cancels the Raise prompt. In this case, both players now Check by default and the game continues.
    ```py
                    except:
                        self.player_status['text']   = 'Player checked...'
                        self.computer_status['text'] = 'Computer checked...'
    ```
- After the player makes a valid Raise or else cancels the Raise prompt, we update the `stage` flag and reconfigure the game buttons based on the current `stage` of the game. Finally, we return `False` to exit the `while` loop.
    ```py
                    finally:
                        if game.stage == 'river':
                            configure_buttons('river')
                            game.stage = 'end'
                        elif game.stage == 'end':
                            self.reveal_button.configure(state='normal')
                        else:
                            configure_buttons()
                            
                        return False
    ```

##### `fold()` 

- The `fold` function is mapped to the Fold button. If the player folds, the computer wins by default and the round immediately ends.
    ```py
            def fold():
                game.computer.won = True  # indicates that the computer has won
                game.stage = 'next'       # indicates that the next round is set to begin
    
                game.update_banks()       # update funds for both players
                game.new_round()          # begin the next round
    
                self.deal_button.configure(text='Next')  # the Deal button temporarily changes to Next
                configure_buttons()                      # all button states are reset to default
    
                self.player_status['text']   = 'Player folded...'        # status label indicates that the player folded
                self.computer_status['text'] = 'Computer wins the pot.'  # status label indicates that the computer won
    ```

##### `reveal()` 

- The `reveal` method is mapped to the Reveal button, which only becomes active at the end of the game when the winning hand is ready to be revealed. When executed, this function reveals the computer player's cards, disables the Reveal button, then determines the winner. The first two steps are seen below.
    ```py
            def reveal():
                for card in computer_pocket: draw_card_on_screen(card, game.computer.cards[computer_pocket.index(card)])
                self.reveal_button.configure(state='disabled')
                ...
    ```
- Next, it begins to deduce the winning hand. It starts by reading the numerical card values in each player's hand...
    ```py
                player_card_values = [int(str(game.player.cards[0])[:-1]), int(str(game.player.cards[1])[:-1])]
                computer_card_values = [int(str(game.computer.cards[0])[:-1]), int(str(game.computer.cards[1])[:-1])]
    ```
- ...then we use the `max()` function to determine the highest value card that each player is holding. If the player is holding an Ace (`1`), their kicker is set to `14` instead.
    ```py
                player_kicker = 14 if 1 in player_card_values else max(player_card_values)
                computer_kicker = 14 if 1 in computer_card_values else max(computer_card_values)
    ```
- Next, we combine each player's cards with the community pool, run it through the `Game().check_hand()` method, and assign the result to a variable.
    ```py
                player_hand = game.check_hand(game.player.cards + game.community)
                computer_hand = game.check_hand(game.computer.cards + game.community)
    ```
- The `check_hand` method returns a `tuple` containing the name of the player's hand and it's hierarchal value. We can compare those hierarchal values to deduce the winner. The first condition checks to see if the player's hand has a greater hierarchal value than the computer's hand. If this condition is `True`, the player is declared the winner.
    ```py
                if player_hand[0] > computer_hand[0]:
                    self.player_status['text'] = f'{player_hand[1]} - Player wins the pot.'
                    self.computer_status['text'] = 'Computer lost...'
                    game.player.won = True
    ```
- The next scenario gets a bit more complex. If both players have a Highcard (`1`) hand, we'll then check to see if if one player's Highcard is of greater value than the other. If one player has a more valuable Highcard, that player is declared the winner.
    ```py
                elif player_hand[0] == computer_hand[0] == 1:
                    if player_hand[2] > computer_hand[2]:
                        self.player_status['text'] = f'{player_hand[2]} high - Player wins the pot.'
                        self.computer_status['text'] = 'Computer lost...'
                        game.player.won = True
    
                    elif player_hand[2] < computer_hand[2]:
                        self.computer_status['text'] = f'{computer_hand[2]} high - Computer wins the pot.'
                        self.player_status['text'] = 'Player lost...'
                        game.computer.won = True
    ```
- If both player hands contain Highcards with equal values, we need to use the kicker to determine the winner. This usually happens when the highest value card on the board is in the community pool. Note that the kicker is derived from the player's pocket cards which they were dealt at the beginning of the game. If both players hold kickers of equal value and a winner cannot be determined, the game is a draw and the players split the pot.
    ```py
                    else:
                        if player_kicker > computer_kicker:
                            self.player_status['text'] = f'Double {player_hand[1]}, Player wins by kicker.'
                            self.computer_status['text'] = 'Computer lost the kicker...'
                            game.player.won = True
    
                        elif player_kicker < computer_kicker:
                            self.computer_status['text'] = f'Double {computer_hand[1]}, Computer wins by kicker.' 
                            self.player_status['text'] = 'Player lost the kicker...'
                            game.computer.won = True
                            
                        else:
                            self.player_status['text'] = f'{player_hand[1]} Draw - Split the pot.'
                            self.computer_status['text'] = f'{computer_hand[1]} Draw - Split the pot.'
                            game.draw = True
    ```
- We also use the same kicker logic to determine a winner if both players have non-Highcard hands of the same hierarchal value.
    ```py
                elif player_hand[0] == computer_hand[0]:
                    if player_kicker > computer_kicker:
                        ...
                    elif player_kicker < computer_kicker:
                        ...
                    else:
                        ...
    ```
- In all other cases, we can assume that the computer has the winning hand without any additional comparisons.
    ```py
                else:
                    self.computer_status['text'] = f'{computer_hand[1]} - Computer wins the pot.'
                    self.player_status['text'] = 'Player lost...'
                    game.computer.won = True
    ```
- Once the winner of the round is determined, we call `update_banks` to update each player's `funds`. Then we check to see if both players still have `funds` in their bank. If both player's `funds` are still above `0`, a new round begins. Otherwise, we check the `won` flag for each player to determine the winner of the game and show a pop-up message.
    ```py
                game.update_banks()
                
                if game.player.funds > 0 and game.computer.funds > 0:
                    self.deal_button.configure(text='Next')
                    game.new_round()
                    configure_buttons()
                else:
                    if game.player.won:
                        messagebox.showinfo('Winner!', 'Computer busted!\nPlayer wins the game!')
                    elif game.computer.won:
                        messagebox.showinfo('Winner!', 'Player busted!\nComputer wins the game!')
    ```

##### `reset()` 

- The `reset` method is mapped to the Reset button and returns all aspects of the game board to their default states.
    ```py
            def reset():
                game.stage = 'opening'
                for card in all_cards: draw_card_on_screen(card, 'empty', False)
                configure_buttons()
                self.player_status['text'] = str()
                self.computer_status['text'] = str()
                game.new_game()
                update_banks()
    ```

##### `App()` (continued...) 

- The remainder of code within the `App().__init__()` method defines the Tkinter GUI components. We start out by defining our root `Tk` widget. This is the top level widget which will act as the parent for all other GUI components. Before generating any other widgets, we also define a few standard parameters for our root widget: the window size, icon, and title. We're using the Joker image for the window icon since it is not part of the standard deck.
    ```py
            self.root = Tk()
            self.root.geometry('800x600')
            self.root.iconphoto(True, PhotoImage(file="./images/j.gif"))
            self.root.title('Poker')
    ```
- Next we define a Tkinter `Frame` to emulate the surface of our poker board. Then we define our custom `CardFrames` that serve as placeholders for our `Labels`. We must call the `place()` method to display our `Frame` on the screen, but our `CardFrames` accept positional arguments for placement by default. 
    ```py
            self.background = Frame(self.root, bg='green')
            self.background.place(relwidth=1, relheight=1)
    
            self.player_card_frame1     = CardFrame(self.background, relx=0.435, rely=0.8)
            self.player_card_frame2     = CardFrame(self.background, relx=0.565, rely=0.8)
    
            self.computer_card_frame1   = CardFrame(self.background, relx=0.435, rely=0.2)
            self.computer_card_frame2   = CardFrame(self.background, relx=0.565, rely=0.2)
    
            self.community_card_frame1  = CardFrame(self.background, relx=0.25,  rely=0.5)
            self.community_card_frame2  = CardFrame(self.background, relx=0.375, rely=0.5)
            self.community_card_frame3  = CardFrame(self.background, relx=0.5,   rely=0.5)
            self.community_card_frame4  = CardFrame(self.background, relx=0.625, rely=0.5)
            self.community_card_frame5  = CardFrame(self.background, relx=0.75,  rely=0.5)
    ```
- Next we define our Tkinter `Labels`. We'll attach our card image files to these labels in order to make our cards appear on the screen.
    ```py
            self.player_card_label1     = Label(self.player_card_frame1)
            self.player_card_label2     = Label(self.player_card_frame2)
    
            self.computer_card_label1   = Label(self.computer_card_frame1)
            self.computer_card_label2   = Label(self.computer_card_frame2)
    
            self.community_card_label1  = Label(self.community_card_frame1)
            self.community_card_label2  = Label(self.community_card_frame2)
            self.community_card_label3  = Label(self.community_card_frame3)
            self.community_card_label4  = Label(self.community_card_frame4)
            self.community_card_label5  = Label(self.community_card_frame5)
    ```
- We also define some text labels to display our player banks, player statuses, minimum bet, and pot values. We can go ahead and place these labels on the screen by default.
    ```py
            self.player_funds_label   = Label(self.background, text=f'My Funds: ${game.player.funds}',   font='Terminal', bg='green')
            self.computer_funds_label = Label(self.background, text=f'AI Funds: ${game.computer.funds}', font='Terminal', bg='green')
    
            self.player_funds_label.place(relx=0.01, rely=0.01)
            self.computer_funds_label.place(relx=0.01, rely=0.05)
    
            self.pot_label = Label(self.background, text=f'Pot: ${game.pot}', font='Terminal', bg='green')
            self.min_label = Label(self.background, text=f'Minimum Bet: ${game.min_bet}', font='Terminal', bg='green')
    
            self.pot_label.place(relx=0.825, rely=0.01)
            self.min_label.place(relx=0.705, rely=0.05)
    
            self.player_status   = Label(self.background, font='Terminal', bg='green', justify='c')
            self.computer_status = Label(self.background, font='Terminal', bg='green', justify='c')
    
            self.player_status.place(rely=0.625, relwidth=1)
            self.computer_status.place(rely=0.325, relwidth=1)
    ```
- Next we'll define all of our custom `GameButton` objects. The Deal and Reset buttons are enabled by default, while the rest of the buttons are disabled until the game progresses. Much like the `CardFrame` objects, the placement of the `GameButtons` is defined upon initialization so that we don't have to call an additional method to place them on the screen.
- Note that we use a `lambda` to call our button functions when a `GameButton` is pressed. Without putting these functions inside a `lambda`, our buttons will likely break after a single execution or may not work properly at all.
    ```py
            self.deal_button   = GameButton(self.background, text="Deal",   command=lambda:deal(),   relx=0.875, rely=0.425)
            self.reset_button  = GameButton(self.background, text="Reset",  command=lambda:reset(),  relx=0.875, rely=0.525)
            self.check_button  = GameButton(self.background, text="Check",  command=lambda:check(),  relx=0.325, rely=0.925, state='disabled')
            self.raise_button  = GameButton(self.background, text="Raise",  command=lambda:raize(),  relx=0.45,  rely=0.925, state='disabled')
            self.fold_button   = GameButton(self.background, text="Fold",   command=lambda:fold(),   relx=0.575, rely=0.925, state='disabled')
            self.reveal_button = GameButton(self.background, text="Reveal", command=lambda:reveal(), relx=0.45,  rely=0.025, state='disabled')
    ```
- We define a `list` containing all of our card labels so that they can easily be iterated through as a group.
    ```py
            all_cards = [self.player_card_label1,
                         self.player_card_label2,
                         self.computer_card_label1,
                         self.computer_card_label2,
                         self.community_card_label1,
                         self.community_card_label2,
                         self.community_card_label3,
                         self.community_card_label4,
                         self.community_card_label5]
    ```
- We also define lists that group our pocket and flop cards together. This allows for easy reference and iteration without having to remember the specific names of each label variable. Additionally, we define quick-reference variables for our `turn` and `river` card labels.
    ```py
            player_pocket   = [self.player_card_label1, self.player_card_label2]
            computer_pocket = [self.computer_card_label1, self.computer_card_label2]
            flops           = [self.community_card_label1, self.community_card_label2, self.community_card_label3]
            
            turn  = self.community_card_label4
            river = self.community_card_label5
    ```
- Finally, we call the `mainloop()` method on our parent widget to initialize the Tkinter program loop.
    ```py
            self.root.mainloop()
    ```

### Running the App (`main.py`)

---

Here we simply import our high-level components, the `Game` and `App` classes. When `main.py` is executed directly, we initialize an instance of the `Game` class within an instance of the `App` class and the program loop begins!

```py
from game import Game
from app import App

if __name__ == '__main__':
    run = App(Game())
```

Put all of the program's modules along with the `images` folder into a single directory. Then execute the `main.py` file to launch the program!

If you wish to compile the program and run it as a standalone executable without a Python dependency, you can easily do so with [**PyInstaller**](https://pypi.org/project/pyinstaller/).
