from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askinteger
from time import sleep


# Framework for the GUI and related components
class App:
    def __init__(self, game):
        # Custom Tk subclass for creating card placeholders
        class CardFrame(Frame):
            def __init__(self, master=None, bg='green', bd='2', relief='solid', relx=1, rely=1, width=75, height=99,
                         anchor='c'):
                super().__init__(master=master, bg=bg, bd=bd, relief=relief)
                self.place(relx=relx, rely=rely, width=width, height=height, anchor=anchor)

        # Custom Tk sublass for creating game buttons
        class GameButton(Button):
            def __init__(self, master=None, state='normal', text=str(), font="Terminal", bg="black", fg="orange", bd=5,
                         relief="ridge", activebackground="orange", activeforeground="black", command=None, relx=0,
                         rely=0, relwidth=0.1):
                super().__init__(master=master, state=state, text=text, font=font, bg=bg, fg=fg, bd=bd, relief=relief,
                                 activebackground=activebackground, activeforeground=activeforeground, command=command)
                self.place(relx=relx, rely=rely, relwidth=relwidth)

        # Draw card images on the screen
        def draw_card_on_screen(card, image, pause=True):
            card.image = PhotoImage(file=f'./images/{image}.gif')
            card.configure(image=card.image)
            card.pack()
            if pause: sleep(0.1)
            self.root.update()

        # Update the pot and player/AI banks after bets are made
        def update_banks():
            self.player_funds_label['text'] = f'My Funds: ${game.player.funds}'
            self.computer_funds_label['text'] = f'AI Funds: ${game.computer.funds}'
            self.pot_label['text'] = f'Pot: ${game.pot}'

        # Enable/disable buttons according to the round
        def configure_buttons(status='default'):
            if status == 'pre-bet':
                self.deal_button.configure(state='disabled')
                self.check_button.configure(state='normal')
                self.raise_button.configure(state='normal')
                self.fold_button.configure(state='normal')
                self.reveal_button.configure(state='disabled')
            elif status == 'river':
                self.deal_button.configure(state='disabled')
                self.check_button.configure(state='disabled')
                self.raise_button.configure(state='disabled')
                self.fold_button.configure(state='disabled')
                self.reveal_button.configure(state='normal')
            elif status == 'end':
                self.deal_button.configure(state='disabled')
                self.check_button.configure(state='disabled')
                self.raise_button.configure(state='disabled')
                self.fold_button.configure(state='disabled')
                self.reveal_button.configure(state='disabled')
            else:
                self.deal_button.configure(state='normal')
                self.check_button.configure(state='disabled')
                self.raise_button.configure(state='disabled')
                self.fold_button.configure(state='disabled')
                self.reveal_button.configure(state='disabled')

            # Remove the ability to raise after a player empties their bank
            if game.player.funds == 0 or game.computer.funds == 0: self.raise_button.configure(state='disabled')

        # Deal the appropriate cards and update button configurations based on the current round
        def deal():
            self.player_status['text'] = 'Awaiting player bet...'
            self.computer_status['text'] = str()

            if game.stage == 'opening':
                configure_buttons('pre-bet')

                for card in player_pocket:   draw_card_on_screen(card, game.player.cards[player_pocket.index(card)])
                for card in computer_pocket: draw_card_on_screen(card, 'b')

                game.player.funds -= game.min_bet
                game.computer.funds -= game.min_bet
                game.pot += game.min_bet * 2

                game.stage = 'pre-flop'
                update_banks()

            elif game.stage == 'pre-flop':
                configure_buttons('pre-bet')
                for card in flops: draw_card_on_screen(card, game.community[flops.index(card)])
                game.stage = 'flop'

            elif game.stage == 'flop':
                configure_buttons('pre-bet')
                draw_card_on_screen(turn, game.community[3])
                game.stage = 'turn'

            elif game.stage == 'turn':
                configure_buttons('pre-bet')
                draw_card_on_screen(river, game.community[4])
                game.stage = 'river'
            elif game.stage == 'next':
                for card in all_cards: draw_card_on_screen(card, 'empty', False)
                game.stage = 'opening'
                self.player_status['text'] = str()
                self.computer_status['text'] = str()
                self.deal_button.configure(text='Deal')
                update_banks()

        # Check the current hand and update button configuration for the next round
        def check():
            self.player_status['text'] = 'Player checked...'
            self.computer_status['text'] = 'Computer checked...'

            if game.stage == 'river':
                configure_buttons('river')
                game.stage = 'end'
            else:
                configure_buttons()

        # Raise the current hand and update button configuration for the next round
        def raize():
            while True:
                try:
                    # Ask the player for a raise value
                    amount = askinteger('Raise', 'How much would you like to raise?')

                    # Validate raise value and implement if valid
                    if game.player.funds >= amount > 0:
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

                        else:
                            game.pot += game.computer.funds * 2
                            game.player.funds -= game.computer.funds
                            game.computer.funds = 0

                            self.player_status['text'] = 'Player capped the pot...'
                            self.computer_status['text'] = 'Computer went all-in...'

                        update_banks()

                        return False

                    else:
                        raize()  # If the raise value is invalid, repeat the raise prompt

                except:
                    # If the player cancels the raise prompt, default to a check
                    self.player_status['text'] = 'Player checked...'
                    self.computer_status['text'] = 'Computer checked...'

                finally:
                    # Update button configuration based on the current phase
                    if game.stage == 'river':
                        configure_buttons('river')
                        game.stage = 'end'
                    elif game.stage == 'end':
                        self.reveal_button.configure(state='normal')
                    else:
                        configure_buttons()

                    return False

        # Fold and forfeit the current hand
        def fold():
            game.computer.won = True
            game.stage = 'next'

            game.update_banks()
            game.new_round()

            self.deal_button.configure(text='Next')
            configure_buttons()

            self.player_status['text'] = 'Player folded...'
            self.computer_status['text'] = 'Computer wins the pot.'

        # Reveal the AI player's cards and determine the winner
        def reveal():
            for card in computer_pocket: draw_card_on_screen(card, game.computer.cards[computer_pocket.index(card)])

            self.reveal_button.configure(state='disabled')

            player_card_values = [int(str(game.player.cards[0])[:-1]), int(str(game.player.cards[1])[:-1])]
            computer_card_values = [int(str(game.computer.cards[0])[:-1]), int(str(game.computer.cards[1])[:-1])]

            player_kicker = 14 if 1 in player_card_values else max(player_card_values)
            computer_kicker = 14 if 1 in computer_card_values else max(computer_card_values)

            player_hand = game.check_hand(game.player.cards + game.community)
            computer_hand = game.check_hand(game.computer.cards + game.community)

            if player_hand[0] > computer_hand[0]:
                self.player_status['text'] = f'{player_hand[1]} - Player wins the pot.'
                self.computer_status['text'] = 'Computer lost...'
                game.player.won = True

            elif player_hand[0] == computer_hand[0] == 1:
                if player_hand[2] > computer_hand[2]:
                    self.player_status['text'] = f'{player_hand[2]} high - Player wins the pot.'
                    self.computer_status['text'] = 'Computer lost...'
                    game.player.won = True

                elif player_hand[2] < computer_hand[2]:
                    self.computer_status['text'] = f'{computer_hand[2]} high - Computer wins the pot.'
                    self.player_status['text'] = 'Player lost...'
                    game.computer.won = True

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

            elif player_hand[0] == computer_hand[0]:
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

            else:
                self.computer_status['text'] = f'{computer_hand[1]} - Computer wins the pot.'
                self.player_status['text'] = 'Player lost...'
                game.computer.won = True

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

        # Reset the board to its default state
        def reset():
            game.stage = 'opening'

            for card in all_cards: draw_card_on_screen(card, 'empty', False)

            configure_buttons()

            self.player_status['text'] = str()
            self.computer_status['text'] = str()

            game.new_game()
            update_banks()

        # GUI component definitions
        self.root = Tk()
        self.root.geometry('800x600')
        self.root.iconphoto(True, PhotoImage(file="./images/j.gif"))
        self.root.title('Poker')

        # Frames
        self.background = Frame(self.root, bg='green')
        self.background.place(relwidth=1, relheight=1)

        self.player_card_frame1 = CardFrame(self.background, relx=0.435, rely=0.8)
        self.player_card_frame2 = CardFrame(self.background, relx=0.565, rely=0.8)

        self.computer_card_frame1 = CardFrame(self.background, relx=0.435, rely=0.2)
        self.computer_card_frame2 = CardFrame(self.background, relx=0.565, rely=0.2)

        self.community_card_frame1 = CardFrame(self.background, relx=0.25, rely=0.5)
        self.community_card_frame2 = CardFrame(self.background, relx=0.375, rely=0.5)
        self.community_card_frame3 = CardFrame(self.background, relx=0.5, rely=0.5)
        self.community_card_frame4 = CardFrame(self.background, relx=0.625, rely=0.5)
        self.community_card_frame5 = CardFrame(self.background, relx=0.75, rely=0.5)

        # Labels
        self.player_card_label1 = Label(self.player_card_frame1)
        self.player_card_label2 = Label(self.player_card_frame2)

        self.computer_card_label1 = Label(self.computer_card_frame1)
        self.computer_card_label2 = Label(self.computer_card_frame2)

        self.community_card_label1 = Label(self.community_card_frame1)
        self.community_card_label2 = Label(self.community_card_frame2)
        self.community_card_label3 = Label(self.community_card_frame3)
        self.community_card_label4 = Label(self.community_card_frame4)
        self.community_card_label5 = Label(self.community_card_frame5)

        self.player_funds_label = Label(self.background, text=f'My Funds: ${game.player.funds}', font='Terminal',
                                        bg='green')
        self.computer_funds_label = Label(self.background, text=f'AI Funds: ${game.computer.funds}', font='Terminal',
                                          bg='green')

        self.player_funds_label.place(relx=0.01, rely=0.01)
        self.computer_funds_label.place(relx=0.01, rely=0.05)

        self.pot_label = Label(self.background, text=f'Pot: ${game.pot}', font='Terminal', bg='green')
        self.min_label = Label(self.background, text=f'Minimum Bet: ${game.min_bet}', font='Terminal', bg='green')

        self.pot_label.place(relx=0.825, rely=0.01)
        self.min_label.place(relx=0.705, rely=0.05)

        self.player_status = Label(self.background, font='Terminal', bg='green', justify='c')
        self.computer_status = Label(self.background, font='Terminal', bg='green', justify='c')

        self.player_status.place(rely=0.625, relwidth=1)
        self.computer_status.place(rely=0.325, relwidth=1)

        # Buttons
        self.deal_button = GameButton(self.background, text="Deal", command=lambda: deal(), relx=0.875, rely=0.425)
        self.reset_button = GameButton(self.background, text="Reset", command=lambda: reset(), relx=0.875, rely=0.525)
        self.check_button = GameButton(self.background, text="Check", command=lambda: check(), relx=0.325, rely=0.925,
                                       state='disabled')
        self.raise_button = GameButton(self.background, text="Raise", command=lambda: raize(), relx=0.45, rely=0.925,
                                       state='disabled')
        self.fold_button = GameButton(self.background, text="Fold", command=lambda: fold(), relx=0.575, rely=0.925,
                                      state='disabled')
        self.reveal_button = GameButton(self.background, text="Reveal", command=lambda: reveal(), relx=0.45, rely=0.025,
                                        state='disabled')

        # Card categories for easy reference
        all_cards = [self.player_card_label1,
                     self.player_card_label2,
                     self.computer_card_label1,
                     self.computer_card_label2,
                     self.community_card_label1,
                     self.community_card_label2,
                     self.community_card_label3,
                     self.community_card_label4,
                     self.community_card_label5]

        player_pocket = [self.player_card_label1, self.player_card_label2]
        computer_pocket = [self.computer_card_label1, self.computer_card_label2]
        flops = [self.community_card_label1, self.community_card_label2, self.community_card_label3]

        turn = self.community_card_label4
        river = self.community_card_label5

        # Initialize Tkinter event loop
        self.root.mainloop()
