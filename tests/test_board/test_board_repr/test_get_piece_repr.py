import pytest
from chess_2.board.board_representation import get_piece_repr
from chess_2.utils.enums import Color, PieceType

@pytest.mark.parametrize("color, piece_type, expected", [
    (Color.BLACK, PieceType.PAWN, "♙"),
    (Color.WHITE, PieceType.PAWN, "♟"),
    (Color.BLACK, PieceType.ROOK, "♖"),
    (Color.WHITE, PieceType.ROOK, "♜"),
    (Color.BLACK, PieceType.KNIGHT, "♘"),
    (Color.WHITE, PieceType.KNIGHT, "♞"),
    (Color.BLACK, PieceType.BISHOP, "♗"),
    (Color.WHITE, PieceType.BISHOP, "♝"),
    (Color.BLACK, PieceType.QUEEN, "♕"),
    (Color.WHITE, PieceType.QUEEN, "♛"),
    (Color.BLACK, PieceType.KING, "♔"),
    (Color.WHITE, PieceType.KING, "♚"),
    (Color.BLACK, PieceType.EMPTY, " "),
    (Color.WHITE, PieceType.EMPTY, " "),
    (Color.NONE, PieceType.PAWN, " "),  # fallback
])

def test_get_piece_repr(color, piece_type, expected):
    assert get_piece_repr(color, piece_type) == expected

