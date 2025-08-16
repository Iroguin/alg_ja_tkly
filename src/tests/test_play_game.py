"""Tests for play_game.py"""

from unittest.mock import Mock, patch
import sys  # pylint: disable=unused-import
from io import StringIO
import pytest
from play_game import play_game_ai


class TestPlayGameAI:
    """Test the play_game_ai function"""

    def test_expectiminimax_algorithm(self):
        """Test game plays with expectiminimax algorithm"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up') as mock_algo:
                with patch('sys.stdout', new_callable=StringIO):
                    play_game_ai(algorithm="expectiminimax", depth=3)

                assert mock_algo.call_count == 2
                mock_algo.assert_called_with(mock_game, 3)

    def test_depth_one_algorithm(self):
        """Test game plays with depth_one algorithm"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.depth_one_move', return_value='left') as mock_algo:
                with patch('sys.stdout', new_callable=StringIO):
                    play_game_ai(algorithm="depth_one")

                assert mock_algo.call_count == 2
                mock_algo.assert_called_with(mock_game)

    def test_invalid_algorithm_raises_error(self):
        """Test that invalid algorithm name raises ValueError"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.return_value = False  # Ensure loop runs
            mock_game.is_won.return_value = False
            mockgame2048.return_value = mock_game

            with pytest.raises(ValueError, match="Unknown algorithm: invalid_algo"):
                play_game_ai(algorithm="invalid_algo")

    def test_win_condition(self):
        """Test game continues after win condition is met"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [
                False, False, False, True]  # Game continues after win
            mock_game.is_won.side_effect = [
                False, True, True]  # Win on second move, stays won
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up') as mock_algo:
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai()

                # Game should continue for 3 moves even after winning
                assert mock_algo.call_count == 3
                output = mock_stdout.getvalue()
                assert "Won in 2 moves!" in output  # Win message appears

    def test_game_over_condition(self):
        """Test game ends when no moves available"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai()

                output = mock_stdout.getvalue()
                assert "Game over after 2 moves!" in output

    def test_invalid_move_handling(self):
        """Test handling when invalid move chosen"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.return_value = False
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = False  # Invalid move
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai()

                output = mock_stdout.getvalue()
                assert "No valid moves available!" in output

    def test_move_counter(self):
        """Test that moves are counted correctly"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, False, False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai()

                output = mock_stdout.getvalue()
                assert "Move 0" in output
                assert "Move 1" in output
                assert "Move 2" in output
                assert "Game over after 3 moves!" in output

    def test_print_board_calls(self):
        """Test that board is printed at appropriate times"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO):
                    play_game_ai()

                # Board printed at start of each turn and at end
                assert mock_game.print_board.call_count == 2


class TestMainBlock:
    """Test command line argument parsing"""

    def test_play_game_with_defaults(self):
        """Test play_game_ai called with default arguments"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [True]
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax'):
                with patch('sys.stdout', new_callable=StringIO):
                    # Test default arguments
                    play_game_ai()

            # Verify game was created
            mockgame2048.assert_called_once()

    def test_play_game_with_depth_one(self):
        """Test play_game_ai with depth_one algorithm"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [True]
            mockgame2048.return_value = mock_game

            with patch('play_game.depth_one_move'):
                with patch('sys.stdout', new_callable=StringIO):
                    play_game_ai('depth_one')

            mockgame2048.assert_called_once()

    def test_play_game_with_custom_depth(self):
        """Test play_game_ai with custom depth"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [True]
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax') as mock_algo:
                with patch('sys.stdout', new_callable=StringIO):
                    play_game_ai('expectiminimax', 5)

            # Should not be called since game is immediately over
            mock_algo.assert_not_called()


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_immediate_game_over(self):
        """Test when game is over from the start"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.return_value = True
            mockgame2048.return_value = mock_game

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                play_game_ai()

            output = mock_stdout.getvalue()
            assert "Game over after 0 moves!" in output

    def test_immediate_win(self):
        """Test when game is won from the start"""
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            # Game should end after detecting the immediate win
            mock_game.is_game_over.side_effect = [
                False, True]  # False first, then True
            mock_game.is_won.return_value = True
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai()

                output = mock_stdout.getvalue()
                assert "Won in 1 moves!" in output

    def test_algorithm_output_messages(self):
        """Test algorithm info in output messages"""
        # Test expectiminimax with depth
        with patch('play_game.Game2048') as mockgame2048:
            mock_game = Mock()
            mock_game.is_game_over.side_effect = [False, True]
            mock_game.is_won.return_value = False
            mock_game.make_move.return_value = True
            mockgame2048.return_value = mock_game

            with patch('play_game.get_best_move_expectiminimax', return_value='up'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai("expectiminimax", 4)

                output = mock_stdout.getvalue()
                assert "expectiminimax algorithm (depth=4)" in output

        # Test depth_one without depth
        with patch('play_game.Game2048') as mockgame20482:
            mock_game2 = Mock()
            mock_game2.is_game_over.side_effect = [False, True]
            mock_game2.is_won.return_value = False
            mock_game2.make_move.return_value = True
            mockgame20482.return_value = mock_game2

            with patch('play_game.depth_one_move', return_value='down'):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    play_game_ai("depth_one")

                output = mock_stdout.getvalue()
                assert "depth_one algorithm" in output
                assert "(depth=" not in output.split(
                    "depth_one algorithm")[1].split("\n")[0]
