from typing import Dict, List

from ControllerInterface import ControllerSecondary
from AIInterface import AIKernel
from MTGAController import Controller
from GameStateInterface import GameStateSecondary


class Game:
    class GameState(GameStateSecondary):
        def __init__(self, game_dict: [str, str or int]):
            self.game_dict = game_dict

        def __str__(self):
            return str(self.game_dict)

        def get_full_state(self) -> Dict[str, str or int]:
            return dict(self.game_dict)

        def get_turn_info(self) -> Dict[str, str or int]:
            return self.get_full_state()['turnInfo']

        def get_game_info(self) -> Dict[str, str or int]:
            return self.get_full_state()['turnInfo']

        def get_zone(self, zone_type: str, owner_seat_id: int = None) -> Dict[str, str or int]:
            zones = self.get_full_state()['zones']
            matching_zones = []
            zone_to_return = None
            for zone in zones:
                if zone['type'] == zone_type:
                    matching_zones.append(zone)
            if len(matching_zones) > 1:
                for zone in matching_zones:
                    if zone['ownerSeatId'] == owner_seat_id:
                        zone_to_return = zone
            elif len(matching_zones) == 1:
                zone_to_return = matching_zones[0]
            return zone_to_return

        def get_annotations(self) -> List[Dict]:
            return self.get_full_state()['annotations']

        def get_actions(self) -> List[Dict]:
            return self.get_full_state()['actions']

        def get_players(self) -> List[Dict]:
            return self.get_full_state()['players']

        def __update_dict(self, dict_to_update: [str, str or int], dict_with_update: [str, str or int]):
            for key in dict_with_update:
                if key in dict_to_update.keys():
                    item_to_update = dict_to_update[key]
                    item_with_update = dict_with_update[key]
                    if isinstance(item_with_update, dict):
                        if isinstance(item_to_update, dict):
                            self.__update_dict(item_to_update, item_with_update)
                        else:
                            temp_dict = {}
                            self.__update_dict(temp_dict, item_with_update)
                            dict_to_update[key] = temp_dict
                    elif isinstance(item_with_update, int) or isinstance(item_with_update, str) or isinstance(item_with_update, list):
                        dict_to_update[key] = dict_with_update[key]
                    else:
                        print("Uh oh something went wrong... :(")
                else:
                    dict_to_update[key] = dict_with_update[key]

        def update(self, updated_state: 'GameStateSecondary') -> None:
            self.__update_dict(self.game_dict, updated_state.get_full_state())

    def __init__(self, controller: ControllerSecondary, ai: AIKernel):
        self.ai = ai
        self.controller = controller

    def start(self):
        self.controller.start_game()
        while not self.controller.game_over():
            current_state = self.controller.get_game_state()
