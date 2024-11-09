class TTTState:
    def __init__(self):
        self.board = [''] * 9  # 9 empty positions
        self.current_player = 'X'  # X starts the game

    def make_move(self, position):
        if 0 <= position < 9 and self.board[position] == '':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def is_game_over(self):
        # Check for a win
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return True
        
        # Check for a draw
        if '' not in self.board:
            return True
        
        return False

    def get_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return self.board[combo[0]]
        return None  # No winner or draw

    def __str__(self):
        return '\n'.join(' | '.join(['-' if x == '' else x for x in self.board[i:i+3]]) for i in range(0, 9, 3))
