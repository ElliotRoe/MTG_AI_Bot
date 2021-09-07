from ControllerInterface import ControllerSecondary
from AIInterface import AIKernel
from GameState import GameState


class Game:

    def __init__(self, controller: ControllerSecondary, ai: AIKernel):
        self.ai = ai
        self.controller = controller

    def start(self):
        self.controller.start_game()
        self.controller.set_decision_callback(self.decision_method)

    def decision_method(self, current_game_state: GameState):
        move = self.ai.generate_move(current_game_state)
        print(move)
        move_name = move.keys()[0]
        if move_name == 'attack':
            self.controller.attack(move[move_name][0])
        elif move_name == 'all_attack':
            self.controller.all_attack()
        elif move_name == 'cast':
            self.controller.cast(move[move_name][0])
        elif move_name == 'block':
            self.controller.block(move[move_name][0], move[move_name][1])
        elif move_name == 'select_target':
            self.controller.select_target(move[move_name][0])
        elif move_name == 'activate_ability':
            self.controller.activate_ability(move[move_name][0], move[move_name][1])
        elif move_name == 'resolve':
            self.controller.resolve()
        elif move_name == 'auto_pass':
            self.controller.auto_pass()
        elif move_name == 'unconditional_auto_pass':
            self.controller.unconditional_auto_pass()
        elif move_name == 'all_block':
            self.controller.all_block()
        else:
            print("Move that was generated was not valid... This should never be reached")
