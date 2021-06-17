class AIKernel:
    """
    Informal Interface
    Defines kernel methods for the AI type.
    """

    def generate_move(self, game_state: (str, ...)) -> str:
        """
        Takes in the game state of a game and returns

        Parameters:
            game_state (str, ..., str): a valid game state of a game
        Requires:
            game_state is of a valid form
        Returns:
            An allowed move in String format
        """
        pass

