from ttt_core import TTTState
from ttt_players import TTTPlayerIdeal
from ttt_llm import TTTPlayerLLMJson
import random

def play_game(player_x, player_o):
    state = TTTState()
    current_player = player_x

    while not state.is_game_over():
        move = current_player.next_move(state)
        if move == -1:
            print(f"Player {current_player.symbol} failed to make a valid move. Game over.")
            return 'F' if current_player == player_x else 'f'
        state.make_move(move)
        current_player = player_o if current_player == player_x else player_x
        
    print("---- Final State ----")
    print(state)

    return state.get_winner()

def simulate_games(num_games, player1, player2):
    results = {'player1': 0, 'player2': 0, 'Draw': 0, 'player1_failure': 0, 'player2_failure': 0}

    for _ in range(num_games):
        # Randomly assign X and O
        if random.choice([True, False]):
            player1.new_game('X')
            player2.new_game('O')
            winner = play_game(player1, player2)
        else:
            player1.new_game('O')
            player2.new_game('X')
            winner = play_game(player2, player1)

        if winner == player1.symbol:
            results['player1'] += 1
        elif winner == player2.symbol:
            results['player2'] += 1
        elif winner == 'F':
            results['player1_failure'] += 1
        elif winner == 'f':
            results['player2_failure'] += 1
        else:
            results['Draw'] += 1

    return results

if __name__ == "__main__":
    num_games = 10
    player_ideal = TTTPlayerIdeal()
    
    player_llm_0 = TTTPlayerLLMJson(
        api_base='http://100.109.96.89:3333/v1/',
        model_name='Hermes-2-Theta-Llama-3-8B-exl2_65bpw'
    )
    player_llm_1 = TTTPlayerLLMJson(
        api_base='http://100.109.96.89:3333/v1/',
        model_name='gpt-4o-mini-2024-07-18'
    )

    results = simulate_games(num_games, player_llm_0, player_llm_1)

    print(f"Results of {num_games} games between TTTPlayerIdeal and TTTPlayerLLMJson:")
    print(f"TTTPlayerIdeal wins: {results['player1']}")
    print(f"TTTPlayerLLMJson wins: {results['player2']}")
    print(f"Draws: {results['Draw']}")
    print(f"TTTPlayerIdeal failures: {results['player1_failure']}")
    print(f"TTTPlayerLLMJson failures: {results['player2_failure']}")

    total_valid_games = num_games - results['player1_failure'] - results['player2_failure']
    win_percentage_ideal = (results['player1'] / total_valid_games) * 100 if total_valid_games > 0 else 0
    win_percentage_llm = (results['player2'] / total_valid_games) * 100 if total_valid_games > 0 else 0
    draw_percentage = (results['Draw'] / total_valid_games) * 100 if total_valid_games > 0 else 0
    failure_percentage_ideal = (results['player1_failure'] / num_games) * 100
    failure_percentage_llm = (results['player2_failure'] / num_games) * 100

    print(f"\nWin percentage for TTTPlayerIdeal: {win_percentage_ideal:.2f}%")
    print(f"Win percentage for TTTPlayerLLMJson: {win_percentage_llm:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")
    print(f"Failure percentage for TTTPlayerIdeal: {failure_percentage_ideal:.2f}%")
    print(f"Failure percentage for TTTPlayerLLMJson: {failure_percentage_llm:.2f}%")
