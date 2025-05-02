from chess_2.board.board_state import BoardState
from chess_2.utils.enums import Color
from chess_2.board.board_representation import generate_board_repr
from chess_2.utils.fen import START_FEN, parse_fen, parse_user_input
from chess_2.utils.input_validation import is_valid_notation, InvalidNotation, does_piece_exist_at_pos,PieceDoesNotExist, is_legal_move, IllegalMove



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
        print(generate_board_repr(board_state.piece_pos))

        move = get_player_input(board_state)

        try:

            if is_valid_notation(move)==False:
                raise InvalidNotation(move)
            
            piece_to_move, final_pos = parse_user_input(move)

            if does_piece_exist_at_pos(board_state.piece_pos, piece_to_move)==False:
                raise PieceDoesNotExist(move)
            
            if is_legal_move(board_state, piece_to_move, final_pos)==False:
                raise IllegalMove(move)
        
        except (InvalidNotation, PieceDoesNotExist, IllegalMove) as e:

            print(e.message)
            continue

        # if no exceptions, move the piece
        board_state.move_piece(piece_to_move, final_pos)
        board_state.switch_player_turn()

        if board_state.is_in_checkmate()==True:
            print(f"{board_state.player_turn} lost")
            break
            
if __name__ == "__main__":
    run_game()
