from openai import OpenAI
from ttt_core import TTTState
from ttt_players import TTTPlayer
import json
from copy import copy

class TTTPlayerLLMJson(TTTPlayer):
    def __init__(self, model_name: str, api_base: str, system_prompt: str = None, move_template: str = None, api_key: str = 'x-ignored', json_response_mode = False, has_system_role = True):
        super().__init__()
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        self.model_name = model_name
        
        self.system_prompt="You are an AI playing Tic-Tac-Toe. Respond with valid JSON."
        if system_prompt: self.system_prompt = system_prompt
        self.has_system_role = has_system_role
        
        self.move_template="It's your turn to play. You are '{symbol}'. The current board state is:\n\n{board}\n\nProvide your next move as a JSON object with 'thought', 'move_row' (one of: top, middle, bottom), and 'move_col' (one of: left, center, right) fields."
        if move_template: self.move_template = move_template

        self.conversation_history = []
        self.json_response_mode = json_response_mode
        
    def player_name(self):
        return self.model_name

    def new_game(self, symbol: str):
        """Reset conversation history for a new game and set the player's symbol."""
        super().new_game(symbol)
        self.conversation_history = []

    def next_move(self, state: TTTState) -> int:
        board_str = str(state)
        move_prompt = self.move_template.format(symbol=self.symbol, board=board_str)
        self.conversation_history.append({"role": "user", "content": move_prompt})  

        bad_reply_count = 0
        while True:
            response = self._get_chat_completion()
            self.conversation_history.append({"role": "assistant", "content": response})
            
            try:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    move_data = json.loads(response[json_start:json_end])
                thought = move_data['thought']
                move_row = move_data['move_row']
                move_col = move_data['move_col']

                move = self._convert_move(move_row, move_col)
                if state.board[move] == '':
                    print(f"{self.model_name} takes {move_row} {move_col}. Thought: {thought}")
                    return move
                else:
                    print(board_str)
                    print("[BAD-MOVE]", response)
                    available_moves = self._get_available_moves(state)
                    error_message = f"The spot at {move_row} {move_col} is already taken. Available moves: {available_moves}. Please choose an empty spot."
                    self.conversation_history.append({"role": "user", "content": error_message})
                    bad_reply_count += 1
            except (json.JSONDecodeError, KeyError, ValueError):
                print("[BAD-FORMAT]", response)
                available_moves = self._get_available_moves(state)
                error_message = f"Invalid response format. Available moves: {available_moves}. Please provide a valid JSON object with 'thought', 'move_row' (one of: top, middle, bottom), and 'move_col' (one of: left, center, right) fields."
                self.conversation_history.append({"role": "user", "content": error_message})
                bad_reply_count += 1
            
            if bad_reply_count >= 2:
                print("LLM failed to provide a valid move after two attempts. Failing this round.")
                return -1  # Indicate a failed round

    def _get_chat_completion(self) -> str:
        if self.has_system_role:
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history        
        else:
            messages = copy(self.conversation_history)
            messages[0]['content'] = self.system_prompt + '\n\n' + messages[0]['content']
        extra_args = { "response_format": {"type": "json_object"} } if self.json_response_mode else {}
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **extra_args
        )

        return response.choices[0].message.content

    def _convert_move(self, row: str, col: str) -> int:
        row_map = {'top': 0, 'middle': 1, 'bottom': 2}
        col_map = {'left': 0, 'center': 1, 'right': 2}
        return row_map[row] * 3 + col_map[col]

    def _get_available_moves(self, state: TTTState) -> list:
        available_moves = []
        row_map = {0: 'top', 1: 'middle', 2: 'bottom'}
        col_map = {0: 'left', 1: 'center', 2: 'right'}
        for i, spot in enumerate(state.board):
            if spot == '':
                row = row_map[i // 3]
                col = col_map[i % 3]
                available_moves.append(f"{row} {col}")
        return available_moves
