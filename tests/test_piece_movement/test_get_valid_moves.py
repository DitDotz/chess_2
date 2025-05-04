
from chess_2.utils.types import Position
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.fen import algebraic_to_index
from chess_2.piece.piece import Piece
from chess_2.piece_movement.king import KingMovement
from chess_2.piece_movement.rook import RookMovement
from chess_2.piece_movement.bishop import BishopMovement
from chess_2.piece_movement.queen import QueenMovement
from chess_2.piece_movement.pawn import PawnMovement
from chess_2.piece_movement.knight import KnightMovement

from tests.helpers import generate_empty_board, place_king

def test_rook_valid_moves_excludes_pins():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")

    # Rook is on e2, black queen is on e8 — rook is pinned vertically
    rook_pos = algebraic_to_index("e2")
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    queen_pos = algebraic_to_index("e8")
    board[queen_pos] = Piece(position=queen_pos, color=Color.BLACK, piece_type=PieceType.QUEEN)

    # The rook can move in many directions by potential logic, but not legally due to the pin
    movement = RookMovement(board[rook_pos])
    valid_moves = movement.get_valid_moves(board)

    expected_moves = {algebraic_to_index(f"e{rank}") for rank in range(3, 9)}

    assert set(valid_moves) == expected_moves


def test_pawn_valid_moves_excludes_pins():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")

    white_pawn_pos = algebraic_to_index("e2")
    board[white_pawn_pos] = Piece(position=white_pawn_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    # Add two black pawns to the diagonal (but shouldn't be capturable due to pin)
    board[algebraic_to_index("d3")] = Piece(position=algebraic_to_index("d3"), color=Color.BLACK, piece_type=PieceType.PAWN)
    board[algebraic_to_index("f3")] = Piece(position=algebraic_to_index("f3"), color=Color.BLACK, piece_type=PieceType.PAWN)

    # Queen pinning the white pawn
    board[algebraic_to_index("e8")] = Piece(position=algebraic_to_index("e8"), color=Color.BLACK, piece_type=PieceType.QUEEN)

    movement = PawnMovement(board[white_pawn_pos])
    valid_moves = movement.get_valid_moves(board)

    # Only e3 (and e4 if clear) should be legal — diagonals expose the king
    expected_moves = {algebraic_to_index("e3"), algebraic_to_index("e4")}

    assert set(valid_moves) == expected_moves


def test_bishop_diagonal_pin_capture_possible():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")

    white_pawn_pos = algebraic_to_index("d2")
    board[white_pawn_pos] = Piece(position=white_pawn_pos, color=Color.WHITE, piece_type=PieceType.PAWN)


    # Queen pinning diagonally the white pawn
    board[algebraic_to_index("c3")] = Piece(position=algebraic_to_index("c3"), color=Color.BLACK, piece_type=PieceType.QUEEN)

    movement = PawnMovement(board[white_pawn_pos])
    valid_moves = movement.get_valid_moves(board)

    # Only e3 (and e4 if clear) should be legal — diagonals expose the king
    expected_moves = {algebraic_to_index("c3")}

    assert set(valid_moves) == expected_moves

def test_bishop_diagonal_pin():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")

    white_pawn_pos = algebraic_to_index("d2")
    board[white_pawn_pos] = Piece(position=white_pawn_pos, color=Color.WHITE, piece_type=PieceType.PAWN)

    # Queen pinning diagonally the white pawn
    board[algebraic_to_index("b4")] = Piece(position=algebraic_to_index("b4"), color=Color.BLACK, piece_type=PieceType.QUEEN)

    movement = PawnMovement(board[white_pawn_pos])
    valid_moves = movement.get_valid_moves(board)

    expected_moves = set()

    assert set(valid_moves) == expected_moves


def test_king_cannot_walk_into_check():
    board = generate_empty_board()
    place_king(board, Color.WHITE, pos="e1")

    board[algebraic_to_index("f8")] = Piece(position=algebraic_to_index("f8"), color=Color.BLACK, piece_type=PieceType.ROOK)
    board[algebraic_to_index("d8")] = Piece(position=algebraic_to_index("d8"), color=Color.BLACK, piece_type=PieceType.ROOK)

    movement = KingMovement(board[algebraic_to_index("e1")])
    valid_moves = movement.get_valid_moves(board)

    expected_moves = {algebraic_to_index("e2")}

    assert set(valid_moves) == expected_moves
