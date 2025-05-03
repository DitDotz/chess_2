from chess_2.utils.types import Position
from chess_2.piece.piece import Piece
from chess_2.utils.enums import Color, PieceType

def is_within_board(position: Position) -> bool:
    """
    Check whether a position is within the 8x8 chessboard.

    Args:
        position (Position): The (row, col) coordinates of the square.

    Returns:
        bool: True if the position is within the board boundaries, False otherwise.
    """

    row, col = position
    return 0 <= row < 8 and 0 <= col < 8


def is_square_empty(piece_loc: dict[Position, Piece], pos: Position) -> bool:
    """
    Check if the target position is empty

    Args:
        piece_loc (dict[Position, Piece]): The current state of the chessboard.
        pos (Position): The (row,col) of the target square
        color (Color): The color of the piece attempting to move.

    Returns:
        bool: True if the target position is empty, False otherwise.
    """
    piece = piece_loc.get(pos)
    return piece.piece_type == PieceType.EMPTY

def is_occupied_by_ally(piece_loc: dict[Position, Piece], pos: Position, color: Color) -> bool:
    """
    Check if the target position is not occupied by a piece of the same color.

    Args:
        piece_loc (dict[Position, Piece]): The current state of the chessboard.
        pos (Position): The (row,col) of the target square
        color (Color): The color of the piece attempting to move.

    Returns:
        bool: True if the target position is occupied by ally, False otherwise.
    """
    piece = piece_loc.get(pos)

    return piece.color == color and piece.piece_type != PieceType.EMPTY

def is_occupied_by_opposing(
    piece_loc: dict[Position, Piece], pos:Position, color: Color
) -> bool:
    """
    Check if the target position is occupied by a piece of the opposing color.

    Args:
        piece_loc (dict[Position, Piece]): The current state of the chessboard.
        pos (Position): The (row,col) of the target square
        color (Color): The color of the piece attempting to move.

    Returns:
        bool: True if the target position is occupied by an opposing piece, False otherwise.
    """
    piece = piece_loc.get(pos)

    return piece.color != color and piece.piece_type != PieceType.EMPTY and piece.color != Color.NONE


def has_moved(piece: Piece) -> bool:
        """
    Check if a piece has previously moved.

    Args:
        piece (Piece): The piece to check.

    Returns:
        bool: True if the piece has moved, False otherwise.
    """
        return piece.has_moved 


def has_horizontal_path_clear_between(
    piece_loc: dict[Position, Piece],
    start: Position,
    end: Position
) -> bool:
    """
    Check if all horizontal squares between start and end (excluding both) are empty.

    Args:
        piece_loc (dict[Position, Piece]): The current board.
        start (Position): One end of the line (usually rook or king).
        end (Position): The other end of the line.

    Returns:
        bool: True if all horizontal squares between 2 specified positions are empty, False otherwise.
    """
    if start.row == end.row:
        # Horizontal path
        row = start.row
        start_col, end_col = sorted([start.col, end.col])
        for col in range(start_col + 1, end_col):
            if piece_loc[Position(row, col)].piece_type != PieceType.EMPTY:
                return False
            
    else:
        raise ValueError("has_horizontal_path_clear_between only supports horizontal paths.")
    
    return True



# TODO
def is_square_under_attack(pos:Position, color:Color, piece_loc:dict[Position, Piece]):
    pass

# TODO
def is_kingside_castling_path_under_attack(color: Color, piece_loc: dict[Position, Piece]) -> bool:
    squares_to_check = {
        Color.WHITE: [Position(7, 5), Position(7, 6)],  # f1, g1
        Color.BLACK: [Position(0, 5), Position(0, 6)],  # f8, g8
    }[color]

    return any(
        is_square_under_attack(square, color, piece_loc) for square in squares_to_check
    )

# TODO
def is_queenside_castling_path_under_attack(color: Color, piece_loc: dict[Position, Piece]) -> bool:
    squares_to_check = {
        Color.WHITE: [Position(7, 3), Position(7, 2)],  # d1, c1
        Color.BLACK: [Position(0, 3), Position(0, 2)],  # d8, c8
    }[color]

    return any(
        is_square_under_attack(square, color, piece_loc) for square in squares_to_check
    )

# TODO
def is_king_in_check(king:Piece, piece_loc: dict[Position, Piece]) -> bool:
    """
    Check if the king of the given color is in check in the current position.

    Args:
        king: The king Piece
        piece_loc (dict[Position, Piece]): The current state of the chessboard.

    Returns:
        bool: True if the king is in check, False otherwise.
    """
    return is_square_under_attack(pos=king.position, color=king.color, piece_loc=piece_loc)

# TODO
def has_valid_moves(color:Color, piece_loc: dict[Position, Piece]):
    pass

#  TODO
def is_king_in_checkmate(king:Piece, piece_loc: dict[Position, Piece]) -> bool:
    """
    Check if the king of the given color is in check in the current position.

    Args:
        king: The king Piece
        piece_loc (dict[Position, Piece]): The current state of the chessboard.

    Returns:
        bool: True if the king is in checkmate, False otherwise.
    """
    return is_king_in_check(king, piece_loc) and not has_valid_moves(king.color, piece_loc)