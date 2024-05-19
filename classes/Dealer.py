from classes.Player import Player
class DealerPlayerRegister:
    def __init__(self):
        self.inserted_id = 'dealer'

class Dealer(Player): 
    def __init__(self):
        super().__init__()

        self.will_save_results = False
        self.player_register = DealerPlayerRegister()

    def add_card_to_hand(self, card):
        if len(self.hold_data_round["hand"]) == 1:
            card.is_hidden = True

        self.hold_data_round["hand"].append(card)
        

    def show_card(self):
        self.hold_data_round["hand"][1].is_hidden = False
        return self.hold_data_round["hand"][1]

    def setup_player(self):
        # Dealer does not need to be registered
        pass