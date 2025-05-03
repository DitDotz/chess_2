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
    def get_valid_moves(
        self, piece_loc: dict[Position, Piece]
    ) -> list[Position]:
        """
        Get the valid moves for the piece on the given board.

        Args:
            piece_loc (dict[Position, Piece]): The current state of the chessboard.

        Returns:
            list[Position]: A list of valid moves for the piece.
        """
        pass
