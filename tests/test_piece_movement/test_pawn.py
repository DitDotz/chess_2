import pytest
from chess_2.utils.enums import Color, PieceType
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece_movement.pawn import PawnMovement

from .. helpers import place_king

def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }

def test_white_pawn_forward_moves():
    board = generate_empty_board()
    pos = algebraic_to_index('d2')
    
    board[pos] = Piece(position=pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    movement = PawnMovement(board[pos])
    potential_moves = movement.get_potential_moves(board)

    assert algebraic_to_index('d3') in potential_moves
    assert algebraic_to_index('d4') in potential_moves  # 2-step from start row

def test_white_pawn_capture():
    board = generate_empty_board()

    pos = algebraic_to_index('d2')
    opp_piece_1_pos = algebraic_to_index('c3')
    opp_piece_2_pos = algebraic_to_index('e3')

    board[pos] = Piece(position=pos, color=Color.WHITE, piece_type=PieceType.PAWN)
    board[opp_piece_1_pos] = Piece(position=opp_piece_1_pos, color=Color.BLACK, piece_type=PieceType.KNIGHT)
    board[opp_piece_2_pos] = Piece(position=opp_piece_2_pos, color=Color.BLACK, piece_type=PieceType.KNIGHT)

    movement = PawnMovement(board[pos])
    potential_moves = movement.get_potential_moves(board)

    assert opp_piece_1_pos in potential_moves
    assert opp_piece_2_pos in potential_moves

def test_black_pawn_forward_moves():
    board = generate_empty_board()

    pos = algebraic_to_index('e7')
    board[pos] = Piece(position=pos, color=Color.BLACK, piece_type=PieceType.PAWN)

    movement = PawnMovement(board[pos])
    potential_moves = movement.get_potential_moves(board)

    assert algebraic_to_index('e6') in potential_moves
    assert algebraic_to_index('e5') in potential_moves  # 2-step from start row

def test_black_pawn_capture():
    board = generate_empty_board()

    pos = algebraic_to_index('e7')
    opp_piece_1_pos = algebraic_to_index('d6')
    opp_piece_2_pos = algebraic_to_index('f6')

    board[pos] = Piece(position=pos, color=Color.BLACK, piece_type=PieceType.PAWN)
    board[opp_piece_1_pos] = Piece(position=opp_piece_1_pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)
    board[opp_piece_2_pos] = Piece(position=opp_piece_2_pos, color=Color.WHITE, piece_type=PieceType.KNIGHT)

    movement = PawnMovement(board[pos])
    potential_moves = movement.get_potential_moves(board)

    assert opp_piece_1_pos in potential_moves
    assert opp_piece_2_pos in potential_moves
