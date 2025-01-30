from game_logic import can_eat, deal_tile, get_break_index, contains_bonus_tiles, replace_bonus_tile, can_pong, can_kong, sort_player_hand, pong_or_kong, check_drawn_kong

class gameState:
    def __init__(self):
        self.players = []
        self.playing_deck = []
        self.discard_pile = []
        self.current_turn = 0
        self.current_dealer = None
        self.round = 0
        self.last_winner = None
        self.game_over = False
        self.round_over = False

        # Sets the current playing deck
    def set_playing_deck(self, deck):
        self.playing_deck = deck

    def get_playing_deck(self):
        return self.playing_deck

        # Sets the current dealer
    def set_dealer(self, dealer):
        self.current_dealer = dealer

        # Sets the current players
    def set_players(self, players):
        self.players = players

        #Sets the current Round
    def set_round(self, cur_round):
        self.round = cur_round

        #Returns the current round
    def get_round(self):
        return self.round

        # Sets the last rounds winner
    def set_last_winner(self, winner):
        self.last_winner = winner

        # Sets the current turn using player_id
    def set_current_turn(self, turn):
        self.current_turn = turn

    def get_current_turn(self):
        return self.current_turn

    def get_discard_pile(self):
        return self.discard_pile

    def set_discard_pile(self, pile):
        self.discard_pile = pile

    def get_last_discard(self):
        return self.discard_pile[-1]

    def next_turn(self):
        self.current_turn = self.current_turn + 1 % 4

    def is_turn(self):
        player = self.players[self.current_turn]

        if not player.just_pong_or_kong:
            if can_eat(player, self.get_discard_pile()):
                # |--> if true prompt user if they would like to eat
                if yes:
                    # eat
                    player.change_just_ate()

        if not player.get_just_ate():
            # Draw a tile
            deal_tile(self.get_playing_deck(), player, get_break_index())

        # Loop until there are no bonus tiles and no kong can be made
        while contains_bonus_tiles(player) or check_drawn_kong(player, player.hand[-1]):
            # Handle bonus tiles
            while contains_bonus_tiles(player):
                for tile in player.hand:
                    if tile.is_bonus:
                        player.bonus_hand.append(tile)
                        player.hand.remove(tile)
                        replace_bonus_tile(self.get_playing_deck(), player)

            # Handle kong
            if check_drawn_kong(player, player.hand[-1]):
                pong_or_kong(player, player.hand[-1])

        # Discard tile
        sort_player_hand(player)

        # Sorts players hand
        if player.get_just_ate():
            player.change_just_ate()

        # Checks if other players can/wants to pong or kong
        for each_player in self.players:
            if not each_player.is_dealer:
                if can_kong(each_player, self.get_last_discard()):
                    if yes:
                        pong_or_kong(each_player, self.discard_pile.pop())
                        each_player.change_just_pong_or_kong()
                        self.set_current_turn(each_player.get_player_id())

                elif can_pong(each_player, self.get_last_discard()):
                    if yes:
                        pong_or_kong(each_player, self.discard_pile.pop())
                        each_player.change_just_pong_or_kong()
                        self.set_current_turn(each_player.get_player_id())
        # Changes whose turn it is
        self.next_turn()








