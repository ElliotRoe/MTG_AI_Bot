class ControllerKernel:
    """
    Informal Interface
    Defines kernel methods for the Controller type.
    """

    def start_game(self) -> None:
        """ Starts a new MTG game from the "home screen"  """

    pass

    def get_game_state(self):
        """ 
        Returns a tuple representing the game's state
        Returns:
            Ugly dump of tuple which is basically just the MTGA log
        """

    pass

    def attack(self, card_id: int = -1) -> None:
        """
        Makes a specified card attack

        Parameters:
            card_id (int): the id of the card that should attack. If card = -1 then all should attack
        Requires:
            game_wave == ('player_attacking')
            number of cards that are able to attack > 0
        Ensures:
            Specified card attacks
        """

    pass

    def block(self, attacker_id: int, blocker_id: int) -> None:
        """
        Makes the blocker card block the attacker

        Parameters:
            attacker_id (int): The id of an opponents card that is attacking
            blocker_id (int): The id of a player's card that should block the specified attacking card
        Requires:
            game_wave == ('opponent_attacking')
            number of cards that are able to block > 0
        Ensures:
            Specified attacker is attempted to be blocked by blocker card
        Returns:
            If the block was successful
        """
        pass

    def cast(self, card_id: int) -> None:
        """
        Makes the blocker card block the attacker

        Parameters:
            card_id (int): The id of a card in the player's hand
        Requires:
            The requirements to cast the card are met
        Ensures:
            Specified card is cast
        Returns:
            If the cast was successful
        """
        pass

    def activate_ability(self, card_id: int, ability_id: int) -> None:
        """
        Activates a specified card's specified ability

        Parameters:
            card_id (int): The id of a card in the player's hand
            ability_id (int): The id of an ability that is to be activated
        Requires:
            All prerequisites for the ability are filled
        Ensures:
            Specified card's ability is used
        """
        pass

    def resolve(self):
        """ Passes and or resolves a decision in the game. Basically a "do nothing" method """
        pass

    def all_attack(self) -> None:
        """ Attacks with all cards that can attack """
        pass


class ControllerSecondary(ControllerKernel):
    """
    Informal Interface
    Defines secondary methods for the Controller type.
    """

    def get_game_state_pretty(self):
        """
        Returns a tuple representing the game's state Returns: (permanents and attributes, player's hand, opponent's
        hand, life totals, spells on the stack, cards in other zones, turn phase, turn)
        """

        pass

    def all_block(self) -> None:
        """ Blocks with all creatures that can block. There is no particular order. Note: kinda complicated to
        implement """
        pass

    def game_over(self) -> bool:
        """ Checks if the game is over and returns true if it is """
