import json
import time

from ControllerInterface import ControllerSecondary
from MTGAController.LogReader import LogReader
from pynput import mouse


class Controller(ControllerSecondary):
    def __init__(self, screen_bounds=((0, 0), (1600, 900))):
        self.screen_bounds = screen_bounds
        self.patterns = {'game_state': '"type": "GREMessageType_GameStateMessage"', 'hover_id': 'objectId'}
        self.log_reader = LogReader(self.patterns.values())
        self.mouse_controller = mouse.ControllerSecondary()
        self.cast_speed = 0.001
        self.cast_card_dist = 10

    def start_game(self) -> None:
        self.log_reader.start_log_monitor()

        # TODO: Add mouse movement to press the play button

    def end_game(self) -> None:
        self.log_reader.stop_log_monitor()

    def cast(self, card_id: int) -> None:
        self.mouse_controller.position = (self.screen_bounds[0][0], self.screen_bounds[1][1] + 30)
        i = 0
        while i < 7:
            while not self.log_reader.has_new_line(self.patterns['hover_id']) and self.mouse_controller.position[0] < \
                    self.screen_bounds[1][0] - 10:
                self.mouse_controller.move(self.cast_card_dist, 0)
                time.sleep(self.cast_speed)
            print("ID Hovered " + str(self.log_reader.get_latest_line_containing_pattern(self.patterns['hover_id'])))
            i += 1
