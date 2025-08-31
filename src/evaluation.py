"""evaluation.py contains functions for evaluating any arbitrary 2048 board state"""
import math


def evaluate_board(board):
    """
    Evaluates a 2048 board position using multiple heuristics
    Receives: 4x4 board
    Returns: float score between 0 and 1 (higher is better)
    """

    # Quick check for game over
    if not has_moves_available(board):
        return 0.0

    empty_cells = 0
    max_val = 0
    board_sum = 0
    merge_potential = 0

    # Single pass for basics
    for i in range(4):
        for j in range(4):
            cell = board[i][j]
            if cell == 0:
                empty_cells += 1
            else:
                board_sum += cell
                max_val = max(max_val, cell)

                # Check adjacent cells for merge possibility
                if j < 3 and board[i][j + 1] == cell:
                    merge_potential += cell
                if i < 3 and board[i + 1][j] == cell:
                    merge_potential += cell

    # 1. Empty cells score (more empty = better mobility)
    empty_score = empty_cells / 16.0

    # 2. Avoid small numbers between big ones (Monotonicity)
    mono_score = calculate_monotonicity(board, board_sum)

    # 3. Corner weight biggest tile in corner is good
    corners = [board[0][0], board[0][3], board[3][0], board[3][3]]
    corner_score = max(corners) / max_val if max_val > 0 else 0

    # 4. focus on merging adjacent equal tiles
    merge_score = merge_potential / board_sum if board_sum > 0 else 0

    # 5. Weighted sum based on tile values
    weighted_score = get_best_weighted_score(board, board_sum)

    # 6. Prefer boards with larger maximum tiles
    max_tile_score = math.log2(max_val) / 17.0 if max_val > 0 else 0

    # Calculate all scores + weights
    total_score = (
        0.20 * empty_score +
        0.20 * mono_score +
        0.20 * corner_score +
        0.15 * merge_score +
        0.15 * weighted_score +
        0.10 * max_tile_score
    )

    return min(1.0, max(0.0, total_score))


def has_moves_available(board):
    """Fast check if any moves are available"""
    # Check for empty cells
    for row in board:
        if 0 in row:
            return True

    # Check for adjacent equal tiles
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j +
                                       1] or board[j][i] == board[j + 1][i]:
                return True
    return False


def get_best_weighted_score(board, board_sum):
    """Calculate weighted score for best orientation so thats its less arbitrary"""
    orientations = [
        [[15, 14, 13, 12], [11, 10, 9, 8], [7, 6, 5, 4], [3, 2, 1, 0]],  # top-left
        [[12, 13, 14, 15], [8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]],  # top-right
        [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8],
            [15, 14, 13, 12]],  # bottom-left
        [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],
            [12, 13, 14, 15]]   # bottom-right
    ]
    max_weighted = 0
    for weights in orientations:
        weighted_sum = (
            board[0][0] * weights[0][0] + board[0][1] * weights[0][1] +
            board[0][2] * weights[0][2] + board[0][3] * weights[0][3] +
            board[1][0] * weights[1][0] + board[1][1] * weights[1][1] +
            board[1][2] * weights[1][2] + board[1][3] * weights[1][3] +
            board[2][0] * weights[2][0] + board[2][1] * weights[2][1] +
            board[2][2] * weights[2][2] + board[2][3] * weights[2][3] +
            board[3][0] * weights[3][0] + board[3][1] * weights[3][1] +
            board[3][2] * weights[3][2] + board[3][3] * weights[3][3]
        )
        if weighted_sum > max_weighted:
            max_weighted = weighted_sum
    return max_weighted / (board_sum * 15) if board_sum > 0 else 0


def calculate_monotonicity(board, board_sum):
    """Monotonicity calculator"""
    if board_sum == 0:
        return 0
    total_mono = 0

    # Check rows
    for row in board:
        inc = dec = 0
        for i in range(3):
            if row[i] != 0 and row[i + 1] != 0:
                if row[i] < row[i + 1]:
                    inc += row[i + 1] - row[i]
                elif row[i] > row[i + 1]:
                    dec += row[i] - row[i + 1]
        total_mono += max(inc, dec)

    # Check columns
    for j in range(4):
        inc = dec = 0
        for i in range(3):
            if board[i][j] != 0 and board[i + 1][j] != 0:
                if board[i][j] < board[i + 1][j]:
                    inc += board[i + 1][j] - board[i][j]
                elif board[i][j] > board[i + 1][j]:
                    dec += board[i][j] - board[i + 1][j]
        total_mono += max(inc, dec)

    # Normalize
    max_possible = board_sum * 2
    return min(1.0, total_mono / max_possible) if max_possible > 0 else 0


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
