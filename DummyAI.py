from AIInterface import AIKernel
from ControllerInterface import ControllerSecondary
from Game import Game

class DummyAI(AIKernel):

    def __init__(self, controller: ControllerSecondary):

        self.controller = controller

    def generate_move(self, game_state: Game.GameState):
        action_list = game_state.get_actions()
        if len(action_list) > 0:
            turn_info = game_state.get_turn_info()
            if turn_info['activePlayer'] == 1 and turn_info['decisionPlayer'] == 1 and turn_info['priorityPlayer'] == 1:
                if turn_info['phase'] == 'Phase_Combat' and turn_info['step'] == 'Step_DeclareAttack':
                    self.controller.all_attack()
                    return
                elif turn_info['phase'] == 'Phase_Main1' or turn_info['phase'] == 'Phase_Main2':
                    for action in action_list:
                        if action['actionType'] == 'ActionType_Cast':
                            self.controller.cast(action['grpId'])
                            return
        self.controller.resolve()
