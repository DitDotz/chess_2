import pytest
from chess_2.utils.fen import parse_fen, START_FEN
from chess_2.utils.enums import PieceType, Color
from chess_2.utils.types import Position

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

