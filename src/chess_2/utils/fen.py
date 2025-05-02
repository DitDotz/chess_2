
from chess_2.utils.enums import PieceType, Color
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
import re

# dictionary of fen as keys and PieceType as values
PIECE_TYPE_FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}

FILE_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
RANK_TO_INDEX = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


def parse_fen(fen: str) -> dict[Position, Piece]:
    """
    Process the FEN string and initialize the board with the specified piece positions.

    Args:
        fen (str): The FEN string representing the piece positions.

    Returns:
        dict[Position, Piece]: A dictionary representing the board with initialized piece positions.
    """

    piece_loc: dict[Position, Piece] = {}
    rows = fen.split('/')


    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                for _ in range(int(char)):  # Repeat for the number of empty squares
                    piece_loc[Position(row=row_idx, col=col_idx)] = Piece(position=Position(row=row_idx, col=col_idx), color=Color.NONE, piece_type=PieceType.EMPTY)
                    col_idx += 1  # Move to the next column

            else:
                color = Color.WHITE if char.isupper() else Color.BLACK
                piece_type = PIECE_TYPE_FEN_MAP[char.lower()]
                piece_loc[Position(row=row_idx, col=col_idx)] = Piece(position=Position(row=row_idx, col=col_idx), color=color, piece_type=piece_type)
                col_idx += 1

    return piece_loc

def parse_user_input(user_input: str) -> tuple[Piece, Position]:
    """
    Parse the user input for chess moves.
    
    Args:
        user_input (str): The user input move in the format '(pe4e5)'.
    
    Returns:
        Tuple[Piece, Position]: The parsed piece, destination position.
    """
    # Regex to match the pattern of a piece and two board squares (e.g., 'pe4e5')
    match = re.match(r"(?P<piece>[pnbrqkPNBRQK])(?P<from_square>[a-h][1-8])(?P<to_square>[a-h][1-8])", user_input)
    # the group('name') syntax refers to named capture groups in a regular expression. These are defined using the syntax (?P<name>...).

    if not match:
        raise ValueError("Invalid input format")

    piece_letter = match.group('piece')  # e.g., 'p' for pawn
    from_square = match.group('from_square')  # e.g., 'e4'
    to_square = match.group('to_square')  # e.g., 'e5'

    piece_type = PIECE_TYPE_FEN_MAP[piece_letter.lower()]  # maps 'p' -> PieceType.PAWN
    piece_color = Color.BLACK if piece_letter.islower() else Color.WHITE

    # Convert the squares to (row, col) format
    from_pos:Position = algebraic_to_index(from_square)
    to_pos:Position = algebraic_to_index(to_square)

    piece_moved = Piece(from_pos,piece_color, piece_type)
    
    return piece_moved, to_pos


def algebraic_to_index(fen_notation: str) -> Position:
    """
    Convert a board square from algebraic notation (e.g., 'e4') to (row, col).
    
    Args:
        fen_notation (str): The algebraic notation of the position (e.g., 'e4').
    
    Returns:
        Position: The row and column index of the position on the board.
    """
    file, rank = fen_notation[0], fen_notation[1]

    return (Position(row=RANK_TO_INDEX[rank], col=FILE_TO_INDEX[file]))