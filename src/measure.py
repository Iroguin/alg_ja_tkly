"""measure.py will contain code to analyze lage quantaties of games
Such as: average 2048 rate, average game length, average score, etc"""

import sys
import time
from algorithms.expectiminimax import get_best_move_expectiminimax
from algorithms.depth_one_move import depth_one_move
from game import Game2048


def run_single_game(algorithm="expectiminimax", depth=3):
    """
    Run a single game and return statistics
    Returns: dict with game statistics
    """
    game = Game2048()
    moves = 0
    won = False

    while not game.is_game_over():
        if algorithm == "expectiminimax":
            move = get_best_move_expectiminimax(game, depth)
        elif algorithm == "depth_one":
            move = depth_one_move(game)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        if game.make_move(move):
            moves += 1
            if game.is_won() and not won:
                won = True

    # Get final board statistics
    final_score = game.get_board_sum()
    max_tile = max(max(row) for row in game.board)

    return {
        'moves': moves,
        'score': final_score,
        'max_tile': max_tile,
        'won': won
    }


def analyze_games(num_games=100, algorithm="expectiminimax", depth=3):
    """
    Run multiple games and compile statistics
    """
    print(f"\nRunning {num_games} games with {algorithm} algorithm" +
          (f" (depth={depth})" if algorithm == "expectiminimax" else ""))
    print("-" * 50)

    results = []
    wins = 0
    tile_counts = {}
    start_time = time.time()

    # Run games
    for i in range(num_games):
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{num_games} games completed...")

        result = run_single_game(algorithm, depth)
        results.append(result)

        if result['won']:
            wins += 1

        # Track max tile distribution
        max_tile = result['max_tile']
        tile_counts[max_tile] = tile_counts.get(max_tile, 0) + 1

    elapsed_time = time.time() - start_time

    # Statistics
    total_moves = sum(r['moves'] for r in results)
    total_score = sum(r['score'] for r in results)
    avg_moves = total_moves / num_games
    avg_score = total_score / num_games
    win_rate = (wins / num_games) * 100

    # Find min and max scores
    min_score = min(r['score'] for r in results)
    max_score = max(r['score'] for r in results)
    min_moves = min(r['moves'] for r in results)
    max_moves = max(r['moves'] for r in results)

    # Display results
    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    print(f"Games played: {num_games}")
    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"Time per game: {elapsed_time / num_games:.2f} seconds")
    print(
        f"Game speed: {
            elapsed_time /
            num_games /
            avg_moves:.4f} seconds per move")
    print()
    print(f"Win rate (2048 reached): {win_rate:.1f}% ({wins}/{num_games})")
    print(f"Average moves per game: {avg_moves:.1f}")
    print(f"Average score: {avg_score:.1f}")
    print()
    print(f"Min score: {min_score} | Max score: {max_score}")
    print(f"Min moves: {min_moves} | Max moves: {max_moves}")
    print()
    print("Max tile distribution:")
    for tile in sorted(tile_counts.keys(), reverse=True):
        percentage = (tile_counts[tile] / num_games) * 100
        load_bar = '█' * int(percentage / 2)
        print(f"  {tile:5}: {
            tile_counts[tile]:3} games ({
            percentage:5.1f}%) {load_bar}")


if __name__ == "__main__":
    # Defaults
    NUM_GAMES = 100
    ALGORITHM = "expectiminimax"
    DEPTH = 3

    if len(sys.argv) > 1:
        NUM_GAMES = int(sys.argv[1])
    if len(sys.argv) > 2:
        ALGORITHM = sys.argv[2]
    if len(sys.argv) > 3:
        DEPTH = int(sys.argv[3])

    analyze_games(NUM_GAMES, ALGORITHM, DEPTH)
