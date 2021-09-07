from GameStateInterface import GameStateSecondary


class AIKernel:
    """
    Informal Interface
    Defines kernel methods for the AI type.
    """

    def generate_move(self, game_state: GameStateSecondary):
        """
        Takes in the game state of a game and returns a Dict of representing a valid move

        Parameters:
            game_state GameStateSecondary: a valid game state of a game
        Requires:
            game_state is of a valid form
        Returns:
            [valid_move: [int,...]]
        """
        pass

