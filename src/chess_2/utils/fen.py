
from chess_2.utils.enums import PieceType, Color
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position

# dictionary of fen as keys and PieceType as values
PIECE_TYPE_FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


def parse_fen(fen: str) -> dict[Position, Piece]:
    """
    Process the FEN string and initialize the board with the specified piece positions.

    Args:
        fen (str): The FEN string representing the piece positions.

    Returns:
        dict[Position, Piece]: A dictionary representing the board with initialized piece positions.
    """

    piece_loc: dict[Position, Piece] = {}
    rows = fen.split('/')


    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                for _ in range(int(char)):  # Repeat for the number of empty squares
                    piece_loc[Position(row=row_idx, col=col_idx)] = Piece(position=Position(row=row_idx, col=col_idx), color=Color.NONE, piece_type=PieceType.EMPTY)
                    col_idx += 1  # Move to the next column

            else:
                color = Color.WHITE if char.isupper() else Color.BLACK
                piece_type = PIECE_TYPE_FEN_MAP[char.lower()]
                piece_loc[Position(row=row_idx, col=col_idx)] = Piece(position=Position(row=row_idx, col=col_idx), color=color, piece_type=piece_type)
                col_idx += 1

    return piece_loc