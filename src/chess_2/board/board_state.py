
from chess_2.utils.enums import Color, PieceType
from chess_2.utils.types import Position

from chess_2.piece.piece import Piece

class BoardState:

    def __init__(self):
        self.piece_pos: dict[Position, Piece] = {}
        self.player_turn = Color.WHITE # default
        self.is_in_checkmate = False
        
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

        # TODO validate move is correct first

        # Move the piece by setting the original position to empty and placing the piece at the new position
        self.set_piece_location(position=original_pos, piece=Piece(position=original_pos, color=Color.NONE, piece_type=PieceType.EMPTY))

        # Update the piece's position to reflect the move

        piece.position = to_pos
        self.set_piece_location(position=to_pos, piece=piece)

        return self.piece_pos




