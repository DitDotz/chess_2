from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position

PIECE_REPR: dict[PieceType, tuple[str, str]] = {
    PieceType.EMPTY: (" ", " "),
    PieceType.PAWN: ("♙", "♟"),
    PieceType.ROOK: ("♖", "♜"),
    PieceType.BISHOP: ("♗", "♝"),
    PieceType.QUEEN: ("♕", "♛"),
    PieceType.KING: ("♔", "♚"),
    PieceType.KNIGHT: ("♘", "♞"),
}


def get_piece_repr(color:Color, piece_type:PieceType) -> str:
    """
    Get the string representation of the piece.

    Returns:
        str: The string representation of the piece based on its color and type.
    """
    if piece_type == PieceType.EMPTY or color == Color.NONE:
        return PIECE_REPR[PieceType.EMPTY][0]

    if color == Color.WHITE:
        return PIECE_REPR[piece_type][1]
    
    else:
        return PIECE_REPR[piece_type][0]
    

def generate_board_repr(board:dict[Position, PieceType]) -> str:
    """
    Generate a string representation of the chessboard based on the board state.

    Args:
        board (dict): A dictionary mapping (x, y) positions to Piece objects.

    Returns:
        str: A string representation of the chessboard.
    """

    representation = "  a   b   c   d   e   f   g   h\n"  # Column labels

    for x in range(8):
        representation += "|---" * 8 + f"| {8 - x}\n"

        for y in range(8):
            piece = board.get((x, y))
            symbol = get_piece_repr(piece.color, piece.piece_type) if piece else " "
            representation += f"| {symbol} "

        representation += "|\n"

    representation += "|---" * 8 + "|\n"
    representation += "  a   b   c   d   e   f   g   h\n"

    return representation


