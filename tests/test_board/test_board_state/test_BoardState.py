import pytest
from chess_2.piece.piece import Piece
from chess_2.utils.enums import PieceType, Color
from chess_2.utils.types import Position
from chess_2.board.board_state import BoardState  # assuming the BoardState class is in the boardstate module
from chess_2.utils.fen import algebraic_to_index
from tests.helpers import generate_empty_board

def test_switch_player_turn():
    board = BoardState()
    
    # Initially assume it's White's turn
    board.player_turn = Color.WHITE
    result = board.switch_player_turn()
    assert result == Color.BLACK
    assert board.player_turn == Color.BLACK

    # Switch back to White
    result = board.switch_player_turn()
    assert result == Color.WHITE
    assert board.player_turn == Color.WHITE

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

def test_white_kingside_castling_execution():
    board = BoardState()
    board.piece_pos.clear()

    king_pos = algebraic_to_index("e1")
    rook_pos = algebraic_to_index("h1")
    board.piece_pos[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board.piece_pos[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    board.move_piece(board.piece_pos[king_pos], algebraic_to_index("g1"))

    assert board.piece_pos[algebraic_to_index("g1")].piece_type == PieceType.KING
    assert board.piece_pos[algebraic_to_index("f1")].piece_type == PieceType.ROOK


def test_white_queenside_castling_execution():
    board = BoardState()
    board.piece_pos.clear()

    king_pos = algebraic_to_index("e1")
    rook_pos = algebraic_to_index("a1")
    board.piece_pos[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)
    board.piece_pos[rook_pos] = Piece(position=rook_pos, color=Color.WHITE, piece_type=PieceType.ROOK)

    board.move_piece(board.piece_pos[king_pos], algebraic_to_index("c1"))

    assert board.piece_pos[algebraic_to_index("c1")].piece_type == PieceType.KING
    assert board.piece_pos[algebraic_to_index("d1")].piece_type == PieceType.ROOK


def test_black_kingside_castling_execution():
    board = BoardState()
    board.piece_pos.clear()

    king_pos = algebraic_to_index("e8")
    rook_pos = algebraic_to_index("h8")
    board.piece_pos[king_pos] = Piece(position=king_pos, color=Color.BLACK, piece_type=PieceType.KING)
    board.piece_pos[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    board.move_piece(board.piece_pos[king_pos], algebraic_to_index("g8"))

    assert board.piece_pos[algebraic_to_index("g8")].piece_type == PieceType.KING
    assert board.piece_pos[algebraic_to_index("f8")].piece_type == PieceType.ROOK


def test_black_queenside_castling_execution():
    board = BoardState()
    board.piece_pos.clear()

    king_pos = algebraic_to_index("e8")
    rook_pos = algebraic_to_index("a8")
    board.piece_pos[king_pos] = Piece(position=king_pos, color=Color.BLACK, piece_type=PieceType.KING)
    board.piece_pos[rook_pos] = Piece(position=rook_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    board.move_piece(board.piece_pos[king_pos], algebraic_to_index("c8"))

    assert board.piece_pos[algebraic_to_index("c8")].piece_type == PieceType.KING
    assert board.piece_pos[algebraic_to_index("d8")].piece_type == PieceType.ROOK

def test_check_if_white_is_in_checkmate():
    board_state = BoardState()
    board_state.piece_pos = generate_empty_board()
    board_state.player_turn = Color.WHITE

    # Place white king at a1
    king_pos = algebraic_to_index("a1")
    board_state.piece_pos[king_pos] = Piece(position=king_pos, color=Color.WHITE, piece_type=PieceType.KING)

    # Black rooks create a checkmate
    rook_1_pos = algebraic_to_index("a8")
    rook_2_pos = algebraic_to_index("b8")
    board_state.piece_pos[rook_1_pos] = Piece(position=rook_1_pos, color=Color.BLACK, piece_type=PieceType.ROOK)
    board_state.piece_pos[rook_2_pos] = Piece(position=rook_2_pos, color=Color.BLACK, piece_type=PieceType.ROOK)

    board_state.check_if_current_player_is_in_checkmate()

    assert board_state.is_in_checkmate is True
