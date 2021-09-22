import requests

API_URL = 'https://api.scryfall.com/cards/arena/'


def get_card_info(mtga_id: int):
    """
    Parameters
        mtga_id: Must be a valid mtg arena id and
    Returns
        A dictionary object containing full info of the card that has the specified MTGA id
        Example output can be found here: https://api.scryfall.com/cards/arena/75519
    """
    card_response = requests.get(API_URL + str(mtga_id))
    return card_response.json()
