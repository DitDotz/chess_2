from chess_2.board.board_state import BoardState
from chess_2.utils.enums import Color
from chess_2.board.board_representation import generate_board_repr
from chess_2.utils.fen import START_FEN, parse_fen, parse_user_input


def get_player_input(color: Color) -> tuple[str, str]:
    """
    Prompts the user to enter a move.

    Returns:
        Tuple of (from_pos, to_pos) in algebraic notation, e.g., ('e2', 'e4').
    """
    print(f"{color.name.capitalize()}'s move:")
    move = input("Enter your move (e.g., be2e4): ").strip().split()
    return move

    
def run_game():
    board_state = BoardState()
    # Initialize from fixed starting position
    board_state.piece_pos = parse_fen(START_FEN)
    
    while True:
        print(generate_board_repr(board_state.piece_pos))
        move = get_player_input()

        piece_to_move, final_pos = parse_user_input(move)
        
        # TO DO: incorporate validation move checks
        board_state.move_piece(piece_to_move, final_pos)
        board_state.switch_player_turn()

if __name__ == "__main__":
    run_game()
