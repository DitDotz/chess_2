import pytest
from chess_2.utils.fen import parse_fen, START_FEN, parse_user_input, algebraic_to_index
from chess_2.utils.enums import PieceType, Color
from chess_2.utils.types import Position
from chess_2.piece.piece import Piece

# Test Case 1: Test a piece_loc with a full set of pieces and empty squares in the middle.

def test_parse_fen_full():
    fen = START_FEN
    piece_loc = parse_fen(fen)

    # Check pieces for row 0
    assert piece_loc[Position(row=0, col=0)].piece_type == PieceType.ROOK
    assert piece_loc[Position(row=0, col=1)].piece_type == PieceType.KNIGHT
    assert piece_loc[Position(row=0, col=7)].piece_type == PieceType.ROOK

    # Check for empty squares in row 2
    for col in range(8):
        assert piece_loc[Position(row=2, col=col)].piece_type == PieceType.EMPTY


# Test 2: FEN with a row of empty squares
def test_parse_fen_empty_row():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/"
    board = parse_fen(fen)

    # Check that row 2 is filled with empty pieces
    for col in range(8):
        assert board[Position(row=2, col=col)].piece_type == PieceType.EMPTY

# Test 3: All empty squares in a row
def test_parse_fen_all_empty():
    fen = "8/8/8/8/8/8/8/8"
    board = parse_fen(fen)

    # Check all rows for empty pieces
    for row in range(8):
        for col in range(8):
            assert board[Position(row=row, col=col)].piece_type == PieceType.EMPTY

# Test 4: FEN with pawns only
def test_parse_fen_pawn_row():
    fen = "pppppppp/8/8/8/8/8/8/pppppppp"
    board = parse_fen(fen)

    # Check the first and last rows for pawns
    for col in range(8):
        assert board[Position(row=0, col=col)].piece_type == PieceType.PAWN
        assert board[Position(row=7, col=col)].piece_type == PieceType.PAWN

# Test 5: Edge case for one empty square (digit value '1')
def test_parse_fen_one_empty_square():
    fen = "r1bqkbnr"
    board = parse_fen(fen)

    # Check that there is 1 empty square at the second column (index 1)
    assert board[Position(row=0, col=1)].piece_type == PieceType.EMPTY
    assert board[Position(row=0, col=0)].piece_type == PieceType.ROOK


def test_parse_user_input_valid_white_pawn():
    user_input = "Pe2e4"
    piece, to_pos = parse_user_input(user_input)

    expected_piece = Piece(position=Position(row=6, col=4), color=Color.WHITE, piece_type=PieceType.PAWN)
    expected_to_pos = Position(row=4, col=4)

    assert piece == expected_piece
    assert to_pos == expected_to_pos

def test_parse_user_input_black_knight():
    user_input = "ng8f6"
    piece, to_pos = parse_user_input(user_input)

    expected_piece = Piece(position=Position(row=0, col=6), color=Color.BLACK, piece_type=PieceType.KNIGHT)
    expected_to_pos = Position(row=2, col=5)

    assert piece == expected_piece
    assert to_pos == expected_to_pos

def test_parse_user_input_invalid_format():
    with pytest.raises(ValueError):
        parse_user_input("e2e4")  # Missing parentheses and piece type

def test_parse_user_input_invalid_piece():
    with pytest.raises(ValueError):
        parse_user_input("xe2e4")  # 'x' is not a valid piece type

def test_algebraic_to_index():
    # Test conversion of various positions
    test_cases = [
        ("e4", Position(row=4, col=4)),  # Should map 'e4' -> (4, 4)
        ("a1", Position(row=7, col=0)),  # Should map 'a1' -> (7, 0)
        ("h8", Position(row=0, col=7)),  # Should map 'h8' -> (0, 7)
        ("d5", Position(row=3, col=3)),  # Should map 'd5' -> (3, 3)
        ("g3", Position(row=5, col=6)),  # Should map 'g3' -> (5, 6)
    ]

    for fen_notation, expected in test_cases:
        result = algebraic_to_index(fen_notation)
        assert result == expected, f"Expected {expected} for {fen_notation}, but got {result}"
