import re
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position

from chess_2.board.board_state import BoardState
from chess_2.utils.fen import algebraic_to_index, index_to_algebraic
from chess_2.board.board_state import Piece


def is_valid_notation(move:str)->bool:
    """ Validate if the move is in the correct format (e.g., pe2e4, Qd1d2) """
    return bool(re.match(r"^[pnbrqkPNBRQK][a-h][1-8][a-h][1-8]$", move))

class InvalidNotation(Exception):
    """Exception raised for invalid move notation."""
    def __init__(self, move: str):
        self.move = move
        self.message = f"Invalid move notation: {move}. Please use the correct format (e.g., pe2e4)."
        super().__init__(self.message)

def does_piece_exist_at_pos(piece_pos:dict[Position, Piece], piece_to_move):
    """
    Check if a piece exists at the given position.
    Args:
        piece_pos (dict(Position, Piece)): The current board state mapping positions to pieces.
        piece_to_move (str): Piece to be moved.
    Returns:
        bool: True if a piece exists at the position, False otherwise.
    """

    return piece_pos.get(piece_to_move.position) == piece_to_move

class PieceDoesNotExist(Exception):
    """Exception raised for invalid move notation."""
    def __init__(self, position: Position):
        self.position = position
        self.message = f"Piece specified not found at position {position}. Please select a valid piece."
        super().__init__(self.message)

def is_legal_move(piece_pos:dict[Position, Piece], piece_to_move:Piece, final_pos:Position):
    """
    Check if a move is legal based on game rules (e.g., piece movement, check condition).
    Args:
        board_state (BoardState): The current board state.
        piece_to_move (Piece): The piece being moved.
        final_pos (str): The target position to move the piece to (e.g., 'e4').
    Returns:
        bool: True if the move is legal, False otherwise.
    """
    #TODO if move is outside of board
    #TODO if move results in own king in check or checkmate
    #TODO if move is not a valid piecetype move
    pass

class IllegalMove(Exception):
    """Exception raised for an illegal move."""
    def __init__(self, move: str, reason: str = ""):
        self.move = move
        self.reason = reason
        self.message = f"Illegal move: {move}. Reason: {reason if reason else 'Unknown reason'}."
        super().__init__(self.message)