from typing import Dict, List
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.enums import Color
from chess_2.piece_movement.piece_move import PieceMovement
from chess_2.utils.move_validation import (
    is_within_board,
    is_occupied_by_ally,
)
class KnightMovement(PieceMovement):
    """
    Defines movement rules for the knight piece.
    """

    def get_potential_moves(self, piece_loc: Dict[Position, Piece]) -> List[Position]:
        directions = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        row, col = self.piece.position
        potential_moves = []

        for dx, dy in directions:
            new_pos = Position(row + dx, col + dy)

            if not is_within_board(new_pos):
                continue

            if not is_occupied_by_ally(piece_loc, new_pos, self.piece.color):
                potential_moves.append(new_pos)

        return potential_moves
