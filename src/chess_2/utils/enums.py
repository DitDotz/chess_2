from enum import Enum

class Color(Enum):
    """
    Enumeration representing the colors of chess pieces.

    Attributes:
        WHITE (int): The value representing the white color.
        BLACK (int): The value representing the black color.
        NONE (int): The value representing no color (for empty squares).
    """

    WHITE = 0
    BLACK = 1
    NONE = -1

class PieceType(Enum):
    """
    Enumeration representing the types of chess pieces.

    Attributes:
        EMPTY (str): Represents an empty square on the chessboard.
        PAWN (str): Represents a pawn piece.
        ROOK (str): Represents a rook piece.
        BISHOP (str): Represents a bishop piece.
        QUEEN (str): Represents a queen piece.
        KNIGHT (str): Represents a knight piece.
        KING (str): Represents a king piece.
    """

    EMPTY = "empty"
    PAWN = "pawn"
    ROOK = "rook"
    BISHOP = "bishop"
    QUEEN = "queen"
    KNIGHT = "knight"
    KING = "king"
