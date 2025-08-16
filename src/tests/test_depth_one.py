"""Tests for depth_one_move algorithm"""

from unittest.mock import Mock, patch
from algorithms.depth_one_move import depth_one_move


class TestDepthOneMove:
    """Test depth_one_move algorithm"""

    def test_chooses_best_scoring_move(self):
        """Test that depth_one_move picks the move with highest evaluation score"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[0] * 4 for i in range(4)]
        mock_game.make_move.return_value = True
        mock_game.set_board.return_value = None

        with patch('algorithms.depth_one_move.evaluate_board') as mock_eval:
            # Make UP return highest score
            mock_eval.side_effect = [10, 20, 5, 15]  # UP, DOWN, LEFT, RIGHT

            result = depth_one_move(mock_game)

            assert result == "down"
            assert mock_game.make_move.call_count == 4
            assert mock_game.set_board.call_count == 4

    def test_handles_no_valid_moves(self):
        """Test fallback when no moves are valid"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[0] * 4 for i in range(4)]
        mock_game.make_move.return_value = False  # No valid moves
        mock_game.set_board.return_value = None

        result = depth_one_move(mock_game)

        assert result == "up"  # Fallback

    def test_restores_board_state(self):
        """Test that original board state is restored after each move test"""
        mock_game = Mock()
        original_board = [[2, 4, 8, 16]] * 4  # 4x4 board
        mock_game.get_board_copy.return_value = original_board
        mock_game.make_move.return_value = True
        mock_game.board = original_board  # Set board for evaluate_board

        with patch('algorithms.depth_one_move.evaluate_board', return_value=10):
            depth_one_move(mock_game)

        # Verify set_board called with original state
        expected_calls = [((original_board,),)] * 4
        assert mock_game.set_board.call_args_list == expected_calls

    def test_only_considers_valid_moves(self):
        """Test that only valid moves are considered for scoring"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[0] * 4 for i in range(4)]
        # Only UP and RIGHT are valid moves
        mock_game.make_move.side_effect = [True, False, False, True]
        mock_game.set_board.return_value = None

        with patch('algorithms.depth_one_move.evaluate_board') as mock_eval:
            mock_eval.side_effect = [10, 20]  # UP=10, RIGHT=20

            result = depth_one_move(mock_game)

            assert result == "right"
            assert mock_eval.call_count == 2  # Only called for valid moves
