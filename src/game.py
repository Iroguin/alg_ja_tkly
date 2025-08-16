"""game.py contains core logic for the game"""
import random

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"


class Game2048:
    """Class encompassing the game"""

    def __init__(self):
        self.board = self.create_empty_board()
        self.add_random_tile()
        self.add_random_tile()

    def create_empty_board(self):
        """Create a 4x4 board filled with zeros"""
        return [[0] * 4 for j in range(4)]

    def move_numbers_left(self, row):
        """Move all non-zero numbers to the left, filling gaps with zeros"""
        non_zero_numbers = [cell for cell in row if cell]
        zeros = [0] * row.count(0)
        return non_zero_numbers + zeros

    def combine_row(self, row):
        """Combine adjacent equal numbers in a row (left direction)"""
        row = self.move_numbers_left(row)
        for i in range(3):  # Only 3 combinations possible
            if row[i] and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        return self.move_numbers_left(row)

    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = [(i, j) for i in range(4)
                       for j in range(4) if not self.board[i][j]]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # 90% chance for 2, 10% chance for 4
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def has_moves_available(self):
        """Check if any moves are still possible - OPTIMIZED"""
        # Check for empty cells first
        for row in self.board:
            if 0 in row:
                return True

        # Check for adjacent equal tiles
        for i in range(4):
            for j in range(3):
                # # Check right neighbor
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
                # Check bottom neighbor
                if self.board[j][i] == self.board[j + 1][i]:
                    return True
        return False

    def check_win_condition(self):
        """Check if tile 2048 has been reached"""
        return any(2048 in row for row in self.board)

    def get_board_sum(self):
        """Get the sum of all tiles on the board"""
        return sum(sum(row) for row in self.board)

    def make_move(self, direction):
        """
        Move in the direction given
        Returns True if the move was valid (board changed)
        """
        moved = False

        if direction in ('a', LEFT):  # Left
            for i in range(4):
                # Combine
                new_row = self.combine_row(self.board[i])
                if new_row != self.board[i]:
                    moved = True
                    self.board[i] = new_row

        elif direction in ('d', RIGHT):  # Right
            for i in range(4):
                # Reverse, combine, reverse
                new_row = self.combine_row(self.board[i][::-1])[::-1]
                if new_row != self.board[i]:
                    moved = True
                    self.board[i] = new_row

        elif direction in ('w', UP):  # Up
            for j in range(4):
                # Transpose, combine, transpose back
                col = [self.board[i][j] for i in range(4)]
                new_col = self.combine_row(col)
                if new_col != col:
                    moved = True
                    for i in range(4):
                        self.board[i][j] = new_col[i]

        elif direction in ('s', DOWN):  # Down
            for j in range(4):
                # Transpose, reverse, combine, reverse, transpose back
                col = [self.board[i][j] for i in range(4)]
                new_col = self.combine_row(col[::-1])[::-1]
                if new_col != col:
                    moved = True
                    for i in range(4):
                        self.board[i][j] = new_col[i]
        else:
            return False  # Invalid direction

        # Add new tile only if the board changed
        if moved:
            self.add_random_tile()
        return moved

    def board_to_string(self):
        """Convert board to string for testing"""
        lines = []
        for row in self.board:
            line = " ".join(f"{cell:4}" if cell else "   ." for cell in row)
            lines.append(line)
        return "\n".join(lines)

    def print_board(self):
        """Print the current board state"""
        print(self.board_to_string())

    def get_board_copy(self):
        """Get a copy of the current board state"""
        return [row[:] for row in self.board]

    def set_board(self, board):
        """Set the board state (useful for testing)"""
        self.board = [row[:] for row in board]

    def is_game_over(self):
        """Check if the game is over (no moves available)"""
        return not self.has_moves_available()

    def is_won(self):
        """Check if the game is won (2048 reached)"""
        return self.check_win_condition()


def get_user_input():
    """Get user input for the next move"""
    return input("Enter direction (wasd): ")


def main():
    """Main game loop"""
    game = Game2048()

    while not game.is_game_over():
        game.print_board()
        direction = get_user_input()

        if not game.make_move(direction):
            print("Invalid move! Try again.")
            continue

        if game.is_won():
            game.print_board()
            print("You win!")
            return

    game.print_board()
    print("Game over!")


if __name__ == "__main__":
    main()
