from typing import List

from pydantic import BaseModel


class Tile(BaseModel):
    tile_type: str
    tile_amount: int
    is_honor: bool
    is_bonus: bool

class Player(BaseModel):
    player_id: int
    player_name: str
    hand: List[Tile]
    bonus_hand: List[Tile]
    revealed_hand: List[Tile]
    is_dealer: bool
    is_turn: bool
    just_pong_or_kong: bool
    just_won: bool
    just_ate: bool

class Deck(BaseModel):
    deck: List[Tile]

class gameState(BaseModel):
    players: List[Player]
    playing_deck: List[Tile]
    discard_pile: List[Tile]
    current_turn: int
    round: int
    last_winner: Player
    game_over: bool
    round_over: bool
