from classes.Deck import Deck
import random
import argparse
import sys

# ['Hearts', 'Diamonds', 'Clubs', 'Spades']

def initialize_cards(num_decks=6):
    all_cards = []
    for _ in range(0, num_decks):
        deck = Deck()
        deck.remove_joker()
        deck.shuffle()
        all_cards += deck.cards
    
    random.shuffle(all_cards)
    
    return all_cards

all_cards = initialize_cards()

# hashmap
mapped = {}

for card in all_cards:
    code = card.suit[0].lower() + str(card.rank)
    mapped[code] = card

memory_hold_hand = []

print("Enter 'h', 'd', 'c', 's', with the rank to compute a card, or 'exit' to quit: ")

while(True):
    userInput = input("type: ").strip().lower()

    if userInput == 'exit':
        print("Exiting...")

        break
    elif userInput.startswith('g'):
        val = userInput[1:]

        if val in mapped:
            card = mapped[val]

            print(card)

            memory_hold_hand.append(card)
            del mapped[val]

    elif userInput.startswith('hit'):
        total = 0
        
        for card in memory_hold_hand:
            if card.rank in [11, 12, 13]:
                total += 10
            elif card.rank == 1:
                total += 11 if total + 11 <= 21 else 1
            else:
                total += card.rank
        
        print(f"Current hand value: {total}")
        
        bust_cards = 0
        safe_cards = 0
        
        for idx in mapped:
            card = mapped[idx]

            card_value = 10 if card.rank in [11, 12, 13] else card.rank

            if card.rank == 1:
                card_value = 11 if total + 11 <= 21 else 1
                
            if total + card_value > 21:
                bust_cards += 1
            else:
                safe_cards += 1
        
        total_remaining = bust_cards + safe_cards

        if total_remaining > 0:
            bust_probability = (bust_cards / total_remaining) * 100

            print(f"Probability of exceeding 21: {bust_probability:.2f}%")
            print(f"Cards that would bust: {bust_cards}/{total_remaining}")

        # DEALER DRAW LOGIC

        else:
            print("No cards remaining in the deck!")

        for card in memory_hold_hand:
            total += card.rank
    elif userInput.startswith('end'):
        memory_hold_hand = []

        print("Hand cleared.")
    else:
        if hasattr(mapped, userInput):
            del mapped[userInput];