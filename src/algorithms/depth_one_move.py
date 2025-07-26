"""depth_one_move.py contains an algorythm mostly for testing purposes"""

from evaluation import evaluate_board

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
