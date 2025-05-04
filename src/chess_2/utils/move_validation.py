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

def can_castle_kingside(color: Color, piece_loc: dict[Position, Piece]) -> bool:

    from chess_2.piece_movement.move_generator import is_kingside_castling_path_under_attack

    king_pos = Position(7, 4) if color == Color.WHITE else Position(0, 4)
    rook_pos = Position(7, 7) if color == Color.WHITE else Position(0, 7)

    king = piece_loc.get(king_pos)
    rook = piece_loc.get(rook_pos)

    if not (king.piece_type==PieceType.KING and rook.piece_type==PieceType.ROOK):
        return False

    if king.has_moved or rook.has_moved:
        return False
        
    if not has_horizontal_path_clear_between(piece_loc, king_pos, rook_pos):
        return False

    if is_kingside_castling_path_under_attack(color=color, piece_loc=piece_loc):
        return False

    return True

def can_castle_queenside(color: Color, piece_loc: dict[Position, Piece]) -> bool:

    from chess_2.piece_movement.move_generator import is_queenside_castling_path_under_attack

    king_pos = Position(7, 4) if color == Color.WHITE else Position(0, 4)
    rook_pos = Position(7, 0) if color == Color.WHITE else Position(0, 0)

    king = piece_loc.get(king_pos)
    rook = piece_loc.get(rook_pos)

    if not (king.piece_type==PieceType.KING and rook.piece_type==PieceType.ROOK):
        return False

    if king.has_moved or rook.has_moved:
        return False

    if not has_horizontal_path_clear_between(piece_loc, king_pos, rook_pos):
        return False

    if is_queenside_castling_path_under_attack(color=color, piece_loc=piece_loc):
        return False

    return True
