
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position

from chess_2.piece.piece import Piece

class BoardState:

    def __init__(self):
        self.piece_pos: dict[Position, Piece] = {}
        self.player_turn = Color.WHITE # default
        
    def switch_player_turn(self)->None:
        """
        Switches player turn
        """
        self.player_turn = Color.BLACK if self.player_turn == Color.WHITE else Color.WHITE

    
    def set_piece_location(self, original_pos: Position, final_pos: Position, piece: Piece) -> None:
        """
        Sets the piece at a given board position.

        Args:
            position (Position): The (x, y) coordinates on the board.
            piece (Piece): The piece to place at the given position.
        """

        piece_moved = piece_pos[original_pos]

        self.piece_pos[original_pos] = Piece(color=Color.NONE, piece_type=PieceType.EMPTY, position=original_pos)
        
        self.piece_pos[final_pos] = piece_moved




