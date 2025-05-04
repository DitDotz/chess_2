import copy

from chess_2.utils.types import Position
from chess_2.piece.piece import Piece
from chess_2.utils.enums import Color, PieceType

from chess_2.piece_movement.rook import RookMovement
from chess_2.piece_movement.bishop import BishopMovement
from chess_2.piece_movement.knight import KnightMovement
from chess_2.piece_movement.queen import QueenMovement
from chess_2.piece_movement.king import KingMovement
from chess_2.piece_movement.pawn import PawnMovement

def get_all_potential_moves(color: Color, piece_loc: dict[Position, Piece]) -> list[tuple[Piece, list[Position]]]:
    """
    Gets all potential moves for the given color on the current board.

    Args:
        color (Color): The color of the player to generate moves for.
        piece_loc (dict[Position, Piece]): The current board state.

    Returns:
        list of tuples: Each tuple is (piece, [list of potential target Positions])
    """
    potential_moves = []

    for piece in piece_loc.values():
        if piece.color != color or piece.piece_type == PieceType.EMPTY:
            continue

        match piece.piece_type:
            case PieceType.ROOK:
                movement = RookMovement(piece)
            case PieceType.BISHOP:
                movement = BishopMovement(piece)
            case PieceType.KNIGHT:
                movement = KnightMovement(piece)
            case PieceType.QUEEN:
                movement = QueenMovement(piece)
            case PieceType.KING:
                movement = KingMovement(piece)
            case PieceType.PAWN:
                movement = PawnMovement(piece)
            case _: # _ is a wildcard — it matches anything not explicitly matched earlier.
                continue 

        moves = movement.get_potential_moves(piece_loc)
        if moves:
            potential_moves.append((piece, moves))

    return potential_moves


def get_all_valid_moves(color: Color, piece_loc: dict[Position, Piece]) -> list[tuple[Piece, list[Position]]]:
    """
    Gets all valid moves for the given color on the current board.

    Args:
        color (Color): The color of the player to generate moves for.
        piece_loc (dict[Position, Piece]): The current board state.

    Returns:
        list of tuples: Each tuple is (piece, [list of valid target Positions])
    """
    valid_moves = []

    for piece in piece_loc.values():
        if piece.color != color or piece.piece_type == PieceType.EMPTY:
            continue

        match piece.piece_type:
            case PieceType.ROOK:
                movement = RookMovement(piece)
            case PieceType.BISHOP:
                movement = BishopMovement(piece)
            case PieceType.KNIGHT:
                movement = KnightMovement(piece)
            case PieceType.QUEEN:
                movement = QueenMovement(piece)
            case PieceType.KING:
                movement = KingMovement(piece)
            case PieceType.PAWN:
                movement = PawnMovement(piece)
            case _: # _ is a wildcard — it matches anything not explicitly matched earlier.
                continue 

        moves = movement.get_valid_moves(piece_loc)
        if moves:
            valid_moves.append((piece, moves))

    return valid_moves

def has_valid_moves(color: Color, piece_loc: dict[Position, Piece]) -> bool:
    """
    Checks if any piece of the given color has at least one potential move.

    Returns:
        bool: True if there is at least one potential move, False otherwise.
    """
    return bool(get_all_valid_moves(color, piece_loc)) # Python treats empty containers as False


def is_square_under_attack(pos:Position, curr_color:Color, piece_loc:dict[Position, Piece]):
    """
    Determines if a square is under attack by any piece of the opposing color.
    """
    opp_color = Color.BLACK if curr_color == Color.WHITE else Color.WHITE
    all_moves = get_all_potential_moves(opp_color, piece_loc)

    return any(pos in destinations for _, destinations in all_moves)
    # The underscore _ means: “I don’t care about the piece itself.”
    # Returns True if any one of those checks is True.

def is_kingside_castling_path_under_attack(color: Color, piece_loc: dict[Position, Piece]) -> bool:
    squares_to_check = {
        Color.WHITE: [Position(7, 5), Position(7, 6)],  # f1, g1
        Color.BLACK: [Position(0, 5), Position(0, 6)],  # f8, g8
    }[color]

    return any(
        is_square_under_attack(square, color, piece_loc) for square in squares_to_check
    )

def is_queenside_castling_path_under_attack(color: Color, piece_loc: dict[Position, Piece]) -> bool:
    squares_to_check = {
        Color.WHITE: [Position(7, 3), Position(7, 2)],  # d1, c1
        Color.BLACK: [Position(0, 3), Position(0, 2)],  # d8, c8
    }[color]

    return any(
        is_square_under_attack(square, color, piece_loc) for square in squares_to_check
    )

def is_king_in_check(king:Piece, piece_loc: dict[Position, Piece]) -> bool:
    """
    Check if the king of the given color is in check in the current position.

    Args:
        king: The king Piece
        piece_loc (dict[Position, Piece]): The current state of the chessboard.

    Returns:
        bool: True if the king is in check, False otherwise.
    """
    return is_square_under_attack(pos=king.position, curr_color=king.color, piece_loc=piece_loc)

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

def is_king_in_check_after_move(
    piece: Piece,
    to_pos: Position,
    piece_loc: dict[Position, Piece]
) -> bool:
    """
    Simulate the move and check if the current player's king is left in check.
    """
    # 1. Copy the board state
    temp_board = copy.deepcopy(piece_loc)

    # 2. Simulate the move
    temp_board[piece.position] = Piece(position=piece.position, color=Color.NONE, piece_type=PieceType.EMPTY)
    moved_piece = Piece(position=to_pos, color=piece.color, piece_type=piece.piece_type)
    temp_board[to_pos] = moved_piece

    # 3. Locate the king
    king = next(
        (p for p in temp_board.values() if p.color == piece.color and p.piece_type == PieceType.KING),
        None  # default
    )

    if not king:
        raise ValueError("King not found on the board for simulation.")

    # 4. Check if king is in check
    return is_king_in_check(king, temp_board)
