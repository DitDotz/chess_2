import pytest
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.move_validation import (
    is_within_board,
    is_square_empty,
    is_occupied_by_ally,
    is_occupied_by_opposing,
    has_moved,
    has_horizontal_path_clear_between,
    can_castle_kingside,
    can_castle_queenside
)

from ..helpers import place_king

def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }


def test_is_within_board():
    assert is_within_board(Position(0, 0)) is True
    assert is_within_board(Position(7, 7)) is True
    assert is_within_board(Position(-1, 0)) is False
    assert is_within_board(Position(0, 8)) is False

def test_is_square_empty():
    board = generate_empty_board()
    assert is_square_empty(board, Position(3, 3)) is True
    board[Position(3, 3)] = Piece(position=Position(3, 3), color=Color.BLACK, piece_type=PieceType.KNIGHT)
    assert is_square_empty(board, Position(3, 3)) is False

def test_is_occupied_by_ally():
    board = generate_empty_board()
    board[Position(4, 4)] = Piece(position=Position(4, 4), color=Color.WHITE, piece_type=PieceType.BISHOP)
    assert is_occupied_by_ally(board, Position(4, 4), Color.WHITE) is True
    assert is_occupied_by_ally(board, Position(4, 4), Color.BLACK) is False

def test_is_occupied_by_opposing():
    board = generate_empty_board()
    board[Position(2, 2)] = Piece(position=Position(2, 2), color=Color.BLACK, piece_type=PieceType.ROOK)
    assert is_occupied_by_opposing(board, Position(2, 2), Color.WHITE) is True
    assert is_occupied_by_opposing(board, Position(2, 2), Color.BLACK) is False
    assert is_occupied_by_opposing(board, Position(2, 2), Color.NONE) is True

def test_has_moved():
    piece = Piece(position=Position(0, 0), color=Color.WHITE, piece_type=PieceType.ROOK, has_moved=True)
    assert has_moved(piece) is True
    piece.has_moved = False
    assert has_moved(piece) is False

def has_horizontal_path_clear_between():
    board = generate_empty_board()
    assert has_horizontal_path_clear_between(board, Position(7, 4), Position(7, 7)) is True
    board[Position(7, 5)] = Piece(position=Position(7, 5), color=Color.WHITE, piece_type=PieceType.KNIGHT)
    assert has_horizontal_path_clear_between(board, Position(7, 4), Position(7, 7)) is False

def test_castling_not_possible_without_rook():
    board = generate_empty_board()
    place_king(board, color=Color.WHITE, pos="e1")  # King in place, rook missing

    assert can_castle_kingside(Color.WHITE, board) is False
    assert can_castle_queenside(Color.WHITE, board) is False

def test_can_castle_kingside_white_true():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")
    rook_pos = Position(7, 7)  # h1
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    assert can_castle_kingside(Color.WHITE, board) is True


def test_can_castle_kingside_black_true():
    board = generate_empty_board()
    place_king(board, Color.BLACK, pos="e8")
    rook_pos = Position(0, 7)  # h8
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    assert can_castle_kingside(Color.BLACK, board) is True


def test_can_castle_kingside_false_if_king_moved():
    board = generate_empty_board()
    king_pos = Position(7, 4)
    board[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING, has_moved=True)
    board[Position(7, 7)] = Piece(position=Position(7, 7), color=Color.WHITE, piece_type=PieceType.ROOK)

    assert can_castle_kingside(Color.WHITE, board) is False


def test_can_castle_kingside_false_if_rook_moved():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")
    rook_pos = Position(7, 7)
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK, has_moved=True)

    assert can_castle_kingside(Color.WHITE, board) is False


def test_can_castle_kingside_false_if_blocked():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")
    board[Position(7, 5)] = Piece(position=Position(7, 5), color=Color.WHITE, piece_type=PieceType.KNIGHT)
    board[Position(7, 7)] = Piece(position=Position(7, 7), color=Color.WHITE, piece_type=PieceType.ROOK)

    assert can_castle_kingside(Color.WHITE, board) is False


def test_can_castle_queenside_white_true():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")
    board[Position(7, 0)] = Piece(position=Position(7, 0), color=Color.WHITE, piece_type=PieceType.ROOK)

    assert can_castle_queenside(Color.WHITE, board) is True


def test_can_castle_queenside_false_if_squares_attacked():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")
    board[Position(7, 0)] = Piece(position=Position(7, 0), color=Color.WHITE, piece_type=PieceType.ROOK)
    board[Position(0, 3)] = Piece(position=Position(0, 3), color=Color.BLACK, piece_type=PieceType.ROOK)

    assert can_castle_queenside(Color.WHITE, board) is False