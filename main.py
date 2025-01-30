#from deck import Deck
from game_logic import initialize_game
#from game_state import gameState
from player import Player

#playing_deck = create_playing_deck()

#for row in playing_deck:
#    print(row)


def main():
    players = [Player("Alice"), Player("Bob"), Player("Charlie"), Player("David")]

    game_state = initialize_game(players)


    for player in players:
        print(f"{player.name}'s Hand:")
        print(player.hand)
        print(f"{player.name}'s Bonus Hand:")
        print(player.bonus_hand)

if __name__ == "__main__":
    main()