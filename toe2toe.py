from ttt_core import TTTState
from ttt_players import TTTPlayerIdeal
from ttt_llm import TTTPlayerLLMJson
import random

def play_game(player_x, player_o):
    state = TTTState()
    current_player = player_x

    while not state.is_game_over():
        move = current_player.next_move(state)
        state.make_move(move)
        current_player = player_o if current_player == player_x else player_x

    return state.get_winner()

def simulate_games(num_games, player1, player2):
    results = {'player1': 0, 'player2': 0, 'Draw': 0}

    for _ in range(num_games):
        # Randomly assign X and O
        if random.choice([True, False]):
            player1.symbol, player2.symbol = 'X', 'O'
            winner = play_game(player1, player2)
        else:
            player1.symbol, player2.symbol = 'O', 'X'
            winner = play_game(player2, player1)

        if winner == player1.symbol:
            results['player1'] += 1
        elif winner == player2.symbol:
            results['player2'] += 1
        else:
            results['Draw'] += 1

    return results

if __name__ == "__main__":
    num_games = 10
    player_ideal = TTTPlayerIdeal('X')  # Initial symbol, will be changed in each game
    player_llm = TTTPlayerLLMJson('O', 'http://100.109.96.89:3333/', 'gpt-4o-mini-2024-07-18', 
                                  "You are an AI playing Tic-Tac-Toe. Respond with valid JSON.",
                                  "It's your turn to play. You are '{symbol}'. The current board state is: {board}. Provide your next move as a JSON object with 'thought', 'move_row', and 'move_col' fields.")

    results = simulate_games(num_games, player_ideal, player_llm)

    print(f"Results of {num_games} games between TTTPlayerIdeal and TTTPlayerLLMJson:")
    print(f"TTTPlayerIdeal wins: {results['player1']}")
    print(f"TTTPlayerLLMJson wins: {results['player2']}")
    print(f"Draws: {results['Draw']}")

    win_percentage_ideal = (results['player1'] / num_games) * 100
    win_percentage_llm = (results['player2'] / num_games) * 100
    draw_percentage = (results['Draw'] / num_games) * 100

    print(f"\nWin percentage for TTTPlayerIdeal: {win_percentage_ideal:.2f}%")
    print(f"Win percentage for TTTPlayerLLMJson: {win_percentage_llm:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")
