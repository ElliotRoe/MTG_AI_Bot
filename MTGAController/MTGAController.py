from ControllerInterface import Controller
from MTGALogReader import MTGALogReader


class MTGAController(Controller):
    def __init__(self):
        self.patterns = ['"type": "GREMessageType_GameStateMessage"', 'PregameSequence end']
        self.log_reader = MTGALogReader(self.patterns)

    def start_game(self) -> None:
        self.log_reader.start_log_monitor()

        # TODO: Add mouse movement to press the play button



