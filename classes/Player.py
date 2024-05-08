import random
from lib.MongoDBClient import MongoDBClient

class Player:
    def __init__(self):
        self.hand = []
        self.readeds = []
        self.will_save_results = True
        self.hold_data_round = {
            "hand": [],
            "decisions": [],
            "current_points": 0,
            "result": None
        }
        
        self.setup_player()

    def add_card_to_hand(self, card):
        self.hold_data_round["hand"].append(card)

    def read_card(self, card):
        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$push": {"readed": card.__dict__}})
            
        self.readeds.append(card)

    def count_point(self):
        total = 0
        has_an_ace = False
        for card in self.hold_data_round["hand"]:
            if (card.rank >= 10):
                total += 10
            elif (card.rank == 1):
                total += 11
                has_an_ace = True
            else:
                total += card.rank

            if (total > 21 and has_an_ace):
                total -= 10

        self.hold_data_round["current_points"] = total

        return total

    def random_decide(self):
        decision = random.randrange(2)

        decision = {
            "decision": decision,
            "current_points": self.current_points,
            "hand_length": len(self.hold_data_round["hand"]),
            "readeds_length": len(self.readeds)
        }

        self.hold_data_round["decisions"].append(decision)

    def setup_player(self):
        self.player_register = MongoDBClient.player.insert_one({})

    def store_result(self, data):
        # Save the result of this round
        
        # Transform hand atribute in a list of dictionaries
        self.hold_data_round["hand"] = [card.__dict__ for card in self.hold_data_round["hand"]]

        self.hold_data_round["result"] = data

        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$push": {"results": self.hold_data_round}})

    def set_num_of_decks(self, num_of_decks):
        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$set": {"num_of_decks": num_of_decks}})

    def set_current_round(self, current_round):
        self.hold_data_round = {
            "hand": [],
            "decisions": [],
            "current_points": 0,
            "result": None
        }

        self.current_round = current_round

        if self.will_save_results:
            MongoDBClient.player.update_one({"_id": self.player_register.inserted_id}, {"$set": {"current_round": current_round}})

    def decide(self, decision):
        decision = {
            "decision": bool(decision),
            "current_points": self.current_points,
            "hand_length": len(self.hold_data_round["hand"]),
            "readeds_length": len(self.readeds)
        }

        self.hold_data_round["decisions"].append(decision)

    def get_last_decision(self):
        if self.hold_data_round["decisions"]:
            return self.hold_data_round["decisions"][-1].get("decision")
        else:
            return False
            
    @property
    def current_points(self):
        return self.hold_data_round["current_points"]      