import pytest
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece_movement.knight import KnightMovement

from ..helpers import place_king

def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }

def test_knight_potential_moves_on_clear_board():
    board = generate_empty_board()
    place_king(board=board, color=Color.WHITE)

    knight_pos = algebraic_to_index('e4')
    board[knight_pos] = Piece(position=knight_pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)

    knight_movement = KnightMovement(board[knight_pos])
    potential_moves = knight_movement.get_potential_moves(board)

    expected_fen_list = 'c5','d6', 'f6','g5','g3','f2','d2','c3'
    expected_moves = {algebraic_to_index(fen) for fen in expected_fen_list}

    assert set(potential_moves) == expected_moves

def test_knight_cannot_capture_ally():
    board = generate_empty_board()
    place_king(board=board, color=Color.WHITE)

    knight_pos = algebraic_to_index('e4')
    ally_pos = algebraic_to_index('c5')
    board[knight_pos] = Piece(position=knight_pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)
    board[ally_pos] = Piece(position=ally_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    knight_movement = KnightMovement(board[knight_pos])
    potential_moves = knight_movement.get_potential_moves(board)

    assert ally_pos not in potential_moves

def test_knight_can_capture_enemy():
    board = generate_empty_board()
    place_king(board=board, color=Color.WHITE)

    knight_pos = algebraic_to_index('e4')
    enemy_pos = algebraic_to_index('c5')
    board[knight_pos] = Piece(position=knight_pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)
    board[enemy_pos] = Piece(position=enemy_pos, color=Color.BLACK, piece_type=PieceType.PAWN)

    knight_movement = KnightMovement(board[knight_pos])
    potential_moves = knight_movement.get_potential_moves(board)

    assert enemy_pos in potential_moves
