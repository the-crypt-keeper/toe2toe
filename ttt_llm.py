from typing import List, Tuple
from openai import OpenAI
from ttt_core import TTTState
from ttt_players import TTTPlayer

class TTTPlayerLLMJson(TTTPlayer):
    def __init__(self, symbol: str, model_name: str, system_prompt: str, move_template: str, api_base: str, api_key: str = 'x-ignored', json_response_mode = True):
        super().__init__(symbol)
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.move_template = move_template
        self.conversation_history = []
        self.json_response_mode = json_response_mode

    def new_game(self):
        """Reset conversation history for a new game."""
        self.conversation_history = []

    def next_move(self, state: TTTState) -> int:
        board_str = str(state)
        move_prompt = self.move_template.format(symbol=self.symbol, board=board_str)

        self.conversation_history.append({"role": "user", "content": move_prompt})

        while True:
            response = self._get_chat_completion()
            self.conversation_history.append({"role": "assistant", "content": response})
            
            try:
                move_data = json.loads(response)
                thought = move_data['thought']
                move_row = move_data['move_row']
                move_col = move_data['move_col']

                move = self._convert_move(move_row, move_col)
                if state.board[move] == '':                    
                    print(f"{self.model_name} Thought: {thought}")
                    return move
                else:
                    print("[BAD-MOVE]", response)
                    error_message = f"The spot at {move_row} {move_col} is already taken. Please choose an empty spot."
                    self.conversation_history.append({"role": "user", "content": error_message})
            except (json.JSONDecodeError, KeyError):
                print("[BAD-FORMAT]", response)
                error_message = "Invalid response format. Please provide a valid JSON object with 'thought', 'move_row' (one of: left, center, right), and 'move_col' (one of: top, middle, bottom) fields."
                self.conversation_history.append({"role": "user", "content": error_message})

    def _get_chat_completion(self) -> str:
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history        
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
