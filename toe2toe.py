from ttt_core import TTTState
from ttt_players import TTTPlayerIdeal

def play_game(player1, player2):
    state = TTTState()
    current_player = player1

    while not state.is_game_over():
        move = current_player.next_move(state)
        state.make_move(move)
        current_player = player2 if current_player == player1 else player1

    return state.get_winner()

def simulate_games(num_games):
    player_x = TTTPlayerIdeal('X')
    player_o = TTTPlayerIdeal('O')
    
    results = {'X': 0, 'O': 0, 'Draw': 0}

    for _ in range(num_games):
        winner = play_game(player_x, player_o)
        if winner:
            results[winner] += 1
        else:
            results['Draw'] += 1

    return results

if __name__ == "__main__":
    num_games = 1000
    results = simulate_games(num_games)

    print(f"Results of {num_games} games between two ideal players:")
    print(f"Player X wins: {results['X']}")
    print(f"Player O wins: {results['O']}")
    print(f"Draws: {results['Draw']}")

    win_percentage_x = (results['X'] / num_games) * 100
    win_percentage_o = (results['O'] / num_games) * 100
    draw_percentage = (results['Draw'] / num_games) * 100

    print(f"\nWin percentage for Player X: {win_percentage_x:.2f}%")
    print(f"Win percentage for Player O: {win_percentage_o:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")
