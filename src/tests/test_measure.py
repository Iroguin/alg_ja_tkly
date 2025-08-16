"""Tests for measure.py code"""
from unittest.mock import Mock, patch
import pytest  # pylint: disable=unused-import
from measure import run_single_game, analyze_games


class TestRunSingleGame:
    """Tests for the run_single_game function"""
    @patch('measure.Game2048')
    @patch('measure.get_best_move_expectiminimax')
    def test_expectiminimax_algorithm(self, mock_get_move, mock_game_class):
        mock_game = Mock()
        mock_game_class.return_value = mock_game
        mock_game.is_game_over.side_effect = [False, False, True]
        mock_game.make_move.return_value = True
        mock_game.is_won.side_effect = [False, True]
        mock_game.get_board_sum.return_value = 4096
        mock_game.board = [[2048, 1024, 512, 256], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        mock_get_move.return_value = 'up'

        result = run_single_game("expectiminimax", depth=3)

        assert result == {
            'moves': 2,
            'score': 4096,
            'max_tile': 2048,
            'won': True}
        mock_get_move.assert_called_with(mock_game, 3)

    @patch('measure.Game2048')
    @patch('measure.depth_one_move')
    def test_depth_one_algorithm(self, mock_depth_move, mock_game_class):
        mock_game = Mock()
        mock_game_class.return_value = mock_game
        mock_game.is_game_over.side_effect = [False, True]
        mock_game.make_move.return_value = True
        mock_game.is_won.return_value = False
        mock_game.get_board_sum.return_value = 2048
        mock_game.board = [[1024, 512, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        mock_depth_move.return_value = 'down'

        result = run_single_game("depth_one")

        assert result == {
            'moves': 1,
            'score': 2048,
            'max_tile': 1024,
            'won': False}
        mock_depth_move.assert_called_with(mock_game)

    def test_invalid_algorithm(self):
        with pytest.raises(ValueError, match="Unknown algorithm: invalid"):
            run_single_game("invalid")

    @patch('measure.Game2048')
    @patch('measure.get_best_move_expectiminimax')
    def test_invalid_moves_not_counted(self, mock_get_move, mock_game_class):
        mock_game = Mock()
        mock_game_class.return_value = mock_game
        mock_game.is_game_over.side_effect = [False, False, True]
        mock_game.make_move.side_effect = [False, True]  # First move invalid
        mock_game.is_won.return_value = False
        mock_game.get_board_sum.return_value = 1024
        mock_game.board = [[512, 0, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        result = run_single_game("expectiminimax")

        assert result['moves'] == 1  # Only successful moves counted


class TestAnalyzeGames:
    """Tests for the analyze_game function"""
    @patch('measure.run_single_game')
    @patch('builtins.print')
    @patch('time.time')
    def test_basic_statistics(self, mock_time, mock_print, mock_run_single):
        mock_time.side_effect = [0, 10]
        mock_run_single.side_effect = [
            {'moves': 100, 'score': 2048, 'max_tile': 512, 'won': False},
            {'moves': 150, 'score': 4096, 'max_tile': 1024, 'won': True},
            {'moves': 200, 'score': 8192, 'max_tile': 2048, 'won': True}
        ]

        analyze_games(num_games=3, algorithm="expectiminimax", depth=2)

        assert mock_run_single.call_count == 3
        for call in mock_run_single.call_args_list:
            assert call[0] == ("expectiminimax", 2)

        output = '\n'.join(str(
            call[0][0]) for call in mock_print.call_args_list if call[0] and len(call[0]) > 0)
        assert "Games played: 3" in output
        assert "Win rate (2048 reached): 66.7% (2/3)" in output
        assert "Average moves per game: 150.0" in output
        assert "Average score: 4778.7" in output
        assert "Min score: 2048 | Max score: 8192" in output
        assert "Min moves: 100 | Max moves: 200" in output

    @patch('measure.run_single_game')
    @patch('builtins.print')
    @patch('time.time')
    def test_tile_distribution(self, mock_time, mock_print, mock_run_single):
        mock_time.side_effect = [0, 1]
        mock_run_single.side_effect = [
            {'moves': 100, 'score': 2048, 'max_tile': 512, 'won': False},
            {'moves': 100, 'score': 2048, 'max_tile': 512, 'won': False},
            {'moves': 100, 'score': 4096, 'max_tile': 1024, 'won': True}
        ]

        analyze_games(num_games=3)

        output = '\n'.join(str(
            call[0][0]) for call in mock_print.call_args_list if call[0] and len(call[0]) > 0)
        assert "1024:   1 games ( 33.3%)" in output
        assert "  512:   2 games ( 66.7%)" in output


if __name__ == "__main__":
    pytest.main([__file__])
