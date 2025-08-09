"""Tests for evaluation.py"""

import pytest
from evaluation import evaluate_board


class TestEvaluateBoard:
    """Test the main evaluate_board function"""

    def test_empty_board(self):
        """Test evaluation of empty board"""
        board = [[0] * 4 for i in range(4)]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        # Empty board should have high empty score
        assert score >= 0.2

    def test_full_board_no_merges(self):
        """Test evaluation of full board with no possible merges"""
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        # Full board with no merges SHOULD have low score (evaluation function
        # bad)
        assert score < 0.3

    def test_monotonic_board(self):
        """Test board with good monotonicity"""
        board = [
            [128, 64, 32, 16],
            [64, 32, 16, 8],
            [32, 16, 8, 4],
            [16, 8, 2, 2]  # needs an option to move
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        assert score > 0.4

    def test_corner_weight(self):
        """Test board with max tile in corner"""
        board = [
            [2048, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        # High empty cells and max tile in corner
        assert score > 0.5

    def test_mergeable_tiles(self):
        """Test board with many mergeable tiles"""
        board = [
            [2, 2, 4, 4],
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [8, 8, 16, 16]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        # Many merge opportunities should increase score
        assert score > 0.3

    def test_score_bounds(self):
        """Test that scores stay within 0-1 bounds"""
        test_boards = [
            [[0] * 4 for i in range(4)],  # Empty
            [[2048] * 4 for i in range(4)],  # All max
            [[2, 4, 8, 16], [32, 64, 128, 256], [
                512, 1024, 2048, 4096], [8192, 16384, 32768, 65536]],
            [[1] * 4 for i in range(4)]  # All ones (if possible)
        ]

        for board in test_boards:
            score = evaluate_board(board)
            assert 0 <= score <= 1

    def test_weighted_position(self):
        """Test weighted sum heuristic"""
        # Board with high value in top-left (highest weight)
        board1 = [
            [1024, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        # Board with same value in bottom-right (lowest weight)
        board2 = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1024]
        ]

        score1 = evaluate_board(board1)
        score2 = evaluate_board(board2)

        # First board should score higher due to weighted position
        assert score1 > score2


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_single_tile(self):
        """Test board with single tile"""
        board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        assert score > 0.5  # High empty space

    def test_alternating_pattern(self):
        """Test checkerboard pattern"""
        board = [
            [2, 0, 2, 0],
            [0, 2, 0, 2],
            [2, 0, 2, 0],
            [0, 2, 0, 2]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1

    def test_snake_pattern(self):
        """Test snake-like pattern (good for weighted sum)"""
        board = [
            [512, 256, 128, 64],
            [1024, 2048, 4096, 32],
            [8192, 16384, 32768, 16],
            [65536, 131072, 8, 4]
        ]
        score = evaluate_board(board)
        assert 0 <= score <= 1

    def test_all_same_value(self):
        """Test board with all same non-zero values"""
        board = [[8] * 4 for i in range(4)]
        score = evaluate_board(board)
        assert 0 <= score <= 1
        # Should have high merge potential
        assert score >= 0.2


class TestHeuristicComponents:
    """Test individual heuristic calculations"""

    def test_empty_cells_heuristic(self):
        """Test empty cells scoring"""
        # 75% empty
        board1 = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        score1 = evaluate_board(board1)

        # 25% empty
        board2 = [
            [2, 4, 8, 0],
            [16, 32, 64, 0],
            [128, 256, 512, 0],
            [1024, 2048, 4096, 0]
        ]
        score2 = evaluate_board(board2)

        # More empty cells should generally mean higher score
        assert score1 > score2

    def test_monotonicity_directions(self):
        """Test different monotonic patterns"""
        # Perfect decreasing monotonicity
        board_decreasing = [
            [16, 8, 4, 2],
            [16, 8, 4, 2],
            [16, 8, 4, 2],
            [16, 8, 4, 2]
        ]

        # Random pattern
        board_random = [
            [2, 16, 4, 8],
            [8, 2, 16, 4],
            [4, 8, 2, 16],
            [16, 4, 8, 2]
        ]

        score_mono = evaluate_board(board_decreasing)
        score_random = evaluate_board(board_random)

        # Monotonic board should score higher
        assert score_mono > score_random

    def test_corner_positions(self):
        """Test max tile in different corners"""
        max_val = 2048
        corners = [
            [[max_val, 0, 0, 0], [0, 0, 0, 0], [
                0, 0, 0, 0], [0, 0, 0, 0]],  # Top-left
            [[0, 0, 0, max_val], [0, 0, 0, 0], [
                0, 0, 0, 0], [0, 0, 0, 0]],  # Top-right
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                [max_val, 0, 0, 0]],  # Bottom-left
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                [0, 0, 0, max_val]],  # Bottom-right
        ]

        center_board = [[0, 0, 0, 0], [0, max_val, 0, 0],
                        [0, 0, 0, 0], [0, 0, 0, 0]]
        corner_scores = [evaluate_board(board) for board in corners]
        center_score = evaluate_board(center_board)

        # All corner positions should score similarly and better than center
        for corner_score in corner_scores:
            assert corner_score > center_score
