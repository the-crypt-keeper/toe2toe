import json
from typing import List
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
        board_json = json.dumps(self._board_to_2d_array(state.board), indent=2)
        move_prompt = self.move_template.format(symbol=self.symbol, board=board_json)

        self.conversation_history.append({"role": "user", "content": move_prompt})

        while True:
            response = self._get_chat_completion()
            self.conversation_history.append({"role": "assistant", "content": response})
            
            try:
                move_data = json.loads(response)
                thought = move_data['thought']
                move_row = move_data['move_row']
                move_col = move_data['move_col']

                move = move_row * 3 + move_col
                if state.board[move] == '':                    
                    print(f"{self.model_name} Thought: {thought}")
                    return move
                else:
                    print("[BAD-MOVE]", response)
                    error_message = f"The spot at row {move_row}, column {move_col} is already taken. Please choose an empty spot."
                    self.conversation_history.append({"role": "user", "content": error_message})
            except (json.JSONDecodeError, KeyError):
                print("[BAD-FORMAT]", response)
                error_message = "Invalid response format. Please provide a valid JSON object with 'thought', 'move_row', and 'move_col' fields."
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

    def _board_to_2d_array(self, board: List[str]) -> List[List[str]]:
        return [
            board[0:3],
            board[3:6],
            board[6:9]
        ]
