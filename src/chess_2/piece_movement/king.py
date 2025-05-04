from typing import Dict, List
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.enums import Color
from chess_2.piece_movement.piece_move import PieceMovement
from chess_2.utils.move_validation import (
    is_within_board,
    is_occupied_by_ally,

)
from chess_2.utils.move_validation import can_castle_kingside, can_castle_queenside

class KingMovement(PieceMovement):
    """
    Defines movement rules for the king piece.
    """
    def get_potential_moves(self, piece_loc: Dict[Position, Piece]) -> List[Position]:
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # vertical/horizontal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonal
        ]
        potential_moves = []
        row, col = self.piece.position

        for dx, dy in directions:
            new_row = row + dx
            new_col = col + dy
            next_pos = Position(new_row, new_col)

            if not is_within_board(next_pos):
                continue

            if not is_occupied_by_ally(piece_loc, next_pos, self.piece.color):
                potential_moves.append(next_pos)

        # Castling checks
        if can_castle_kingside(self.piece.color, piece_loc):
            potential_moves.append(Position(row, 6))  # g1 or g8

        if can_castle_queenside(self.piece.color, piece_loc):
            potential_moves.append(Position(row, 2))  # c1 or c8

        return potential_moves