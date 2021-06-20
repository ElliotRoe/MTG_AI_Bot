from GameStateInterface import GameStateSecondary


class AIKernel:
    """
    Informal Interface
    Defines kernel methods for the AI type.
    """

    def generate_move(self, game_state: GameStateSecondary) -> str:
        """
        Takes in the game state of a game and returns

        Parameters:
            game_state GameStateSecondary: a valid game state of a game
        Requires:
            game_state is of a valid form
        Returns:
            An allowed move in Dict format
        """
        pass

