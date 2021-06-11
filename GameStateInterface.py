class GameStateKernel:
    """
    Informal Interface
    Defines methods for the GameState type
    """

    def get_full_state(self) -> dict[str, str]:
        """
        Returns:
             a dictionary object with the game state fully constructed like a JSON object
        """
        pass


class GameState:
    """
    Informal Interface
    Defines secondary methods for the GameState type
    """

    def get_zone(self, zone_type: str, owner_seat_id: int = None) -> dict[str, str]:
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
