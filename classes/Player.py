import random
from lib.MongoDBClient import MongoDBClient

class Player:
    def __init__(self):
        self.hand = []
        self.readeds = []
        self.is_done = False
        self.will_save_results = True
        
        self.setup_player()

    def add_card_to_hand(self, card):
        self.hold_data_round.hand.append(card)

    def read_card(self, card):
        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$push": {"readed": card.__dict__}})
        self.readeds.append(card)

    def count_point(self):
        total = 0
        has_an_ace = False
        for card in self.hold_data_round.hand:
            if (card.rank >= 10):
                total += 10
            elif (card.rank == 1):
                total += 11
                has_an_ace = True
            else:
                total += card.rank

            if (total > 21 and has_an_ace):
                total -= 10

        self.current_points = total

        return total

    def decide(self):
        decision = random.randrange(2)

        if decision == 0:
            self.is_done = True

        decision = {
            "decision": decision,
            "current_points": self.current_points,
            "hand_length": len(self.hold_data_round.hand),
            "readeds_length": len(self.readeds)
        }

        self.hold_data_round.decisions.append(decision)

    def setup_player(self):
        self.player_register = MongoDBClient.player.insert_one({})
        print(self.player_register)

    def store_result(self, data):
        # Save the result of this round
        result_obj = {
            "result": data,
            "round_hand_range": len(self.hold_data_round.hand),
            "round_readeds_range": len(self.readeds)
        }

        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$push": {"results": result_obj}})

    def set_num_of_decks(self, num_of_decks):
        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$set": {"num_of_decks": num_of_decks}})

    def set_current_round(self, current_round):
        self.hold_data_round = {
            hand: [],
            decisions: []
        }

        self.current_round = current_round

        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$set": {"current_round": current_round}})