from typing import Optional, Dict, Tuple

from chess_2.utils.enums import Color

from chess_2.piece import Piece

class BoardState:

    def __init__(self):
        self.piece_pos: dict = {} # piece : tuple
        self.player_turn = Color.WHITE # default
        
    def switch_player_turn(self):
        """
        Switches player turn
        """
        self.player_turn = Color.BLACK if self.player_turn == Color.WHITE else Color.WHITE

    
    def set_piece_location(self.piece_pos:dict, position: str, piece: str) -> None:
        """
        Sets the piece at a given position.
        """
        pass

