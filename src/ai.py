from evaluation import evaluate_board
from game import Game2048

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

def depth_one_move(game):
    """
    Algorithm that tries each move and picks the best one.
    Doesnt use expectiminimax.
    Args: game: Game2048 instance
    Returns: str: Best direction to move
    """
    directions = [UP, DOWN, LEFT, RIGHT]
    best_score = 0
    best_move = None
    
    for direction in directions:
        # Save current board state
        original_board = game.get_board_copy()
        
        # Try the move
        if game.make_move(direction):
            score = evaluate_board(game.board)
            
            # Update best if better
            if score > best_score:
                best_score = score
                best_move = direction
        
        game.set_board(original_board)
    return best_move if best_move else directions[0]  # Fallback to UP


def play_game_ai():
    """Play a game using the one-move-depth AI"""
    game = Game2048()
    moves = 0
    
    while not game.is_game_over():
        game.print_board()
        print(f"Move {moves}")
        
        # Get AI move
        move = depth_one_move(game)
        print(f"AI chooses: {move}")
        
        # Make the move
        if game.make_move(move):
            moves += 1
        else:
            print("No valid moves available!")
            break
        
        if game.is_won():
            game.print_board()
            print(f"Won in {moves} moves!")
            return
    
    game.print_board()
    print(f"Game over after {moves} moves!")


if __name__ == "__main__":
    play_game_ai()

