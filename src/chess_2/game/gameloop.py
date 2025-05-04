from chess_2.board.board_state import BoardState
from chess_2.board.board_representation import generate_board_repr

from chess_2.piece.piece import Piece

from chess_2.utils.enums import Color, PieceType
from chess_2.utils.fen import START_FEN, parse_fen, parse_user_input
from chess_2.utils.types import Position
from chess_2.utils.input_validation import (
    is_valid_notation,
    does_piece_exist_at_pos,
    InvalidNotation,
    PieceDoesNotExist,
    IllegalMove
)


def get_player_input(board_state:BoardState) -> str:
    """
    Prompts the user to enter a move.

    Returns:
        Tuple of (from_pos, to_pos) in algebraic notation, e.g., ('e2', 'e4').
    """
    print(f"{board_state.player_turn}'s move:")
    move = input(f"Enter your move (e.g., be2e4): ")
    return move

def run_game():
    board_state = BoardState()
    # Initialize from fixed starting position
    board_state.piece_pos = parse_fen(START_FEN)
    
    while True:

        move = get_player_input(board_state)

        try:
            result = parse_user_input(move)
            
            if result is None:
                raise InvalidNotation(move)

            piece_to_move, final_pos = result

            if not does_piece_exist_at_pos(board_state.piece_pos, piece_to_move):
                raise PieceDoesNotExist(piece_to_move.position)

            from chess_2.piece_movement.move_generator import get_all_valid_moves
            all_valid = get_all_valid_moves(piece_to_move.color, board_state.piece_pos)

            for piece, moves in all_valid:
                if piece.position == piece_to_move.position and final_pos in moves:
                    break
            else:
                raise IllegalMove(move, reason="Move is not legal for this piece")

        except (InvalidNotation, PieceDoesNotExist, IllegalMove) as e:
            print(e.message)
            continue


        board_state.move_piece(piece_to_move, final_pos)
        board_state.move_history.append(move)
        board_state.switch_player_turn()
            
if __name__ == "__main__":
    run_game()
