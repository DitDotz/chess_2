import re
from chess_2.utils.types import Position
from chess_2.board.board_state import Piece
# from chess_2.piece_movement import xxx

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

class IllegalMove(Exception):
    """Exception raised for an illegal move."""
    def __init__(self, move: str, reason: str = ""):
        self.move = move
        self.reason = reason
        self.message = f"Illegal move: {move}. Reason: {reason if reason else 'Unknown reason'}."
        super().__init__(self.message)