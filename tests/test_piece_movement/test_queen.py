import pytest
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece_movement.queen import QueenMovement

def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }

def test_queen_potential_moves_on_clear_board():
    board = generate_empty_board()
    queen_pos = algebraic_to_index('e4')
    board[queen_pos] = Piece(position=queen_pos, color=Color.WHITE, piece_type=PieceType.QUEEN)

    queen_movement = QueenMovement(board[queen_pos])
    potential_moves = queen_movement.get_potential_moves(board)

    expected_moves = set()

    for i in range(8):
        if i != 4:
            expected_moves.add(Position(i, 4))  # vertical
            expected_moves.add(Position(4, i))  # horizontal

    for i in range(1, 8):
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            row = 4 + dx * i
            col = 4 + dy * i
            if 0 <= row < 8 and 0 <= col < 8:
                expected_moves.add(Position(row, col))

    assert set(potential_moves) == expected_moves

def test_queen_blocked_by_ally():
    board = generate_empty_board()
    queen_pos = algebraic_to_index('e4')
    ally_pos = algebraic_to_index('g4')
    board[queen_pos] = Piece(position=queen_pos, color=Color.WHITE, piece_type=PieceType.QUEEN)
    board[ally_pos] = Piece(position=ally_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    queen_movement = QueenMovement(board[queen_pos])
    potential_moves = queen_movement.get_potential_moves(board)

    assert ally_pos not in potential_moves
    assert algebraic_to_index('h4') not in potential_moves

def test_queen_can_capture_enemy():
    board = generate_empty_board()
    queen_pos = algebraic_to_index('e4')
    enemy_pos = algebraic_to_index('g4')
    board[queen_pos] = Piece(position=queen_pos, color=Color.WHITE, piece_type=PieceType.QUEEN)
    board[enemy_pos] = Piece(position=enemy_pos, color=Color.BLACK, piece_type=PieceType.PAWN)

    queen_movement = QueenMovement(board[queen_pos])
    potential_moves = queen_movement.get_potential_moves(board)

    assert enemy_pos in potential_moves
    assert algebraic_to_index('h4') not in potential_moves
