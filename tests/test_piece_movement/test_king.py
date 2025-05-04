import pytest
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece_movement.king import KingMovement

def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }

def test_king_potential_moves_on_clear_board():
    board = generate_empty_board()
    king_pos = algebraic_to_index('e4')
    board[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)

    king_movement = KingMovement(board[king_pos])
    potential_moves = king_movement.get_potential_moves(board)

    expected_fen_list = 'd4','f4', 'd5','e5','f5','d3','e3','f3'
    expected_moves = {algebraic_to_index(fen) for fen in expected_fen_list}

    assert set(potential_moves) == expected_moves

def test_king_cannot_move_into_ally():
    board = generate_empty_board()
    king_pos = algebraic_to_index('e4')
    ally_pos = algebraic_to_index('f3')
    board[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[ally_pos] = Piece(position=ally_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    king_movement = KingMovement(board[king_pos])
    potential_moves = king_movement.get_potential_moves(board)

    assert ally_pos not in potential_moves

def test_king_can_capture_enemy():
    board = generate_empty_board()
    king_pos = algebraic_to_index('e4')
    enemy_pos = algebraic_to_index('f3')
    board[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[enemy_pos] = Piece(position=enemy_pos, color=Color.BLACK, piece_type=PieceType.PAWN)

    king_movement = KingMovement(board[king_pos])
    potential_moves = king_movement.get_potential_moves(board)

    assert enemy_pos in potential_moves
