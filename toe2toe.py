from ttt_core import TTTState
from ttt_players import TTTPlayerIdeal
from ttt_llm import TTTPlayerLLMJson
import random

def calculate_statistics(results, num_games):
    total_valid_games = num_games - results['player1_failure'] - results['player2_failure']
    stats = {
        'win_percentage_1': (results['player1'] / total_valid_games) * 100 if total_valid_games > 0 else 0,
        'win_percentage_2': (results['player2'] / total_valid_games) * 100 if total_valid_games > 0 else 0,
        'draw_percentage': (results['Draw'] / total_valid_games) * 100 if total_valid_games > 0 else 0,
        'failure_percentage_1': (results['player1_failure'] / num_games) * 100,
        'failure_percentage_2': (results['player2_failure'] / num_games) * 100
    }
    return stats

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
    num_games = 50
    player_ideal = TTTPlayerIdeal()
    
    player_llm_0 = TTTPlayerLLMJson(
        api_base='http://100.109.96.89:3333/v1/',
        model_name='Mistral-Nemo-Instruct-2407-Q6_K',
        has_system_role=False
    )
    player_llm_1 = TTTPlayerLLMJson(
        api_base='http://100.109.96.89:3333/v1/',
        model_name='Meta-Llama-3.1-8B-Instruct-Q8_0'
    )

    results = simulate_games(num_games, player_llm_0, player_llm_1)

    print(f"Results of {num_games} games between {player_llm_0.player_name()} and {player_llm_1.player_name()}:")
    print(f"{player_llm_0.player_name()} wins: {results['player1']}")
    print(f"{player_llm_1.player_name()} wins: {results['player2']}")
    print(f"Draws: {results['Draw']}")
    print(f"{player_llm_0.player_name()} failures: {results['player1_failure']}")
    print(f"{player_llm_1.player_name()} failures: {results['player2_failure']}")

    stats = calculate_statistics(results, num_games)

    print(f"\nWin percentage for {player_llm_0.player_name()}: {stats['win_percentage_1']:.2f}%")
    print(f"Win percentage for {player_llm_1.player_name()}: {stats['win_percentage_2']:.2f}%")
    print(f"Draw percentage: {stats['draw_percentage']:.2f}%")
    print(f"Failure percentage for {player_llm_0.player_name()}: {stats['failure_percentage_1']:.2f}%")
    print(f"Failure percentage for {player_llm_1.player_name()}: {stats['failure_percentage_2']:.2f}%")
