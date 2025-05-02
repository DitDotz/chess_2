from chess_2.utils.enums import Color, PieceType

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