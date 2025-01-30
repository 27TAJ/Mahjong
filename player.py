class Player:

    def __init__(self, name, player_id=None, just_won=False):
        self.player_id = player_id
        self.name = name
        self.hand = []
        self.bonus_hand = []
        self.revealed_hand = []
        self.is_dealer = False
        self.is_turn = False
        self.just_pong_or_kong = False
        self.just_won = just_won
        self.just_ate = False

    def get_player_id(self):
        return self.player_id

    def change_just_pong_or_kong(self):
        self.just_pong_or_kong = not self.get_just_pong_or_kong()

    def get_just_pong_or_kong(self):
        return self.just_pong_or_kong

    def change_just_ate(self):
        self.just_ate = not self.just_ate

    def get_just_ate(self):
        return self.just_ate
