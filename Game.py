from ControllerInterface import Controller
from MTGAController import MTGAController


class Game:
    def __init__(self, controller: Controller = MTGAController()):
        controller.start_game()
        while not controller.game_over():
            current_state = controller.get_game_state()



