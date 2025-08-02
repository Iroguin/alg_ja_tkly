"""play_game.py contains code to execute playing the game using various algorithms"""

from algorithms.expectiminimax import get_best_move_expectiminimax
from algorithms.depth_one_move import depth_one_move
from game import Game2048

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"


def play_game_ai(algorithm="expectiminimax", depth=3):
    """
    Play a game using the specified AI algorithm
    Args:
        algorithm: str - "depth_one" or "expectiminimax"
        depth: int - search depth for expectiminimax (ignored for depth_one)
    """
    game = Game2048()
    moves = 0

    while not game.is_game_over():
        game.print_board()
        print(f"Move {moves}")

        # Get move based on algorithm
        if algorithm == "expectiminimax":
            move = get_best_move_expectiminimax(game, depth)
        elif algorithm == "depth_one":
            move = depth_one_move(game)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        print(f"AI chooses: {move}")

        # Play move
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
    print(f"Played with {algorithm} algorithm" +
          (f" (depth={depth})" if algorithm == "expectiminimax" else ""))
    print(f"Game over after {moves} moves!")


if __name__ == "__main__":
    import sys

    # Default algorithm
    PLAY_ALGORTYHM = "expectiminimax"
    PLAY_DEPTH = 3

    # Command line arguments
    if len(sys.argv) > 1:
        PLAY_ALGORTYHM = sys.argv[1]
    if len(sys.argv) > 2:
        PLAY_DEPTH = int(sys.argv[2])

    print(f"Playing with {PLAY_ALGORTYHM} algorithm" +
          (f" (depth={PLAY_DEPTH})" if PLAY_ALGORTYHM == "expectiminimax" else ""))
    play_game_ai(PLAY_ALGORTYHM, PLAY_DEPTH)
