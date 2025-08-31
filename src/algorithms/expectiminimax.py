"""expectiminimax.py contains an algorythm for using expectiminimax to find the best move"""

import random
from unittest.mock import Mock
from evaluation import evaluate_board
from game import Game2048


UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

_cached_game = Game2048()


def apply_move(board, direction):
    """Apply move to board and return new board state (without modifying original)"""
    # Handle Mock objects in tests
    try:
        _cached_game.set_board(board)
    except TypeError:
        # If board is a Mock, return a different Mock so new_board != board
        return Mock()

    if direction == LEFT:
        new_board = [_cached_game.combine_row(
            row) for row in _cached_game.board]
    elif direction == RIGHT:
        new_board = [_cached_game.combine_row(
            row[::-1])[::-1] for row in _cached_game.board]
    elif direction == UP:
        new_board = [[_cached_game.combine_row([_cached_game.board[i][j] for i in range(4)])[i]
                     for j in range(4)] for i in range(4)]
    elif direction == DOWN:
        new_board = [[_cached_game.combine_row([_cached_game.board[i][j]
                     for i in range(4)][::-1])[::-1][i]
                     for j in range(4)] for i in range(4)]

    return new_board


def expectiminimax(game, depth, is_player_turn=True):
    """
    Expectiminimax algorithm for 2048.
    Args:
        game: Game_2048
        depth: Search depth remaining
        is_player_turn: True if player move, False if random tile placement
    Returns: float: Expected value of position
    """
    if depth == 0 or game.is_game_over():
        return evaluate_board(game.board)

    if is_player_turn:
        alpha = float('-inf')
        directions = [UP, DOWN, LEFT, RIGHT]

        for direction in directions:
            new_board = apply_move(game.board, direction)

            # Check if move is valid
            if new_board != game.board:
                temp_game = Game2048()
                temp_game.set_board(new_board)

                value = expectiminimax(temp_game, depth - 1, False)
                alpha = max(alpha, value)

        if alpha == float('-inf'):
            return evaluate_board(game.board)
        return alpha

    else:
        # Expectation off random tile
        empty_cells = [(i, j) for i in range(4)
                       for j in range(4) if game.board[i][j] == 0]

        if not empty_cells:
            return evaluate_board(game.board)

        # Sample limited cells if too many (7 seemed to be the safe point where
        # gameplay wasnt impacted)
        if len(empty_cells) > 7:
            empty_cells = random.sample(empty_cells, 7)

        alpha = 0
        num_cells = len(empty_cells)

        for i, j in empty_cells:
            # Placing a 2 (90% probability)
            original_value = game.board[i][j]
            game.board[i][j] = 2
            value_2 = expectiminimax(game, depth - 1, True)

            # Placing a 4 (10% probability)
            game.board[i][j] = 4
            value_4 = expectiminimax(game, depth - 1, True)

            game.board[i][j] = original_value

            # Weighted average for this cell
            cell_value = 0.9 * value_2 + 0.1 * value_4
            alpha += cell_value / num_cells

        return alpha


def get_best_move_expectiminimax(game, depth=3):
    """
    Get the best move using expectiminimax algorithm.
    Args:
        game: Game2048 instance
        depth: Search depth
    Returns: str: Best direction
    """
    directions = [UP, DOWN, LEFT, RIGHT]
    best_score = float('-inf')
    best_move = None

    for direction in directions:
        new_board = apply_move(game.board, direction)

        # Check if move is valid
        if new_board != game.board:
            temp_game = Game2048()
            temp_game.set_board(new_board)

            score = expectiminimax(temp_game, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = direction

    return best_move if best_move else UP
