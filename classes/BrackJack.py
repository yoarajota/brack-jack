
from classes.Deck import Deck
from classes.Dealer import Dealer

class BrackJack:
    def __init__(self, player_list, number_of_decks = 6):
        self.players = player_list
        self.number_of_decks = number_of_decks

        for player in self.players:
            player.set_num_of_decks(number_of_decks)

        self.shuffle_and_cut()

        self.dealer = Dealer()

        self.current_round_loosers = []

        self.round = 0

    def shuffle_and_cut(self):
        all_cards = []

        for _ in range(0, self.number_of_decks):
            deck = Deck()
            deck.remove_joker()
            deck.shuffle()
            all_cards += deck.cards

        half = len(all_cards) // 2

        self.cards = all_cards[:half]
        self.used_cards = []

    def draw_card(self):
        if len(self.cards) > 0:
            card = self.cards.pop()
            self.used_cards.append(card)
            return card
        else:
            return None

    def all_players_read_card(self, card):
        self.log(card.__str__() + ' was readed')

        for player in self.players:
            player.read_card(card)

    def deal_card(self, player):
        card = self.draw_card()
        player.add_card_to_hand(card)
        self.all_players_read_card(card)

    def all_players_stoped(self):
        count_stoped = 0

        for player in self.players:
            if player.get_last_decision() or player in self.current_round_loosers:
                count_stoped += 1

        return count_stoped == len(self.players)

    def player_turn(self, player):
        self.log(str(player.player_register.inserted_id) + ' turn')
        self.deal_card(player)
        if len(player.hold_data_round["hand"]) == 1:
            self.deal_card(player)

        player.count_point()

        if player.current_points > 21:
            self.current_round_loosers.append(player)
            self.lost(player)
        elif player.current_points == 21:
            player.decide(True)
        else: 
            player.random_decide()

    def players_turn(self):
        for player in self.players:
            player.set_current_round(self.round)
            
        while not self.all_players_stoped():
            for player in self.players:
                if not player.get_last_decision() or player not in self.current_round_loosers:
                    self.player_turn(player)

    def find_round_winners(self):
        round_winners = []
        max_players_points = 0
        done_players = [player for player in self.players if player not in self.current_round_loosers]

        for player in done_players:
            if player.current_points > max_players_points:
                max_players_points = player.current_points
                round_winners = [player]
            elif player.current_points == max_players_points:
                round_winners.append(player)
            else:
                self.lost(player)

        return round_winners, max_players_points

    def dealer_turn(self, max_players_points):
        self.dealer.show_card()
        self.dealer.count_point()

        while self.dealer.current_points < max_players_points and self.dealer.current_points < 21:
            self.deal_card(self.dealer)
            self.dealer.count_point()

    def can_play_round(self):
        return len(self.cards) > 20
    
    def new_round(self):
        self.round += 1
        self.current_round_loosers = []
        self.dealer.set_current_round(self.round)

    def play(self):
        self.log("Starting game...")

        while self.can_play_round():
            self.log("NEW ROUND")

            self.new_round()

            self.deal_card(self.dealer)
            self.dealer.add_card_to_hand(self.draw_card())

            self.players_turn()

            round_winners, max_players_points = self.find_round_winners()

            if len(self.current_round_loosers) != len(self.players):
                self.dealer_turn(max_players_points)

                if self.dealer.current_points > 21:
                    for player in round_winners:
                        self.win(player)

                # TEMPORARY (WILL CHANGE WHEN ADDED NEW RULES)
                elif self.dealer.current_points == 21:
                    for player in round_winners:
                        self.lost(player)
                else:
                    for player in round_winners:
                        if player.current_points > self.dealer.current_points:
                            self.win(player)
                        else:
                            self.lost(player)
            else:
                self.log('All players lost, dealer does not need to play')

            self.log("END ROUND")


    def win(self, player):
        player.store_result('win')
        self.log(f'{player.player_register.inserted_id} wins this round!')

    def lost(self, player):
        player.store_result('lost')
        self.current_round_loosers.append(player)
        self.log(f'{player.player_register.inserted_id} lost this round!')

    def log(self, text):
        with open('log.txt', 'a') as f:
            f.write(str(self.round) + " - " + text + '\n')
            f.close()