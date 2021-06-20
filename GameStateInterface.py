from typing import Dict


class GameStateKernel:
    """
    Informal Interface
    Defines methods for the GameState type
    """

    def get_full_state(self) -> Dict[str, str or int]:
        """
        Returns:
             a dictionary object with the game state fully constructed like a JSON object
        """
        pass


class GameStateSecondary(GameStateKernel):
    """
    Informal Interface
    Defines secondary methods for the GameState type
    """

    def get_zone(self, zone_type: str, owner_seat_id: int = None) -> Dict[str, str or int]:
        """
        Gets specified zone information

        Parameters:
            zone_type (str): Which zone to pull information from. Must be one of the following: Revealed,
                Suppressed, Pending, Command, Stack, Battlefield, Exile, Limbo, Hand, Library, Graveyard, Sideboard
            owner_seat_id (int):  Which player owns the zone (this parameter is not required for zones that have no
                ownership)
        Returns:
            A properly formatted dictionary with all the information necessary needed for a zone
        """

    def get_actions(self):
        """
        Gets a list of possible actions

        """
        pass

    def get_actions(self) -> Dict[str, str or int]:
        """
        Gets all possible actions that are currently available

        Returns:
            A properly formatted dictionary with all the information necessary for actions
        """
        pass

    def get_turn_info(self) -> Dict[str, str or int]:
        """
        Gets all possible actions that are currently available

        Returns:
            A properly formatted dictionary with all the information necessary for actions
        """
        pass

    def get_players(self) -> Dict[str, str or int]:
        """
        Get player info

        Returns:
            A properly formatted dictionary with all the information necessary for the players
        """
        pass

    def get_annotations(self) -> Dict[str, str or int]:
        """
        Get annotation info

        Returns:
            A properly formatted dictionary with all the information necessary for annotations on permanents
        """
        pass

    def get_game_info(self) -> Dict[str, str or int]:
        """
        Gets game info

        Returns:
            A properly formatted dictionary with all the information necessary for information on the game
        """
        pass

    def clear(self) -> None:
        """
        Clears a gamestate back to its default value
        """
        pass

    def update(self, updated_state: 'GameStateSecondary') -> None:
        """
        Updates self to the updated state. If self does not contain an index that updated_state does then the index
        is added to state.
        """
        pass

    def diff(self, state: 'GameStateSecondary') -> Dict[str, str or int]:
        """
        Returns the difference between the two states in a new state object
        """
        pass
