from chess_2.board.board_state import BoardState
from chess_2.utils.enums import Color
from chess_2.board.board_representation import generate_board_repr
from chess_2.utils.fen import algebraic_to_position, starting_fen


def get_player_input(color: Color) -> tuple[str, str]:
    """
    Prompts the user to enter a move.

    Returns:
        Tuple of (from_pos, to_pos) in algebraic notation, e.g., ('e2', 'e4').
    """
    print(f"{color.name.capitalize()}'s move:")
    move = input("Enter your move (e.g., e2 e4): ").strip().split()
    return move

    
def run_game():
    board_state = BoardState()
    # TO DO: Initialize from fixed starting position
    
    while True:
        print(generate_board_repr(board_state.piece_pos))
        move = get_player_input()
        # TO DO: process move from fen to Position
        # TO DO: incorporate validation move checks
        board_state.set_piece_location()
        board_state.switch_player_turn()

if __name__ == "__main__":
    run_game()
