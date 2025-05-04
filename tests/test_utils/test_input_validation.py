import pytest
from chess_2.utils.input_validation import (
    InvalidNotation,
    does_piece_exist_at_pos,
    PieceDoesNotExist,
    IllegalMove,
)
from chess_2.utils.types import Position
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece


def test_does_piece_exist_at_pos_true():
    pos = Position(1, 1)
    piece = Piece(position=pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)
    piece_pos = {pos: piece}
    assert does_piece_exist_at_pos(piece_pos, piece) is True


def test_does_piece_exist_at_pos_false():
    pos = Position(1, 1)
    piece = Piece(position=pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)
    wrong_piece = Piece(position=pos, color=Color.BLACK, piece_type=PieceType.BISHOP)
    piece_pos = {pos: wrong_piece}
    assert does_piece_exist_at_pos(piece_pos, piece) is False


def test_invalid_notation_exception_message():
    move = "e2e4"
    with pytest.raises(InvalidNotation) as exc:
        raise InvalidNotation(move)
    assert "Invalid move notation: e2e4" in str(exc.value)


def test_piece_does_not_exist_exception_message():
    pos = Position(4, 4)
    with pytest.raises(PieceDoesNotExist) as exc:
        raise PieceDoesNotExist(pos)
    assert f"Piece specified not found at position {pos}" in str(exc.value)
