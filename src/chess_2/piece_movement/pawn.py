from typing import Dict, List
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.enums import Color, PieceType
from chess_2.piece_movement.piece_move import PieceMovement
from chess_2.utils.move_validation import (
    is_within_board,
    is_square_empty,
    is_occupied_by_opposing,
)

class PawnMovement(PieceMovement):
    """
    Defines movement rules for the pawn piece.
    """

    def get_potential_moves(self, piece_loc: Dict[Position, Piece]) -> List[Position]:
        direction = -1 if self.piece.color == Color.WHITE else 1
        start_row = 6 if self.piece.color == Color.WHITE else 1
        row, col = self.piece.position
        potential_moves = []

        # 1-step forward
        one_forward = Position(row + direction, col)
        if is_within_board(one_forward) and is_square_empty(piece_loc, one_forward):
            potential_moves.append(one_forward)

            # 2-step forward from starting row
            two_forward = Position(row + 2 * direction, col)
            if row == start_row and is_square_empty(piece_loc, two_forward):
                potential_moves.append(two_forward)

        # Diagonal captures
        for dc in [-1, 1]:  # left and right
            diag_pos = Position(row + direction, col + dc)
            if is_within_board(diag_pos) and is_occupied_by_opposing(piece_loc, diag_pos, self.piece.color):
                potential_moves.append(diag_pos)

        return potential_moves
