from chess_2.utils.types import Position
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece.piece import Piece

def place_king(board: dict[Position, Piece], color: Color, pos: str = None) -> None:
    """
    Places a king of the given color on the board at a specified or default position.

    Defaults:
        - White king at 'e1'
        - Black king at 'e8'
    """
    if pos is None:
        pos = "e1" if color == Color.WHITE else "e8"

    king_pos = algebraic_to_index(pos)
    board[king_pos] = Piece(position=king_pos, color=color, piece_type=PieceType.KING)

# Helper to generate a full empty board
def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }
