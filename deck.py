import random
from tile import Tile

class Deck:

    def __init__(self):
        tile_types = ['Bamboo', 'Barrels', 'Characters']
        tile_amounts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.deck = []

        for i in range(4):
            self.deck.extend(Tile(tile_type, amount) for tile_type in tile_types for amount in tile_amounts)
            self.add_honor_tiles()
        self.add_bonus_tiles()

    def __str__(self):
        return ' '.join(str(each_tile) for each_tile in self.deck)

    def __getitem__(self, index):
        return self.deck[index]

    # Shuffles and returns deck of tiles
    # @Return: List deck
    def shuffle_deck(self):
        random.shuffle(self.deck)
        return self.deck

    # Adds honors tiles to deck
    # @Return: void
    def add_honor_tiles(self):
        tile_types = ['North', 'South', 'East', 'West', 'Board', 'Center', 'Festival']

        self.deck.extend(Tile(tile_type, is_honor=True) for tile_type in tile_types)

    # Adds bonus tiles to deck
    # @Return: void
    def add_bonus_tiles(self):
        flower_types = ['Plum', 'Orchid', 'Chrysanthemum', 'Bamboo']
        season_types = ['Spring', 'Summer', 'Autumn', 'Winter']
        amounts = [1, 2, 3, 4]

        for i, flower in enumerate(flower_types):
            self.deck.append(Tile(flower, amounts[i], is_bonus=True))
        for i, season in enumerate(season_types):
            self.deck.append(Tile(season, amounts[i], is_bonus=True))

    # Returns length of the deck
    # @Return: Int
    def length(self):
        return len(self.deck)