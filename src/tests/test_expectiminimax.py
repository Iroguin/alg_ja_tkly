"""Tests for expectiminimax algorythm"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from algorithms.expectiminimax import expectiminimax, get_best_move_expectiminimax


class TestExpectiminimax:
    """Test expectiminimax algorithm"""

    def test_base_case_depth_zero(self):
        """Test that depth 0 returns evaluation score"""
        mock_game = Mock()
        mock_game.board = [[2, 4], [8, 16]]

        with patch('algorithms.expectiminimax.evaluate_board', return_value=100):
            result = expectiminimax(mock_game, depth=0, is_player_turn=True)

        assert result == 100

    def test_base_case_game_over(self):
        """Test that game over returns evaluation score"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = True
        mock_game.board = [[2, 4], [8, 16]]

        with patch('algorithms.expectiminimax.evaluate_board', return_value=50):
            result = expectiminimax(mock_game, depth=3, is_player_turn=True)

        assert result == 50


class TestGetBestMoveExpectiminimax:
    """Test get_best_move_expectiminimax function"""

    def test_only_considers_valid_moves(self):
        """Test that only valid moves are evaluated"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[2, 4, 8, 16]] * 4

        with patch('algorithms.expectiminimax.Game2048') as mockgame:
            mock_temp_game = Mock()
            # Simulate that only some moves change the board

            def mock_combine_row(row):
                return row  # No change, simulating invalid move
            mock_temp_game.combine_row.side_effect = mock_combine_row
            mock_temp_game.board = [[2, 4, 8, 16]] * 4
            mockgame.return_value = mock_temp_game

            result = get_best_move_expectiminimax(mock_game, depth=2)

            # Should return fallback since no moves are valid
            assert result == "up"

    def test_default_depth(self):
        """Test that default depth is used when not specified"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[0] * 4 for i in range(4)]

        with patch('algorithms.expectiminimax.Game2048') as mockgame:
            mock_temp_game = Mock()
            mock_temp_game.combine_row.side_effect = lambda x: [
                1] + x[1:]  # Valid move
            mock_temp_game.board = [[0] * 4 for i in range(4)]
            mockgame.return_value = mock_temp_game

            with patch('algorithms.expectiminimax.expectiminimax', return_value=10) as mock_expectiminimax:
                get_best_move_expectiminimax(mock_game)  # No depth specified

                # Should be called with depth-1 = 2 (default depth is 3)
                mock_expectiminimax.assert_called_with(
                    mock_temp_game, 2, False)

    def test_handles_tie_scores(self):
        """Test behavior when multiple moves have same score"""
        mock_game = Mock()
        mock_game.get_board_copy.return_value = [[0] * 4 for i in range(4)]

        with patch('algorithms.expectiminimax.Game2048') as mockgame:
            mock_temp_game = Mock()
            mock_temp_game.combine_row.side_effect = lambda x: [
                1] + x[1:]  # Valid move
            mock_temp_game.board = [[0] * 4 for i in range(4)]
            mockgame.return_value = mock_temp_game

            with patch('algorithms.expectiminimax.expectiminimax', return_value=10):
                result = get_best_move_expectiminimax(mock_game, depth=2)

                # Should return first move that achieves the best score
                assert result == "up"
