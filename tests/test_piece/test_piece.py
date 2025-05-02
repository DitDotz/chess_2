import pytest
from chess_2.piece.piece import Piece
from chess_2.utils.enums import Color, PieceType

def test_piece_initialization():
    piece = Piece(position=(0, 1), color=Color.WHITE, piece_type=PieceType.KNIGHT)
    assert piece.position == (0, 1)
    assert piece.color == Color.WHITE
    assert piece.piece_type == PieceType.KNIGHT
    assert piece.has_moved is False
    assert piece.en_passantable is False

def test_piece_repr_white():
    piece = Piece(position=(0, 1), color=Color.WHITE, piece_type=PieceType.KING)
    assert piece.repr == "♚"  # Unicode for white king as per PIECE_STR_REPR

def test_piece_repr_black():
    piece = Piece(position=(0, 1), color=Color.BLACK, piece_type=PieceType.ROOK)
    assert piece.repr == "♖"  # Unicode for black rook as per PIECE_STR_REPR

def test_piece_repr_empty():
    piece = Piece(position=(0, 1), color=Color.NONE, piece_type=PieceType.EMPTY)
    assert piece.repr == " "
