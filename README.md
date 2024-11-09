# toe2toe: A Tic-Tac-Toe LLM Evaluation System

This project implements a system to evaluate the ability of large language models (LLMs) to play Tic-Tac-Toe. It provides a framework for testing and comparing different LLM-based players against each other or against an ideal player implementation.

## Project Structure

- `ttt_core.py`: Contains the core game logic, including the `TTTState` class which represents the game state.
- `ttt_players.py`: Defines player classes, including the `TTTPlayerIdeal` which implements an optimal strategy.
- `ttt_llm.py`: Implements the `TTTPlayerLLMJson` class for integrating LLMs as Tic-Tac-Toe players.
- `toe2toe.py`: Contains the main simulation logic for running games between players and calculating statistics.

## Features

- Tic-Tac-Toe game state management
- Ideal player implementation with optimal move selection
- Integration with LLMs for player behavior using OpenAI-compatible APIs
- Evaluation metrics for comparing LLM performance
- Flexible configuration for different LLM models and API endpoints

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/the-crypt-keeper/toe2toe.git
   cd toe2toe
   ```

2. Install the required dependencies:
   ```
   pip install openai
   ```

3. Set up your LLM API endpoint and credentials (if required).

## Usage

To run a simulation between two LLM players:

1. Open `toe2toe.py` and configure the `TTTPlayerLLMJson` instances with your desired API endpoints and model names.

2. Run the simulation:
   ```
   python toe2toe.py
   ```

This will execute a series of games between the configured players and output the results and statistics.

## Customization

- Modify the `system_prompt` and `move_template` in `TTTPlayerLLMJson` to experiment with different prompting strategies.
- Adjust the `num_games` variable in `toe2toe.py` to change the number of games in each simulation.
- Implement new player classes in `ttt_players.py` to test different strategies or integrate other AI models.

## Contributing

Contributions to improve the system or add new features are welcome. Please feel free to submit pull requests or open issues for discussion.

## License

This project is open-source and available under the MIT License.
