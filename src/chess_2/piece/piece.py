from dataclasses import dataclass

from chess_2.utils.types import Position
from chess_2.utils.enums import Color, PieceType
from chess_2.board.board_representation import get_piece_repr

@dataclass
class Piece:
    position: Position 
    color: Color
    piece_type: PieceType
    has_moved:bool = False
    en_passantable:bool = False  # only valid for pawns. only True for pawn that moved 2 spaces, and returns to False after 1 turn by opposite color

    @property
    def repr(self) -> str:
        """
        Get the string representation of the piece.
        """
        return get_piece_repr(self.color, self.piece_type)
