from AIInterface import AIKernel
from ControllerInterface import ControllerSecondary
from GameState import GameState


class DummyAI(AIKernel):

    def generate_keep(self, card_list) -> bool:
        return True

    def generate_move(self, game_state: GameState):
        move = {'resolve': []}
        action_list = game_state.get_actions()
        if len(action_list) > 0:
            turn_info = game_state.get_turn_info()
            if turn_info['activePlayer'] == 1 and turn_info['decisionPlayer'] == 1 and turn_info['priorityPlayer'] == 1:
                if turn_info['phase'] == 'Phase_Combat' and turn_info['step'] == 'Step_DeclareAttack':
                    move = {'all_attack': []}
                elif turn_info['phase'] == 'Phase_Main1' or turn_info['phase'] == 'Phase_Main2':
                    for action_wrapper in action_list:
                        action = action_wrapper['action']
                        if action['actionType'] == 'ActionType_Play':
                            move = {'cast': [action['instanceId']]}
                            break
        return move
