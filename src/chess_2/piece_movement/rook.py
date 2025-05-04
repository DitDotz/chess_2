from chess_2.piece_movement.piece_move import PieceMovement
from chess_2.piece.piece import Piece
from chess_2.utils.types import Position
from chess_2.utils.move_validation import (
    is_within_board,
    is_square_empty,
    is_occupied_by_ally,
)

class RookMovement(PieceMovement):
    """
    Defines movement rules for the rook piece.
    """

    def get_potential_moves(
        self, piece_loc: dict[Position, Piece]
    ) -> list[Position]:
        """
        Get the valid moves for the rook on the given board.

        Args:
            piece_loc (dict[Position, Piece]): The current state of the chessboard.

        Returns:
            list[Position]: A list of valid moves for the rook.
        """
        # Define directions for rook movement: up, down, left, right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        potential_moves = []
        row, col  = self.piece.position

        for dx, dy in directions:
            step = 1
            while True:
                new_row = row + dx * step
                new_col = col + dy * step
                next_pos = Position(new_row, new_col)

                if not is_within_board(next_pos):
                    break

                if is_square_empty(piece_loc, next_pos):
                    potential_moves.append(next_pos)

                elif is_occupied_by_ally(piece_loc, next_pos, self.piece.color):
                    break
                
                else:
                    potential_moves.append(next_pos)
                    break

                step += 1

        return potential_moves
