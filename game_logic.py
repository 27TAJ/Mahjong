import random
from deck import Deck
from game_state import gameState


roll_sum = 0
cur_break_index = 0
cur_bonus_index = 0


    # Returns the playing deck as a 2-D List
    # @Return: List
def create_playing_deck():
    rows = 2
    columns = 72
    deck = Deck()
    deck.shuffle_deck()
    index = 0
    playing_deck = [[] for _ in range(rows)]
    for r in range(rows):
        for c in range(columns):
            playing_deck[r].append(deck[index])
            index += 1
    return playing_deck

    # Returns the value of roll_sum
    # @Return: Int
def get_roll_sum():
    global roll_sum
    return roll_sum


    # Returns left of the break index to indicate where players start getting their tiles ; Sets bonus index
    # @Param: Int sum_roll
    # @Return: Int
def find_break(sum_roll):
    x = (sum_roll % 4)/4-0.25
    if x < 0:
        x = 0.75

    bonus_index = (x * 72 + (18-sum_roll))
    break_index = bonus_index-1
    set_bonus_index(int(bonus_index))
    return int(break_index)

    # Rolls 2 dice to get a sum 2-12
    # @Return: void
def roll_dice():
    global roll_sum
    roll_sum = random.randint(2, 12)

    # Deals the initial players hands (4 tiles each until they each have 16)
    # @Param: List players
    # @Param: List playing_deck
    # @Return: void
def deal_player_hands(players, playing_deck):
    set_break_index(find_break(get_roll_sum()))
    for i in range(4):
        for player in players:
            for j in range(4):
                deal_tile(playing_deck, player, get_break_index())

    # Sets the current break_index
    # @Param: Int index
    # @Return: void
def set_break_index(index):
    global cur_break_index
    cur_break_index = index
    if cur_break_index < 0:
        cur_break_index = 71


    # Returns the current break_index
    # @Return: void
def get_break_index():
    global cur_break_index
    return cur_break_index

    # Returns the current bonus_index
    # @Return: void
def get_bonus_index():
    global cur_bonus_index
    return cur_bonus_index

    #Sets the current bonus_index
    # @Param: Int index
    # @Return: void
def set_bonus_index(index):
    global cur_bonus_index
    cur_bonus_index = index

    # Sorts a players hand
    # @Param: Player player
    # @Return: void
def sort_player_hand(player):
    player.hand.sort(key=lambda tile: (tile.is_honor, tile.tile_type, tile.amount))

    # Deals 1 tile to the player from the deck and break_index // Checks if top tile is gone, if so uses bottom and changes break_index
    # @Param: List playing_deck
    # @Param: Player player
    # @Param: Int index
    # @Return: void
def deal_tile(playing_deck, player, index):

    if playing_deck[0][index] is not None:
        player.hand.append(playing_deck[0][index])
        playing_deck[0][index] = None
    else:
        player.hand.append(playing_deck[1][index])
        playing_deck[1][index] = None
        set_break_index(index-1)

    # Function to replace bonus tile from "dead wall" (tail of playing deck)
    # @Param: List playing_deck
    # @Param: Player player
    # @Return: void
def replace_bonus_tile(playing_deck, player):
    index = get_bonus_index()
    if playing_deck[0][index] is not None:
        player.hand.append(playing_deck[0][index])
        playing_deck[0][index] = None
    else:
        player.hand.append(playing_deck[1][index])
        playing_deck[1][index] = None
        if get_bonus_index() > 71:
            set_bonus_index(0)
        else:
            set_bonus_index(index+1)

    # Returns the player that is the current dealer
    # @Param: List players
    # @Return: void
def find_dealer(players):
    for player in players:
        if player.is_dealer:
            return player

    # Assigns player id's 0-3 randomly at the start of the game
    # @Param: List players
    # @Return: void
def assign_player_ids(players):
    ids = [0, 1, 2, 3]
    for player in players:
        player.player_id = random.choice(ids)
        ids.remove(player.player_id)

    # Assigns dealer boolean to player_id 1 at the start of the game
    # @Param: List players
    # @Return: void
def assign_dealer(players):
    for player in players:
        if player.player_id == 0:
            player.is_dealer = True

    # Checks each players hand from East to North and reveals bonus tiles, replacing them with normal. Loops until no more bonus tiles in each players hand
    # @Param: List players
    # @Param: List playing_deck
    # @Return: void
def check_init_bonus_tiles(players, playing_deck):
    all_removed = False

    while not all_removed:
        all_removed = True
        for player in players:
            bonus_tiles = [tile for tile in player.hand if is_bonus_tile(tile)]
            for tile in bonus_tiles:
                player.bonus_hand.append(tile)
                player.hand.remove(tile)
                replace_bonus_tile(playing_deck, player)
        for player in players:
            for tile in player.hand:
                if is_bonus_tile(tile):
                    all_removed = False

    # Returns whether a players hand contains bonus tiles.
    # @Param: Player player
    # @Return: boolean
def contains_bonus_tiles(player):
    for tile in player.hand:
        if tile.is_bonus:
            return True
    return False

    # Returns whether a tile is a bonus tile or not // Checks if tile is None
    # @Param: Tile tile
    # @Return: boolean
def is_bonus_tile(tile):
    if tile is None:
        return False
    return tile.is_bonus is True

    # Prepares a new round
    # @Param: GameState game_state
    # @Param: List players
    # @Return void
def prep_new_round(game_state, players):
    playing_deck = create_playing_deck()
    game_state.set_playing_deck(playing_deck)

    roll_dice()

    deal_player_hands(players, playing_deck)
    check_init_bonus_tiles(players, playing_deck)
    for player in players:
        sort_player_hand(player)

    # Returns boolean to whether or not a given tile could allow a player to chow
    # @Param: Player player
    # @Param: Tile tile
    # @Return: boolean
def can_make_chow(player, tile):
    discard_tile_amount = tile.amount
    discard_tile_type = tile.tile_type
    if 2 < discard_tile_amount < 8:
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand):
            return True
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 2 for tile in player.hand):
            return True
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 2 for tile in player.hand):
            return True
    elif discard_tile_amount == 2:
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 2 for tile in player.hand):
            return True
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand):
            return True
    elif discard_tile_amount == 8:
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 2 for tile in player.hand):
            return True
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand):
            return True
    elif discard_tile_amount == 1:
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount + 2 for tile in player.hand):
            return True
    elif discard_tile_amount == 9:
        if any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 1 for tile in player.hand) and any(tile.tile_type == discard_tile_type and tile.amount == discard_tile_amount - 2 for tile in player.hand):
            return True
    return False

    # Returns boolean whether a player can eat the last discarded tile.
    # @Param: Player player
    # @Param: List discard_pile
    # @Return: boolean
def can_eat(player, discard_pile):
    if len(discard_pile) == 0:
        return False
    tile = discard_pile[len(discard_pile) - 1]
    if can_make_chow(player, tile):
        return True
    return False

    # Removes a tile from players hand and adds it to the discard pile
    # @Param: Player player
    # @Param: Tile tile
    # @Param: List pile
    # @Return: void
def discard_tile(player, tile, pile):
    player.hand.remove(tile)
    pile.append(tile)

    # Returns whether a player can pong
    # @Param: Player player
    # @Param: Tile tile
    # @Return: boolean
def can_pong(player, tile):
    count = 0
    for each_tile in player.hand:
        if each_tile.tile_type == tile.tile_type and each_tile.amount == tile.amount:
            count += 1
    if count == 2:
        return True
    else:
        return False

    # Returns whether a player can kong
    # @Param: Player player
    # @Param: Tile tile
    # @Return: boolean
def can_kong(player, tile):
    count = 0
    for each_tile in player.hand:
        if each_tile.tile_type == tile.tile_type and each_tile.amount == tile.amount:
            count += 1
    if count == 3:
        return True
    else:
        return False

    #checks if a kong is drawn
    # @Param: Player player
    # @Param: Tile tile
    # @Return: boolean
def check_drawn_kong(player, tile):
    count = 0
    for each_tile in player.hand:
        if each_tile.tile_type == tile.tile_type and each_tile.amount == tile.amount:
            count += 1
    if count == 4:
        return True
    return False


    # Pongs or kong's a tile for a user
    # @Param: Player player
    # @Param: Tile tile
    # @Return: void
def pong_or_kong(player, tile):
    new_pong_or_kong = []

    for each_tile in player.hand:
        if each_tile.tile_type == tile.tile_type and each_tile.amount == tile.amount:
            new_pong_or_kong.append(each_tile)
            player.hand.remove(each_tile)
    new_pong_or_kong.append(tile)
    player.revealed_hand.append(new_pong_or_kong)

    # Initializes the game
def initialize_game(players):

    game_state = gameState()

    assign_player_ids(players)
    assign_dealer(players)
    players.sort(key=lambda p: player.player_id)
    game_state.set_players(players)


    playing_deck = create_playing_deck()
    game_state.set_playing_deck(playing_deck)
    game_state.set_dealer(find_dealer(players))

    roll_dice()

    game_state.set_round(1)

    deal_player_hands(players, playing_deck)
    check_init_bonus_tiles(players, playing_deck)
    for player in players:
        sort_player_hand(player)




