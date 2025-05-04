import pytest
from chess_2.piece.piece import Piece
from chess_2.utils.enums import Color, PieceType
from chess_2.piece_movement.rook import RookMovement
from chess_2.utils.types import Position


def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)}

def test_rook_valid_moves_on_clear_board():
    board = generate_empty_board()
    rook_pos = Position(4, 4)
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    rook_movement = RookMovement(board[rook_pos])
    valid_moves = rook_movement.get_potential_moves(board)

    expected_moves = [
        Position(r, 4) for r in range(8) if r != 4
    ] + [
        Position(4, c) for c in range(8) if c != 4
    ]
    assert set(valid_moves) == set(expected_moves)


def test_rook_blocked_by_ally():
    board = generate_empty_board()
    rook_pos = Position(4, 4)
    ally_pos = Position(4, 6)
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    board[ally_pos] = Piece(position=ally_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    rook_movement = RookMovement(board[rook_pos])
    valid_moves = rook_movement.get_potential_moves(board)

    assert ally_pos not in valid_moves # can't occupy ally pos
    assert Position(4, 7) not in valid_moves # can't move past ally

def test_rook_can_capture_enemy():
    board = generate_empty_board()
    rook_pos = Position(4, 4)
    enemy_pos = Position(4, 6)
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    board[enemy_pos] = Piece(position=enemy_pos, color=Color.BLACK, piece_type=PieceType.PAWN)

    rook_movement = RookMovement(board[rook_pos])
    valid_moves = rook_movement.get_potential_moves(board)

    assert enemy_pos in valid_moves # can capture opp
    assert Position(4, 7) not in valid_moves # can't move past opp
