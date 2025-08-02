"""expectiminimax.py contains an algorythm for using expectiminimax to find the best move"""

from evaluation import evaluate_board
from game import Game2048

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"


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
            original_board = game.get_board_copy()

            if game.make_move(direction):
                # Move was valid, dont add random tile
                # Remove the random tile added by make_move
                game.board = [row[:] for row in game.board]

                # move manually to avoid random tile
                temp_game = Game2048()
                temp_game.set_board(original_board)

                if direction == LEFT:
                    temp_game.board = [
                        temp_game.combine_row(row) for row in temp_game.board]
                elif direction == RIGHT:
                    temp_game.board = [temp_game.combine_row(
                        row[::-1])[::-1] for row in temp_game.board]
                elif direction == UP:
                    temp_game.board = [[temp_game.combine_row([temp_game.board[i][j] for i in range(
                        4)])[
                        i] for j in range(4)] for i in range(4)]
                elif direction == DOWN:
                    temp_game.board = [[temp_game.combine_row([temp_game.board[i][j] for i in range(
                        4)][::-1])[::-1][i] for j in range(4)] for i in range(4)]

                value = expectiminimax(temp_game, depth - 1, False)
                alpha = max(alpha, value)

            game.set_board(original_board)

        return alpha if alpha != float('-inf') else evaluate_board(game.board)

    else:
        # Expectation off random tile
        empty_cells = [(i, j) for i in range(4)
                       for j in range(4) if game.board[i][j] == 0]

        if not empty_cells:
            return evaluate_board(game.board)

        alpha = 0
        num_cells = len(empty_cells)

        for i, j in empty_cells:
            # Placing a 2 (90% probability)
            original_board = game.get_board_copy()
            game.board[i][j] = 2
            value_2 = expectiminimax(game, depth - 1, True)
            game.set_board(original_board)

            # Placing a 4 (10% probability)
            game.board[i][j] = 4
            value_4 = expectiminimax(game, depth - 1, True)
            game.set_board(original_board)

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
        original_board = game.get_board_copy()

        # Simulate move without random tile
        temp_game = Game2048()
        temp_game.set_board(original_board)

        move_valid = False
        if direction == LEFT:
            new_board = [temp_game.combine_row(row) for row in temp_game.board]
            move_valid = new_board != temp_game.board
            temp_game.board = new_board
        elif direction == RIGHT:
            new_board = [temp_game.combine_row(
                row[::-1])[::-1] for row in temp_game.board]
            move_valid = new_board != temp_game.board
            temp_game.board = new_board
        elif direction == UP:
            new_board = [[temp_game.combine_row([temp_game.board[i][j] for i in range(4)])[
                i] for j in range(4)] for i in range(4)]
            move_valid = new_board != temp_game.board
            temp_game.board = new_board
        elif direction == DOWN:
            new_board = [[temp_game.combine_row([temp_game.board[i][j] for i in range(
                4)][::-1])[::-1][i] for j in range(4)] for i in range(4)]
            move_valid = new_board != temp_game.board
            temp_game.board = new_board

        if move_valid:
            score = expectiminimax(temp_game, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = direction

    return best_move if best_move else UP
