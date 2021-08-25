import json
import time

from pynput.mouse import Button

from ControllerInterface import ControllerSecondary
from MTGAController.LogReader import LogReader
from pynput import mouse


class Controller(ControllerSecondary):

    def __init__(self, log_path, screen_bounds=((0, 0), (1600, 900))):
        self.screen_bounds = screen_bounds
        self.patterns = {'game_state': '"type": "GREMessageType_GameStateMessage"', 'hover_id': 'objectId'}
        self.log_reader = LogReader(self.patterns.values(), log_path=log_path)
        self.mouse_controller = mouse.Controller()
        self.cast_speed = 0.001
        self.cast_card_dist = 10
        self.all_attack_coordinates = (screen_bounds[1][0]-20, screen_bounds[1][0]-50)

    def start_game(self) -> None:
        self.log_reader.start_log_monitor()

        # TODO: Add mouse movement to press the play button

    def end_game(self) -> None:
        self.log_reader.stop_log_monitor()

    @staticmethod
    def __parse_object_id_line(self, line):
        number_string = ""
        i = 0
        while i < len(line):
            if line[i].isnumeric():
                number_string = number_string + line[i]
            i = i + 1
        return int(number_string)

    def cast(self, card_id: int) -> None:
        self.mouse_controller.position = (self.screen_bounds[0][0], self.screen_bounds[1][1] + 30)
        current_hovered_id = None
        while current_hovered_id != card_id:
            while not self.log_reader.has_new_line(self.patterns['hover_id']):
                self.mouse_controller.move(self.cast_card_dist, 0)
                time.sleep(self.cast_speed)
            current_hovered_id = self.__parse_object_id_line(self.log_reader.get_latest_line_containing_pattern(
                self.patterns['hover_id']))

        self.mouse_controller.press(Button.left)
        self.mouse_controller.move(-50, 100)
        self.mouse_controller.release(Button.left)

    def all_attack(self) -> None:
        self.mouse_controller.position = self.all_attack_coordinates()
        self.mouse_controller.click(Button.left, 1)
        time.sleep(1)
        self.mouse_controller.click(Button.left, 1)
