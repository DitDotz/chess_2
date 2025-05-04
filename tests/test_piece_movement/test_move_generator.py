import pytest
from chess_2.utils.fen import algebraic_to_index
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index, parse_fen, START_FEN
from chess_2.piece.piece import Piece
from chess_2.piece_movement.move_generator import (
    get_all_potential_moves,
    get_all_valid_moves, 
    has_valid_moves,
    is_square_under_attack,
    is_kingside_castling_path_under_attack,
    is_queenside_castling_path_under_attack,
    is_king_in_check,
    is_king_in_checkmate,
    is_king_in_check_after_move
)

from ..helpers import place_king

# Helper to generate a full empty board
def generate_empty_board() -> dict[Position, Piece]:
    return {
        Position(row, col): Piece(position=Position(row, col), color=Color.NONE, piece_type=PieceType.EMPTY)
        for row in range(8) for col in range(8)
    }

def test_get_all_potential_moves_returns_rook_moves():
    board = generate_empty_board()

    rook_pos = algebraic_to_index('e4')
    rook = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    board[rook_pos] = rook

    all_moves = get_all_potential_moves(Color.WHITE, board)

    assert any(piece == rook and moves for piece, moves in all_moves)

def test_is_square_under_attack_by_knight():
    board = generate_empty_board()
    knight_pos = algebraic_to_index('b6')
    board[knight_pos] = Piece(position=knight_pos, color=Color.BLACK, piece_type=PieceType.KNIGHT)

    # Knight can attack (0, 2)
    assert is_square_under_attack(algebraic_to_index('c8'), Color.WHITE, board)

def test_is_square_not_under_attack_when_no_enemies():
    board = generate_empty_board()
    assert is_square_under_attack(Position(3, 3), Color.WHITE, board) is False

def test_white_kingside_castling_path_under_attack_f_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('f8')
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    assert is_kingside_castling_path_under_attack(Color.WHITE, board) is True

def test_white_kingside_castling_path_under_attack_g_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('g8')
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    assert is_kingside_castling_path_under_attack(Color.WHITE, board) is True

def test_white_queenside_castling_path_under_attack_d_file():
    board = generate_empty_board()
    # Place a black rook attacking d1 (0,3) — part of queenside castling path
    rook_pos = algebraic_to_index('d8')
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    assert is_queenside_castling_path_under_attack(Color.WHITE, board) is True

def test_white_queenside_castling_path_under_attack_c_file():
    board = generate_empty_board()
    # Place a black rook attacking d1 (0,3) — part of queenside castling path
    rook_pos = algebraic_to_index('c8')
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    assert is_queenside_castling_path_under_attack(Color.WHITE, board) is True

def test_black_kingside_castling_path_under_attack_f_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('f1')  # attacking f8
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    assert is_kingside_castling_path_under_attack(Color.BLACK, board) is True

def test_black_kingside_castling_path_under_attack_g_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('g1')  # attacking g8
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    assert is_kingside_castling_path_under_attack(Color.BLACK, board) is True

def test_black_queenside_castling_path_under_attack_d_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('d1')  # attacking d8
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    assert is_queenside_castling_path_under_attack(Color.BLACK, board) is True

def test_black_queenside_castling_path_under_attack_c_file():
    board = generate_empty_board()
    rook_pos = algebraic_to_index('c1')  # attacking c8
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    assert is_queenside_castling_path_under_attack(Color.BLACK, board) is True

def test_white_queenside_castling_path_not_under_attack_on_empty_board():
    board = generate_empty_board()
    assert is_queenside_castling_path_under_attack(Color.WHITE, board) is False

def test_black_queenside_castling_path_not_under_attack_on_empty_board():
    board = generate_empty_board()
    assert is_queenside_castling_path_under_attack(Color.BLACK, board) is False

def test_white_kingside_castling_path_not_under_attack_on_empty_board():
    board = generate_empty_board()
    assert is_kingside_castling_path_under_attack(Color.WHITE, board) is False

def test_black_kingside_castling_path_not_under_attack_on_empty_board():
    board = generate_empty_board()
    assert is_kingside_castling_path_under_attack(Color.BLACK, board) is False

def test_is_white_king_in_check_true():
    board = generate_empty_board()
    king_pos = algebraic_to_index('e1')
    king = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[king_pos] = king

    rook_pos = algebraic_to_index('e8')
    board[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    assert is_king_in_check(king, board)

def test_is_black_king_in_check_true():
    board = generate_empty_board()
    king_pos = algebraic_to_index('e8')
    king = Piece(position=king_pos, color=Color.BLACK, piece_type=PieceType.KING)
    board[king_pos] = king

    rook_pos = algebraic_to_index('e1')
    board[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    assert is_king_in_check(king, board) == True

def test_is_white_king_in_checkmate_true():
    board = generate_empty_board()
    king_pos = algebraic_to_index('a1')
    king = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[king_pos] = king

    # Surround with rooks
    rook_1_pos = algebraic_to_index('a8')
    rook_2_pos = algebraic_to_index('b8')
    board[rook_1_pos] = Piece(position=rook_1_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    board[rook_2_pos] = Piece(position=rook_2_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    assert is_king_in_checkmate(king, board) == True

def test_rook_move_exposes_king_to_check():
    board = generate_empty_board()

    king_pos = algebraic_to_index("e1")
    white_king = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[king_pos] = white_king

    rook_pos = algebraic_to_index("e2")
    white_rook = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)
    board[rook_pos] = white_rook

    black_rook_pos = algebraic_to_index("e8")
    black_rook = Piece(position=black_rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    board[black_rook_pos] = black_rook

    to_pos = algebraic_to_index("f2")
    assert is_king_in_check_after_move(white_rook, to_pos, board) is True

def test_king_moves_into_check_from_rook():
    board = generate_empty_board()

    king_pos = algebraic_to_index("d1")
    white_king = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[king_pos] = white_king

    black_rook_pos = algebraic_to_index("e8")
    black_rook = Piece(position=black_rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    board[black_rook_pos] = black_rook

    to_pos = algebraic_to_index("e1")
    assert is_king_in_check_after_move(white_king, to_pos, board) is True

def test_king_moves_into_safe_square():
    board = generate_empty_board()

    king_pos = algebraic_to_index("d1")
    white_king = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board[king_pos] = white_king

    black_rook_pos = algebraic_to_index("h8")
    black_rook = Piece(position=black_rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    board[black_rook_pos] = black_rook

    to_pos = algebraic_to_index("c1")
    assert is_king_in_check_after_move(white_king, to_pos, board) is False


def test_get_all_valid_moves_from_starting_fen():
    piece_pos = parse_fen(START_FEN)
    all_moves = get_all_valid_moves(Color.WHITE, piece_pos)

    # Flatten the result to (from_pos, to_pos) pairs for easy checking
    actual_moves = set()
    for piece, destinations in all_moves:
        for dest in destinations:
            actual_moves.add((piece.position, dest))

    # Define all expected moves in (from_pos, to_pos) format
    expected_moves = {
        # Pawns (a2–h2 to a3–h3 and a4–h4)
        (algebraic_to_index(f"{file}2"), algebraic_to_index(f"{file}3")) for file in "abcdefgh"
    }.union({
        (algebraic_to_index(f"{file}2"), algebraic_to_index(f"{file}4")) for file in "abcdefgh"
    }).union({
        # Knights
        (algebraic_to_index("b1"), algebraic_to_index("a3")),
        (algebraic_to_index("b1"), algebraic_to_index("c3")),
        (algebraic_to_index("g1"), algebraic_to_index("f3")),
        (algebraic_to_index("g1"), algebraic_to_index("h3")),
    })

    assert actual_moves == expected_moves

def test_has_valid_moves():

    piece_loc = parse_fen(START_FEN)

    assert has_valid_moves(color=Color.WHITE, piece_loc = piece_loc)==True