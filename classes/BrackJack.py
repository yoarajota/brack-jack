
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
        for player in self.players:
            player.read_card(card)

    def deal_card(self, player):
        card = self.draw_card()
        player.add_card_to_hand(card)
        self.all_players_read_card(card)

    def all_players_stoped(self):
        count_stoped = 0

        for player in self.players:
            if player.is_done or player in self.current_round_loosers:
                count_stoped += 1

        return count_stoped == len(self.players)

    def player_turn(self, player):
        self.deal_card(player)
        player.count_point()

        if player.current_points > 21:
            self.current_round_loosers.append(player)
            self.lost(player)

        if player.current_points == 21:
            player.is_done = True
        else: 
            player.decide()

    def players_turn(self):
        while not self.all_players_stoped():
            for player in self.players:
                if not player.is_done or player not in self.current_round_loosers:
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
        return len(self.cards) > 10

    def play(self):
        while self.can_play_round():
            self.round += 1

            for player in self.players:
                player.set_current_round(self.round)

            self.deal_card(self.dealer)
            self.dealer.add_card_to_hand(self.draw_card())

            self.players_turn()

            round_winners, max_players_points = self.find_round_winners()

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


    def win(self, player):
        player.store_result('win')
        print(f'{player.player_register.inserted_id} wins this round!')

    def lost(self, player):
        player.store_result('lost')
        print(f'{player.player_register.inserted_id} lost this round!')