import re

from chess_2.utils.enums import PieceType, Color
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position

# dictionary of fen as keys and PieceType as values
PIECE_TYPE_FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
    "n": PieceType.KNIGHT,
}

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

def parse_user_input(user_input: str, piece_color:Color) -> tuple[Piece, Position]:
    """
    Parse the user input for chess moves.

    Supports both standard notation like 'Pe2e4' and special castling notation 'O-O' or 'O-O-O'.

    Args:
        user_input (str): The move in string format.
        piece_color (Color): The current player's color

    Returns:
        Tuple[Piece, Position]: The parsed piece and the destination position.
    """
    user_input = user_input.strip()

    # Castling handling
    if user_input == "O-O":
        king_pos = algebraic_to_index("e1" if piece_color == Color.WHITE else "e8")
        dest_pos = algebraic_to_index("g1" if piece_color == Color.WHITE else "g8")
        return Piece(position=king_pos, color=piece_color, piece_type=PieceType.KING), dest_pos

    elif user_input == "O-O-O":
        king_pos = algebraic_to_index("e1" if piece_color == Color.WHITE else "e8")
        dest_pos = algebraic_to_index("c1" if piece_color == Color.WHITE else "c8")
        return Piece(position=king_pos, color=piece_color, piece_type=PieceType.KING), dest_pos

    # Regex to match piece and two positions (e.g., Pe2e4)
    match = re.match(r"(?P<piece>[pnbrqkPNBRQK])(?P<from_square>[a-h][1-8])(?P<to_square>[a-h][1-8])", user_input)
    if not match:
        return None

    piece_letter = match.group('piece')
    from_square = match.group('from_square')
    to_square = match.group('to_square')

    piece_type = PIECE_TYPE_FEN_MAP[piece_letter.lower()]
    parsed_color = Color.BLACK if piece_letter.islower() else Color.WHITE

    from_pos = algebraic_to_index(from_square)
    to_pos = algebraic_to_index(to_square)

    piece_moved = Piece(from_pos, parsed_color, piece_type)

    return piece_moved, to_pos

FILE_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
RANK_TO_INDEX = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

INDEX_TO_FILE = {v: k for k, v in FILE_TO_INDEX.items()}
INDEX_TO_RANK = {v: k for k, v in RANK_TO_INDEX.items()}

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

def index_to_algebraic(pos: Position) -> str:
    """
    Convert a (row, col) board position to algebraic notation (e.g., Position(4, 4) -> 'e4').

    Args:
        pos (Position): The board position to convert.

    Returns:
        str: The algebraic notation string.
    """
    file = INDEX_TO_FILE[pos.col]
    rank = INDEX_TO_RANK[pos.row]
    return f"{file}{rank}"