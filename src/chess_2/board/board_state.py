
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position
from chess_2.utils.fen import algebraic_to_index

from chess_2.piece.piece import Piece
from chess_2.piece_movement.move_generator import is_king_in_checkmate

class BoardState:

    def __init__(self):
        self.piece_pos: dict[Position, Piece] = {}
        self.player_turn = Color.WHITE # default
        self.is_in_checkmate = False
        self.move_history:list[str] = []
        
    def switch_player_turn(self)->None:
        """
        Switches player turn
        """
        self.player_turn = Color.BLACK if self.player_turn == Color.WHITE else Color.WHITE
        return self.player_turn

    def set_piece_location(self, position: Position, piece: Piece) -> None:
        """
        Place a piece at the specified position on the board.

        Args:
            position (Position): The position where the piece should be placed.
            piece (Piece): The piece to place at the given position.

        Returns:
            dict[Position, Piece]: The updated board state.

        """
        self.piece_pos[position] = piece
        return self.piece_pos  # Returning the updated board state for testability

    def move_piece(self, piece: Piece, to_pos: Position) -> None:
        """
        Sets the piece at a given board position.

        Args:
            piece (Piece): The piece to move.
            to_pos (Position): The destination position of the piece.

        Returns:
            dict[Position, Piece]: The updated board state.
        """
        # Get the original position from the piece's current position
        original_pos = piece.position

        # Detect castling
        if piece.piece_type == PieceType.KING and abs(to_pos.col - original_pos.col) == 2:
            if to_pos == algebraic_to_index("g1"):  # White kingside
                self._castle_rook(original_pos, Position(7, 7), Position(7, 5))
            elif to_pos == algebraic_to_index("c1"):  # White queenside
                self._castle_rook(original_pos, Position(7, 0), Position(7, 3))
            elif to_pos == algebraic_to_index("g8"):  # Black kingside
                self._castle_rook(original_pos, Position(0, 7), Position(0, 5))
            elif to_pos == algebraic_to_index("c8"):  # Black queenside
                self._castle_rook(original_pos, Position(0, 0), Position(0, 3))

        # Move the piece by setting the original position to empty and placing the piece at the new position
        self.set_piece_location(position=original_pos, piece=Piece(position=original_pos, color=Color.NONE, piece_type=PieceType.EMPTY))

        # Update the piece's position to reflect the move

        piece.position = to_pos
        self.set_piece_location(position=to_pos, piece=piece)

        return self.piece_pos
    
    def _castle_rook(self, king_pos: Position, rook_from: Position, rook_to: Position) -> None:
        rook = self.piece_pos[rook_from]
        self.piece_pos[rook_from] = Piece(rook_from, Color.NONE, PieceType.EMPTY)

        rook.position = rook_to
        rook.has_moved = True
        self.piece_pos[rook_to] = rook


    def check_if_current_player_is_in_checkmate(self) -> bool:
        king = next(
        p for p in self.piece_pos.values()
        if p.color == self.player_turn and p.piece_type == PieceType.KING
    )

        if is_king_in_checkmate(king, self.piece_pos):
            self.is_in_checkmate=True



