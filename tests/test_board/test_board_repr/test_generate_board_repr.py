from dataclasses import dataclass

from chess_2.board.board_representation import generate_board_repr

from chess_2.board.board_representation import get_piece_repr
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position

# Mock Piece class for testing
@dataclass
class Piece:
    position: Position 
    color: Color
    piece_type: PieceType
    has_moved:bool = False
    en_passantable:bool = False  # only valid for pawns. only True for pawn that moved 2 spaces, and returns to False after 1 turn by opposite color

    @property
    def repr(self) -> str:
        """
        Get the string representation of the piece.
        """
        return get_piece_repr(self.color, self.piece_type)

# Test: Empty board
def test_empty_board():
    board = {}
    for x in range(8):
        for y in range(8):
            board[(x, y)] = Piece(color=Color.NONE, piece_type = PieceType.EMPTY, position = (x,y))

    # Generate expected output
    expected = "  a   b   c   d   e   f   g   h\n"
    for x in range(8):
        expected += "|---" * 8 + f"| {8 - x}\n"
        expected += "|   " * 8 + "|\n"
    expected += "|---" * 8 + "|\n"
    expected += "  a   b   c   d   e   f   g   h\n"

    assert generate_board_repr(board) == expected

# Test: Board with some pieces
def test_board_with_pieces():

    board = {}
    board[(0, 0)] = Piece(position=(0, 0), color=Color.WHITE, piece_type=PieceType.ROOK)
    board[(7, 7)] = Piece(position=(7, 7), color=Color.BLACK, piece_type=PieceType.KING)

    # Fill the rest with empty pieces
    for x in range(8):
        for y in range(8):
            if (x, y) not in board:
                board[(x, y)] = Piece(position=(x, y), color=Color.NONE, piece_type=PieceType.EMPTY)

    board_repr = generate_board_repr(board)

    # Check specific lines
    lines = board_repr.split("\n")
    top_row = lines[2]  # This is rank 8
    bottom_row = lines[16]  # This is rank 1

    assert get_piece_repr(Color.WHITE, PieceType.ROOK) in top_row
    assert get_piece_repr(Color.BLACK, PieceType.KING) in bottom_row

