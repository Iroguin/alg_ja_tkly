"""Tests for core game logic"""

import pytest
import random
from unittest.mock import patch
from game import Game2048, UP, DOWN, LEFT, RIGHT


class TestGame2048Initialization:
    """Test game initialization"""

    def test_empty_board_creation(self):
        """Test that create_empty_board creates a 4x4 grid of zeros"""
        game = Game2048()
        empty_board = game.create_empty_board()

        assert len(empty_board) == 4
        assert all(len(row) == 4 for row in empty_board)
        assert all(cell == 0 for row in empty_board for cell in row)

    @patch('random.choice')
    @patch('random.random')
    def test_initialization_adds_two_tiles(self, mock_random, mock_choice):
        """Test that initialization adds exactly two tiles"""
        # Mock the tile placement and values
        # Place tiles at specific positions
        mock_choice.side_effect = [(0, 0), (1, 1)]
        # First tile gets 2, second gets 4
        mock_random.side_effect = [0.5, 0.95]

        game = Game2048()
        non_zero_count = sum(
            1 for row in game.board for cell in row if cell != 0)
        assert non_zero_count == 2

        # Check specific placements
        assert game.board[0][0] == 2
        assert game.board[1][1] == 4


class TestRandomTileAddition:
    """Test random tile addition logic"""

    def test_add_random_tile_to_empty_board(self):
        """Test adding a tile to an empty board"""
        game = Game2048()
        game.board = game.create_empty_board()

        with patch('random.choice', return_value=(2, 3)), \
                patch('random.random', return_value=0.5):
            game.add_random_tile()
            assert game.board[2][3] == 2

    def test_tile_probability_distribution(self):
        """Test that tiles are 90% 2s and 10% 4s"""
        game = Game2048()
        game.board = game.create_empty_board()

        # Test tile 2 (90% chance)
        with patch('random.choice', return_value=(0, 0)), \
                patch('random.random', return_value=0.5):  # < 0.9
            game.add_random_tile()
            assert game.board[0][0] == 2

        # Test tile 4 (10% chance)
        game.board = game.create_empty_board()
        with patch('random.choice', return_value=(0, 0)), \
                patch('random.random', return_value=0.95):  # >= 0.9
            game.add_random_tile()
            assert game.board[0][0] == 4

    def test_add_random_tile_no_empty_cells(self):
        """Test that no tile is added when board is full"""
        game = Game2048()
        # Fill the board completely
        game.board = [[2] * 4 for _ in range(4)]

        original_board = [row[:] for row in game.board]
        game.add_random_tile()

        assert game.board == original_board


class TestRowOperations:
    """Test row movement and combination logic"""

    def test_move_numbers_left_basic(self):
        game = Game2048()

        # Test with gaps
        assert game.move_numbers_left([2, 0, 4, 0]) == [2, 4, 0, 0]
        assert game.move_numbers_left([0, 0, 2, 4]) == [2, 4, 0, 0]
        assert game.move_numbers_left([0, 0, 0, 0]) == [0, 0, 0, 0]
        assert game.move_numbers_left([2, 4, 8, 16]) == [2, 4, 8, 16]

    def test_combine_row_basic_combinations(self):
        game = Game2048()

        # Simple combinations
        assert game.combine_row([2, 2, 0, 0]) == [4, 0, 0, 0]
        assert game.combine_row([2, 2, 4, 4]) == [4, 8, 0, 0]
        assert game.combine_row([0, 2, 2, 0]) == [4, 0, 0, 0]

    def test_combine_row_no_double_merge(self):
        """Test that tiles don't merge twice in one move"""
        game = Game2048()

        # A tile that just merged cannot merge again
        assert game.combine_row([2, 2, 4, 0]) == [4, 4, 0, 0]
        assert game.combine_row([4, 2, 2, 0]) == [4, 4, 0, 0]

    def test_combine_row_triple_tiles(self):
        """Test behavior with three identical tiles"""
        game = Game2048()

        # Only the first two should merge
        assert game.combine_row([2, 2, 2, 0]) == [4, 2, 0, 0]
        assert game.combine_row([4, 4, 4, 4]) == [8, 8, 0, 0]

    def test_combine_row_no_combinations(self):
        """Test rows with no possible combinations"""
        game = Game2048()

        assert game.combine_row([2, 4, 8, 16]) == [2, 4, 8, 16]
        assert game.combine_row([2, 4, 2, 4]) == [2, 4, 2, 4]


class TestMovement:
    """Test board movement in all directions"""

    def test_move_left(self):
        game = Game2048()
        game.set_board([
            [2, 0, 2, 0],
            [4, 4, 0, 0],
            [0, 8, 0, 8],
            [2, 4, 8, 16]
        ])

        with patch.object(game, 'add_random_tile'):
            game.make_move(LEFT)

        expected = [
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [16, 0, 0, 0],
            [2, 4, 8, 16]
        ]
        assert game.board == expected

    def test_move_right(self):
        game = Game2048()
        game.set_board([
            [2, 0, 2, 0],
            [0, 0, 4, 4],
            [8, 0, 0, 8],
            [2, 4, 8, 16]
        ])

        with patch.object(game, 'add_random_tile'):
            game.make_move(RIGHT)

        expected = [
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [0, 0, 0, 16],
            [2, 4, 8, 16]
        ]
        assert game.board == expected

    def test_move_up(self):
        game = Game2048()
        game.set_board([
            [2, 4, 0, 2],
            [0, 4, 8, 4],
            [2, 0, 0, 8],
            [0, 0, 8, 16]
        ])

        with patch.object(game, 'add_random_tile'):
            game.make_move(UP)

        expected = [
            [4, 8, 16, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [0, 0, 0, 16]
        ]
        assert game.board == expected

    def test_move_down(self):
        game = Game2048()
        game.set_board([
            [2, 4, 8, 2],
            [0, 4, 0, 4],
            [2, 0, 8, 8],
            [0, 0, 0, 16]
        ])

        with patch.object(game, 'add_random_tile'):
            game.make_move(DOWN)

        expected = [
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [4, 8, 16, 16]
        ]
        assert game.board == expected


class TestGameState:
    """Test game state checking"""

    def test_has_moves_available_empty_cells(self):
        """Test moves available when there are empty cells"""
        game = Game2048()
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],  # Has empty cell
            [4, 8, 16, 32]
        ])
        assert game.has_moves_available() is True

    def test_has_moves_available_horizontal_merge(self):
        """Test moves available with horizontal merge possibility"""
        game = Game2048()
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 2],  # Adjacent equal numbers
            [4, 8, 16, 32]
        ])
        assert game.has_moves_available() is True

    def test_has_moves_available_vertical_merge(self):
        """Test moves available with vertical merge possibility"""
        game = Game2048()
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [4, 8, 2, 32]  # Vertical match with row above
        ])
        assert game.has_moves_available() is True

    def test_no_moves_available(self):
        game = Game2048()
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [4, 8, 16, 32]
        ])
        assert game.has_moves_available() is False

    def test_check_win_condition(self):
        game = Game2048()

        # No win
        game.set_board([[2, 4, 8, 16]] * 4)
        assert game.check_win_condition() is False

        # Win condition
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4],  # Contains 2048
            [4, 8, 16, 32]
        ])
        assert game.check_win_condition() is True


class TestMoveValidation:
    """Test move validation and invalid moves"""

    def test_valid_move_returns_true(self):
        game = Game2048()
        game.set_board([
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        with patch.object(game, 'add_random_tile'):
            result = game.make_move(RIGHT)

        assert result is True

    def test_invalid_move_returns_false(self):
        """Test that moves that don't change the board return False"""
        game = Game2048()
        game.set_board([
            [2, 4, 8, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        with patch.object(game, 'add_random_tile'):
            result = game.make_move(RIGHT)  # Already at rightmost positions

        assert result is False

    def test_invalid_direction_returns_false(self):
        game = Game2048()
        result = game.make_move('x')  # Invalid direction
        assert result is False

    def test_direction_constants(self):
        """Test that direction constants work"""
        game = Game2048()
        game.set_board([
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        with patch.object(game, 'add_random_tile'):
            # Test all direction constants
            assert game.make_move(LEFT) is False
            assert game.make_move(RIGHT) is True

        game.set_board([[2, 0, 0, 0], [0, 0, 0, 0],
                       [0, 0, 0, 0], [0, 0, 0, 0]])
        with patch.object(game, 'add_random_tile'):
            assert game.make_move(UP) is False
            assert game.make_move(DOWN) is True


class TestBoardUtilities:
    """Test board utility functions"""

    def test_board_to_string(self):
        game = Game2048()
        game.set_board([
            [2, 0, 4, 8],
            [0, 16, 0, 32],
            [64, 0, 128, 0],
            [0, 256, 0, 512]
        ])

        result = game.board_to_string()
        lines = result.split('\n')

        assert len(lines) == 4
        assert "   2" in lines[0] and "   ." in lines[0]
        assert " 512" in lines[3]

    def test_get_board_copy(self):
        game = Game2048()
        original_board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        game.set_board(original_board)
        board_copy = game.get_board_copy()

        # Modify the copy
        board_copy[0][0] = 999

        # Original should be unchanged
        assert game.board[0][0] == 2
        assert board_copy[0][0] == 999

    def test_set_board(self):
        game = Game2048()
        new_board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 2],
            [4, 8, 16, 32]
        ]

        game.set_board(new_board)
        assert game.board == new_board


class TestGameStateProperties:
    """Test high-level game state properties"""

    def test_is_game_over(self):
        game = Game2048()

        # Game not over - has empty cells
        game.set_board([
            [2, 4, 8, 0],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [4, 8, 16, 32]
        ])
        assert game.is_game_over() is False

        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [4, 8, 16, 32]
        ])
        assert game.is_game_over() is True

    def test_is_won(self):
        game = Game2048()

        # Not won
        game.set_board([[2, 4, 8, 16]] * 4)
        assert game.is_won() is False

        # Won
        game.set_board([
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4],
            [4, 8, 16, 32]
        ])
        assert game.is_won() is True


# Integration test
class TestFullGameScenario:
    """Test complete game scenarios"""

    def test_simple_game_sequence(self):
        """Test a simple sequence of moves"""
        game = Game2048()
        game.set_board([
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        with patch.object(game, 'add_random_tile'):
            # Move up - should combine the 2s
            result = game.make_move(UP)
            assert result is True
            assert game.board[0][0] == 4
            assert game.board[1][0] == 0


if __name__ == "__main__":
    pytest.main([__file__])
