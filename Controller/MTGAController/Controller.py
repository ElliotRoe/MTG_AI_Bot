import json
import threading
import time

from pynput.mouse import Button

from Controller.ControllerInterface import ControllerSecondary
from Controller.MTGAController.LogReader import LogReader
from pynput import mouse
from pynput import keyboard
from Controller.Utilities.GameState import GameState


class Controller(ControllerSecondary):

    def __init__(self, log_path, screen_bounds=((0, 0), (1600, 900))):
        self.__decision_callback = None
        self.__mulligan_decision_callback = None
        self.__current_execution_thread = None
        self.__has_mulled_keep = False
        self.__intro_delay = 15
        self.__decision_delay = 4
        self.screen_bounds = screen_bounds
        self.patterns = {'game_state': '"type": "GREMessageType_GameStateMessage"', 'hover_id': 'objectId'}
        self.log_reader = LogReader(self.patterns.values(), log_path=log_path, callback=self.__log_callback)
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.cast_speed = 0.01
        # Height of the mouse when cards are scanned for casting
        self.cast_height = 30
        # Offset of the resolve button from the bottom right
        self.main_br_button_offset = (165, 136)
        self.mulligan_keep_coors = (1101, 870)
        self.mulligan_mull_coors = (801, 870)
        self.player_button_coors = (1699, 996)
        self.home_play_button_coors = (1699, 996)
        self.cast_card_dist = 10
        self.main_br_button_coordinates = (
            self.screen_bounds[1][0] - self.main_br_button_offset[0],
            self.screen_bounds[1][1] - self.main_br_button_offset[1],
        )
        self.updated_game_state = GameState()
        self.__inst_id_grp_id_dict = {}

    def start_game_from_home_screen(self):
        self.mouse_controller.position = self.home_play_button_coors
        self.mouse_controller.press(Button.left)
        time.sleep(0.2)
        self.mouse_controller.release(Button.left)
        time.sleep(1)
        self.mouse_controller.press(Button.left)
        time.sleep(0.2)
        self.mouse_controller.release(Button.left)

    def start_monitor(self) -> None:
        self.log_reader.start_log_monitor()

    def start_game(self) -> None:
        self.start_monitor()
        self.start_game_from_home_screen()

    def set_decision_callback(self, method) -> None:
        self.__decision_callback = method

    def set_mulligan_decision_callback(self, method) -> None:
        self.__mulligan_decision_callback = method

    def end_game(self) -> None:
        self.log_reader.stop_log_monitor()

    def cast(self, card_id: int) -> None:
        time.sleep(1)
        self.mouse_controller.position = (self.screen_bounds[0][0], self.screen_bounds[1][1] + self.cast_height)
        current_hovered_id = None
        while current_hovered_id != card_id:
            while not self.log_reader.has_new_line(self.patterns['hover_id']):
                self.mouse_controller.move(self.cast_card_dist, 0)
                time.sleep(self.cast_speed)
            current_hovered_id = self.__parse_object_id_line(self.log_reader.get_latest_line_containing_pattern(
                self.patterns['hover_id']))
            print(str(current_hovered_id) + '|' + str(card_id))
        time.sleep(1)
        self.mouse_controller.click(Button.left, 1)
        time.sleep(0.1)
        self.mouse_controller.click(Button.left, 1)

    def all_attack(self) -> None:
        self.mouse_controller.position = self.main_br_button_coordinates
        self.mouse_controller.click(Button.left, 1)
        time.sleep(1)
        self.mouse_controller.click(Button.left, 1)

    def resolve(self) -> None:
        if self.updated_game_state.get_turn_info()['step'] != 'Step_DeclareAttack' \
                or self.updated_game_state.get_turn_info()['activePlayer'] == 2:
            self.mouse_controller.position = self.main_br_button_coordinates
        else:
            self.mouse_controller.position = (
                self.main_br_button_coordinates[0],
                self.main_br_button_coordinates[1] - 50,
            )
        self.mouse_controller.click(Button.left, 1)

    def auto_pass(self) -> None:
        self.keyboard_controller.press(keyboard.Key.enter)
        time.sleep(0.4)
        self.keyboard_controller.release(keyboard.Key.enter)

    def unconditional_auto_pass(self) -> None:
        self.keyboard_controller.press(keyboard.Key.shift)
        self.keyboard_controller.press(keyboard.Key.enter)
        time.sleep(0.4)
        self.keyboard_controller.release(keyboard.Key.shift)
        self.keyboard_controller.release(keyboard.Key.enter)

    def get_game_state(self) -> 'GameStateSecondary':
        return self.updated_game_state

    def keep(self, keep: bool):
        if keep:
            self.mouse_controller.position = self.mulligan_keep_coors
        else:
            self.mouse_controller.position = self.mulligan_mull_coors
        self.mouse_controller.click(Button.left)

    def get_grp_id(self, inst_id):
        return self.__inst_id_grp_id_dict[inst_id]

    @staticmethod
    def __parse_object_id_line(line):
        number_string = ""
        i = 0
        while i < len(line):
            if line[i].isnumeric():
                number_string = number_string + line[i]
            i = i + 1
        return int(number_string)

    def __log_callback(self, pattern: str, line_containing_pattern: str):
        if pattern == self.patterns["game_state"]:
            self.__update_game_state(json.loads(line_containing_pattern))

    def __update_inst_id__grp_id_dict(self, object_dict_arr):
        for object_dict in object_dict_arr:
            if object_dict['instanceId'] not in self.__inst_id_grp_id_dict.keys():
                self.__inst_id_grp_id_dict[object_dict['instanceId']] = object_dict['grpId']

    def __update_game_state(self, raw_dict: [str, str or int]):
        game_state = Controller.__get_game_state_from_raw_dict(raw_dict)
        self.updated_game_state.update(game_state)
        print(self.updated_game_state)
        turn_info_dict = self.updated_game_state.get_turn_info()
        if self.updated_game_state.is_complete():
            self.__update_inst_id__grp_id_dict(self.updated_game_state.get_game_objects())
            if turn_info_dict['decisionPlayer'] == 1 and self.__has_mulled_keep:
                self.__current_execution_thread = threading.Timer(self.__decision_delay,
                                                                  lambda:
                                                                  self.__decision_callback(self.updated_game_state))
                self.__current_execution_thread.start()
            elif not self.__has_mulled_keep:
                self.__current_execution_thread = threading.Timer(self.__intro_delay,
                                                                  lambda:
                                                                  self.__mulligan_decision_callback([]))
                self.__current_execution_thread.start()
                self.__has_mulled_keep = True

    @staticmethod
    def __get_game_state_from_raw_dict(raw_dict: [str, str or int]):
        temp_dict = raw_dict['greToClientEvent']
        temp_arr = temp_dict['greToClientMessages']
        return_game_state = GameState({})
        for message in temp_arr:
            if message['type'] == "GREMessageType_GameStateMessage":
                raw_game_state_dict = message['gameStateMessage']
                game_state_dict = {}
                for key in GameState.GAME_STATE_KEYS:
                    if key in raw_game_state_dict:
                        game_state_dict[key] = raw_game_state_dict[key]
                generated_game_state = GameState(game_state_dict)
                return_game_state.update(generated_game_state)
        return return_game_state
