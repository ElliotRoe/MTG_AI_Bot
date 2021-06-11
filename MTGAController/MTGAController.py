import json

from ControllerInterface import Controller
from MTGALogReader import MTGALogReader


class MTGAController(Controller):
    def __init__(self):
        self.patterns = {'game_state': '"type": "GREMessageType_GameStateMessage"', 'start': 'PregameSequence end'}
        self.log_reader = MTGALogReader(self.patterns.items())

    def start_game(self) -> None:
        self.log_reader.start_log_monitor()

        # TODO: Add mouse movement to press the play button

    def get_game_state_pretty(self):
        game_state_string = self.log_reader.get_latest_line_containing_pattern(self.patterns['game_state'])
        game_state_dic = json.loads(game_state_string)
        player_life_total = game_state_dic["greToClientEvent"]["greToClientMessages"][0]["gameStateMessage"]["players"][0]["lifeTotal"]

