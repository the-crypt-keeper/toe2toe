from ttt_core import TTTState                                                                                                                                                                                                
                                                                                                                                                                                                                              
class TTTPlayer:                                                                                                                                                                                                             
    def __init__(self):                                                                                                                                                                                              
        self.symbol = None                                                                                                                                                                                                 

    def new_game(self, symbol):
        """Reset any game-specific state and set the player's symbol."""
        self.symbol = symbol
                                                                                                                                                                                                                            
    def next_move(self, state: TTTState) -> int:                                                                                                                                                                             
        raise NotImplementedError("Subclasses must implement next_move method")                                                                                                                                              
                                                                                                                                                                                                                              
class TTTPlayerIdeal(TTTPlayer):                                                                                                                                                                                             
    def next_move(self, state: TTTState) -> int:
        if self.symbol is None:
            raise ValueError("Player symbol not set. Call new_game() before making moves.")
                                                                                                                                                                                             
        # Check for winning move                                                                                                                                                                                             
        winning_move = self._find_winning_move(state, self.symbol)                                                                                                                                                           
        if winning_move is not None:                                                                                                                                                                                         
            return winning_move                                                                                                                                                                                              
                                                                                                                                                                                                                            
        # Check for blocking opponent's winning move                                                                                                                                                                         
        opponent = 'O' if self.symbol == 'X' else 'X'                                                                                                                                                                        
        blocking_move = self._find_winning_move(state, opponent)                                                                                                                                                             
        if blocking_move is not None:                                                                                                                                                                                        
            return blocking_move                                                                                                                                                                                             
                                                                                                                                                                                                                            
        # Prefer middle                                                                                                                                                                                                      
        if state.board[4] == '':                                                                                                                                                                                             
            return 4                                                                                                                                                                                                         
                                                                                                                                                                                                                            
        # Prefer corners                                                                                                                                                                                                     
        corners = [0, 2, 6, 8]                                                                                                                                                                                               
        for corner in corners:                                                                                                                                                                                               
            if state.board[corner] == '':                                                                                                                                                                                    
                return corner                                                                                                                                                                                                
                                                                                                                                                                                                                            
        # Take any available space                                                                                                                                                                                           
        for i in range(9):                                                                                                                                                                                                   
            if state.board[i] == '':                                                                                                                                                                                         
                return i                                                                                                                                                                                                     
                                                                                                                                                                                                                            
    def _find_winning_move(self, state: TTTState, symbol: str) -> int | None:                                                                                                                                                
        winning_combinations = [                                                                                                                                                                                             
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows                                                                                                                                                                         
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns                                                                                                                                                                      
            (0, 4, 8), (2, 4, 6)  # Diagonals                                                                                                                                                                                
        ]                                                                                                                                                                                                                    
        for a, b, c in winning_combinations:                                                                                                                                                                                 
            if state.board[a] == state.board[b] == symbol and state.board[c] == '':                                                                                                                                          
                return c                                                                                                                                                                                                     
            if state.board[a] == state.board[c] == symbol and state.board[b] == '':                                                                                                                                          
                return b                                                                                                                                                                                                     
            if state.board[b] == state.board[c] == symbol and state.board[a] == '':                                                                                                                                          
                return a                                                                                                                                                                                                     
        return None
