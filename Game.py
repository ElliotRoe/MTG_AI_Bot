from typing import Dict

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
            return self.game_dict

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
