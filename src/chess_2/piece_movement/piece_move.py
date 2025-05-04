from chess_2.utils.types import Position
from chess_2.piece.piece import Piece
from abc import ABC, abstractmethod

class PieceMovement(ABC):
    """
    Abstract class for defining movement rules of chess pieces.

    Attributes:
        piece (Piece): The piece for which movement rules are defined.
    """

    def __init__(self, piece: Piece):
        """Initialize the PieceMovement object."""
        self.piece = piece

    @abstractmethod
    def get_potential_moves(self, piece_loc: dict[Position, Piece]) -> list[Position]:
        """
        Get all potential (theoretical) moves for the piece without considering king safety.

        Args:
            piece_loc (dict[Position, Piece]): The current board state.

        Returns:
            List[Position]: Potential moves for the piece.
        """
        pass

    def get_valid_moves(self, piece_loc: dict[Position, Piece]) -> list[Position]:
        """
        Get legal moves for the piece (excluding those that leave king in check).

        Args:
            piece_loc (dict[Position, Piece]): The current board state.

        Returns:
            List[Position]: Valid legal moves.
        """
        from chess_2.piece_movement.move_generator import is_king_in_check_after_move

        valid_moves = []
        for move in self.get_potential_moves(piece_loc):
            if not is_king_in_check_after_move(self.piece, move, piece_loc):
                valid_moves.append(move)

        return valid_moves
