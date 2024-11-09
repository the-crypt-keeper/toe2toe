from ttt_core import TTTState
from ttt_players import TTTPlayerIdeal
from ttt_llm import TTTPlayerLLMJson

def play_game(player1, player2):
    state = TTTState()
    current_player = player1

    while not state.is_game_over():
        move = current_player.next_move(state)
        state.make_move(move)
        current_player = player2 if current_player == player1 else player1

    return state.get_winner()

def simulate_games(num_games, player1, player2):
    results = {'X': 0, 'O': 0, 'Draw': 0}

    for _ in range(num_games):
        winner = play_game(player1, player2)
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1

    return results

if __name__ == "__main__":
    num_games = 10
    player_ideal = TTTPlayerIdeal('X')
    player_llm = TTTPlayerLLMJson('O', 'http://100.109.96.89:3333/', 'gpt-4o-mini-2024-07-18', 
                                  "You are an AI playing Tic-Tac-Toe. Respond with valid JSON.",
                                  "It's your turn to play. You are '{symbol}'. The current board state is: {board}. Provide your next move as a JSON object with 'thought', 'move_row', and 'move_col' fields.")

    results = simulate_games(num_games, player_ideal, player_llm)

    print(f"Results of {num_games} games between TTTPlayerIdeal (X) and TTTPlayerLLMJson (O):")
    print(f"Player X (Ideal) wins: {results['X']}")
    print(f"Player O (LLM) wins: {results['O']}")
    print(f"Draws: {results['Draw']}")

    win_percentage_x = (results['X'] / num_games) * 100
    win_percentage_o = (results['O'] / num_games) * 100
    draw_percentage = (results['Draw'] / num_games) * 100

    print(f"\nWin percentage for Player X (Ideal): {win_percentage_x:.2f}%")
    print(f"Win percentage for Player O (LLM): {win_percentage_o:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")
