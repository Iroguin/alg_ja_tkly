"""Tests for expectiminimax algorythm"""

from unittest.mock import Mock, patch
import pytest
from algorithms.expectiminimax import expectiminimax, get_best_move_expectiminimax, UP


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

            with patch('algorithms.expectiminimax.expectiminimax',
                       return_value=10) as mock_expectiminimax:
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


class TestExpectiminimaxPlayerTurn:
    """Test expectiminimax algorithm player turn logic"""

    def test_player_turn_with_valid_moves(self):
        """Test evaluates all valid moves on player turn"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.board = [[0, 2, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        with patch('algorithms.expectiminimax.apply_move') as mock_apply:
            mock_apply.side_effect = [
                [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # UP
                [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # DOWN
                [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # LEFT
                [[0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],  # RIGHT
            ]

            with patch('algorithms.expectiminimax.evaluate_board', return_value=50):
                result = expectiminimax(
                    mock_game, depth=1, is_player_turn=True)

        assert result == 50
        assert mock_apply.call_count == 4  # All 4 directions tested

    def test_player_turn_no_valid_moves(self):
        """Test player turn when no moves are valid"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.board = [[2, 4, 2, 4], [
            4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        mock_game.get_board_copy.return_value = mock_game.board
        mock_game.make_move.return_value = False  # No valid moves

        with patch('algorithms.expectiminimax.evaluate_board', return_value=25):
            result = expectiminimax(mock_game, depth=2, is_player_turn=True)

        assert result == 25  # Falls back to evaluate_board


class TestExpectiminimaxRandomTurn:
    """Test expectiminimax algorithm random tile placement logic"""

    def test_random_tile_placement(self):
        """Test expectation calculation for random tile placement"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.board = [[2, 0, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        with patch('algorithms.expectiminimax.evaluate_board', return_value=100):
            with patch('algorithms.expectiminimax.random.sample') as mock_sample:
                # Mock sampling to return 7 cells (set to 7 in code to reduce
                # time)
                mock_sample.return_value = [
                    (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
                result = expectiminimax(
                    mock_game, depth=1, is_player_turn=False)

        # Should calculate weighted average across sampled cells
        assert pytest.approx(result) == 100
        assert mock_sample.called

    def test_random_turn_no_empty_cells(self):
        """Test random turn when board is full"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.board = [[2, 4, 8, 16], [32, 64, 128, 256], [
            512, 1024, 2048, 4096], [8192, 16384, 32768, 65536]]

        with patch('algorithms.expectiminimax.evaluate_board', return_value=75):
            result = expectiminimax(mock_game, depth=2, is_player_turn=False)

        assert result == 75  # No empty cells, returns evaluation


class TestExpectiminimaxMoveSimulation:
    """Test the actual move simulation logic"""

    def test_left_move_simulation(self):
        """Test LEFT move board transformation"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.board = [[2, 2, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        with patch('algorithms.expectiminimax._cached_game') as mock_cached:
            mock_cached.combine_row.side_effect = lambda row: [
                4, 0, 0, 0] if row == [2, 2, 0, 0] else row
            mock_cached.board = [[2, 2, 0, 0], [
                0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

            with patch('algorithms.expectiminimax.evaluate_board', return_value=100):
                expectiminimax(mock_game, depth=1, is_player_turn=True)

            # Verify combine_row was called for LEFT
            assert mock_cached.combine_row.called

    def test_up_down_move_transformations(self):
        """Test UP and DOWN move board transformations"""
        mock_game = Mock()
        board = [[2, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        mock_game.get_board_copy.return_value = board
        mock_game.is_game_over.return_value = False
        mock_game.board = board
        mock_game.set_board = Mock()

        with patch('algorithms.expectiminimax._cached_game') as mock_cached_game:
            mock_cached_game.board = board
            mock_cached_game.combine_row = Mock(
                side_effect=lambda col: [4, 0, 0, 0] if col == [2, 2, 0, 0] else col)

            with patch('algorithms.expectiminimax.evaluate_board', return_value=100):
                expectiminimax(mock_game, depth=1, is_player_turn=True)

            # Should have called combine_row for column operations
            assert mock_cached_game.combine_row.call_count > 0


class TestGetBestMoveAllDirections:
    """Test get_best_move_expectiminimax for all directions"""

    def test_all_moves_invalid_returns_up(self):
        """Test that UP is returned when all moves are invalid"""
        mock_game = Mock()
        full_board = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        mock_game.get_board_copy.return_value = full_board

        with patch('algorithms.expectiminimax.Game2048') as mockgame2048:
            mock_temp_game = Mock()
            mock_temp_game.board = full_board
            # No changes possible = board stays the same
            mock_temp_game.combine_row = Mock(side_effect=lambda row: row)
            mockgame2048.return_value = mock_temp_game

            result = get_best_move_expectiminimax(mock_game, depth=1)

        assert result == UP  # Default fallback


class TestRecursiveDepth:
    """Test recursive depth behavior"""

    def test_recursive_depth_calculation(self):
        """Test that recursion properly decrements depth"""
        mock_game = Mock()
        mock_game.is_game_over.return_value = False
        mock_game.get_board_copy.return_value = [
            [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        mock_game.board = [[2, 0, 0, 0], [
            0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        mock_game.make_move.return_value = True
        mock_game.set_board = Mock()

        with patch('algorithms.expectiminimax.Game2048') as mockgame2048:
            mock_temp_game = Mock()
            mock_temp_game.board = [[2, 0, 0, 0], [
                0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            mock_temp_game.combine_row = Mock(
                side_effect=lambda row: [
                    2, 0, 0, 0] if row[0] == 2 else row)
            mockgame2048.return_value = mock_temp_game

            with patch('algorithms.expectiminimax.evaluate_board', return_value=50):
                # Call with depth=2 to verify it reaches depth 0
                result = expectiminimax(
                    mock_game, depth=2, is_player_turn=True)

        # The function should return a value
        assert isinstance(result, (int, float))
