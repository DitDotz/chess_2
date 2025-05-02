import pytest
from chess_2.piece.piece import Piece
from chess_2.utils.enums import PieceType, Color
from chess_2.utils.types import Position
from chess_2.board.board_state import BoardState  # assuming the BoardState class is in the boardstate module

def test_set_piece_location():
    board = BoardState()
    piece = Piece(position=Position(0, 0), color=Color.WHITE, piece_type=PieceType.ROOK)
    
    # Place the piece at position (0, 0)
    board_state = board.set_piece_location(Position(0, 0), piece)
    
    # Assert that the piece is at the correct location
    assert board_state[Position(0, 0)] == piece

def test_move_piece():
    board = BoardState()
    piece = Piece(position=Position(0, 0), color=Color.WHITE, piece_type=PieceType.ROOK)
    
    # Place the piece at position (0, 0)
    board.set_piece_location(Position(0, 0), piece)
    
    # Move the piece to position (1, 1)
    board_state = board.move_piece(piece, Position(1, 1))
    
    # Assert that the piece has been moved to the new position
    assert board_state[Position(1, 1)] == piece
    assert board_state[Position(0, 0)] == Piece(position=Position(0, 0), color=Color.NONE, piece_type=PieceType.EMPTY)  # The original position is now empty
