
from chess_2.utils.enums import PieceType


# dictionary of fen as keys and PieceType as values
FEN_MAP: dict[str, PieceType] = {}

PIECE_STR_REPR: dict[PieceType, tuple[str, str]] = {}

Position = tuple[int, int]

