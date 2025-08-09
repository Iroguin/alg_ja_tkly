"""evaluation.py contains functions for evaluating any arvitrary 2048 board state"""
import math
from game import Game2048


def evaluate_board(board):
    """
    Evaluates a 2048 board position using multiple heuristics.
    Rcieves: 4x4 board
    Returns: float score between 0 and 1 (higher is better)
    """

    def get_all_values():
        return [cell for row in board for cell in row if cell != 0]

    temp_game = Game2048()
    temp_game.set_board(board)
    all_values = get_all_values()

    if not temp_game.has_moves_available():
        return 0.0

    # 1. Empty cells score (more empty = better mobility)
    empty_cells = sum(row.count(0) for row in board)
    empty_score = empty_cells / 16.0

    # 2. Avoid small numbers between big ones
    def monotonicity():
        def mono_direction(values):
            increasing = decreasing = 0
            for i in range(len(values) - 1):
                if values[i] < values[i + 1]:
                    increasing += values[i + 1] - values[i]
                elif values[i] > values[i + 1]:
                    decreasing += values[i] - values[i + 1]
            return max(increasing, decreasing)

        row_mono = sum(mono_direction(row) for row in board)
        col_mono = sum(mono_direction([board[i][j]
                       for i in range(4)]) for j in range(4))

        max_possible = sum(all_values) * 2  # Rough normalization (fix)
        if max_possible == 0:
            return 0
        return min(1.0, (row_mono + col_mono) / max_possible)

    # 3. Corner weight biggest tile in corner is good
    def corner_weight():
        corners = [board[0][0], board[0][3], board[3][0], board[3][3]]
        max_val = max(all_values) if all_values else 0

        if max_val == 0:
            return 0

        corner_bonus = max(corners) / max_val
        return corner_bonus

    # 4. focus on merging adjacent equal tiles
    def mergeability():
        merge_potential = 0

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    continue

                # Check adjacent cells for merge possibility
                for di, dj in [
                        (0, 1), (1, 0)]:  # only right and bottom cell to avoid checking pairs twice
                    ni, nj = i + di, j + dj
                    if (0 <= ni < 4 and 0 <= nj < 4 and
                            board[ni][nj] == board[i][j]):
                        merge_potential += board[i][j]

        max_possible = sum(all_values)
        return merge_potential / max_possible if max_possible > 0 else 0

    # 5. Weighted sum based on tile values
    def weighted_sum():
        weight_matrix = [
            [15, 14, 13, 12],
            [11, 10, 9, 8],
            [7, 6, 5, 4],
            [3, 2, 1, 0]
        ]

        total = sum(board[i][j] * weight_matrix[i][j]
                    for i in range(4) for j in range(4))
        max_weight = 15  # Top-left corner weight
        board_sum = temp_game.get_board_sum()
        return total / (board_sum * max_weight) if board_sum > 0 else 0

    # 6. Prefer boards with larger maximum tiles (nykyinen implementaatio
    # huono mutta toimii)
    def max_tile_score():
        """Score based on the largest tile - always prefer bigger tiles"""
        max_tile = max(all_values) if all_values else 0
        if max_tile == 0:
            return 0
        return math.log2(max_tile) / 17.0 if max_tile > 0 else 0

    # Calculate all scores
    mono_score = monotonicity()
    corner_score = corner_weight()
    merge_score = mergeability()
    weighted_score = weighted_sum()
    max_tile = max_tile_score()

    weights = {
        'empty': 0.20,
        'monotonic': 0.20,
        'corner': 0.20,
        'merge': 0.15,
        'weighted': 0.15,
        'max_tile': 0.10
    }

    total_score = (
        weights['empty'] * empty_score +
        weights['monotonic'] * mono_score +
        weights['corner'] * corner_score +
        weights['merge'] * merge_score +
        weights['weighted'] * weighted_score +
        weights['max_tile'] * max_tile
    )

    return min(1.0, max(0.0, total_score))


# Test Functionality
if __name__ == "__main__":
    test_board = [
        [2, 4, 8, 16],
        [0, 2, 4, 8],
        [0, 0, 2, 4],
        [0, 0, 0, 2]
    ]

    score = evaluate_board(test_board)
    print(f"Board score: {score:.3f}")
