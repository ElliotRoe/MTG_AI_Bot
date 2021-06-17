from ControllerInterface import ControllerSecondary
from AIInterface import AIKernel
from MTGAController import Controller
from GameStateInterface import GameStateSecondary

class Game:
    class GameState(GameStateSecondary):
        def __init__(self):
            pass

    def __init__(self, controller: ControllerSecondary, ai: AIKernel):
        self.ai = ai
        self.controller = controller

    def start(self):
        self.controller.start_game()
        while not self.controller.game_over():
            current_state = self.controller.get_game_state()



