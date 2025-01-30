class Tile:

    def __init__(self, tile_type, amount=0, is_honor=False, is_bonus=False):
        self.tile_type = tile_type
        self.amount = amount
        self.is_honor = is_honor
        self.is_bonus = is_bonus

    def __str__(self):
        return f'{self.tile_type}: {self.amount}'
    def __repr__(self):
        return self.__str__()