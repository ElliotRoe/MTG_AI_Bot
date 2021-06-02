from ControllerInterface import Controller
from MTGAController import MTGAController


class MTGGame:
    class GameState:
        def __init__(self, permanent_id_array, ):
            self.permanent_id_array = permanent_id_array

    def __init__(self, controller: Controller = MTGAController()):
        controller.start_game()
        while not controller.game_over():
            current_state = controller.get_game_state()



