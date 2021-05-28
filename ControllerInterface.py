class ControllerInterface:
    def start_game(self) -> None:
        """ Starts a new MTG game from the "home screen"  """

    pass

    def get_game_state(self) -> (str, str):
        """ Returns a tuple representing the game's state """

    pass

    def attack(self, card: int = -1) -> None:
        """
        Makes a specified card attack

        Parameters:
            card (int): the id of the card that should attack. If card = -1 then all should attack
        Requires:
            game_wave == ('player_attacking')
            number of cards that are able to attack > 0
        Ensures:
            Specified card attacks
        """

    pass

    def block(self, attacker: int, blocker: int) -> bool:
        """
        Makes the blocker card block the attacker

        Parameters:
            attacker (int): The id of an opponents card that is attacking
            blocker (int): The id of a player's card that should block the specified attacking card
        Requires:
            game_wave == ('opponent_attacking')
            number of cards that are able to block > 0
        Ensures:
            Specified attacker is attempted to be blocked by blocker card
        Returns:
            If the block was successful
        """
        pass

    def cast(self, card: int) -> bool:
        """
        Makes the blocker card block the attacker

        Parameters:
            card (int): The id of a card in the player's hand
        Requires:
            game_wave == ('player_main') or (card is an instant and controller not busy)
            mana needed to cast the card is present
        Ensures:
            Specified card is cast
        Returns:
            If the cast was successful
        """
        pass

    def is_busy(self):
        """
        Checks if the controller is waiting on opponent or busy doing a task
        """
        pass
