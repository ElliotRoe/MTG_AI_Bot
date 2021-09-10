from AIInterface import AIKernel
from ControllerInterface import ControllerSecondary
from GameState import GameState


class DummyAI(AIKernel):

    def __init__(self):
        self.__current_turn_num = 0
        self.__has_land_been_played_this_turn = False

    def generate_keep(self, card_list) -> bool:
        return True

    def generate_move(self, game_state: GameState):
        move = {'resolve': []}
        turn_info = game_state.get_turn_info()
        new_turn_num = turn_info['turnNumber']
        if self.__current_turn_num < new_turn_num:
            self.__current_turn_num = new_turn_num
            self.__has_land_been_played_this_turn = False
        action_list = game_state.get_actions()
        if len(action_list) > 0:
            if turn_info['activePlayer'] == 1 and turn_info['decisionPlayer'] == 1 and turn_info['priorityPlayer'] == 1:
                if turn_info['phase'] == 'Phase_Combat' and turn_info['step'] == 'Step_DeclareAttack':
                    move = {'all_attack': []}
                elif turn_info['phase'] == 'Phase_Main1' or turn_info['phase'] == 'Phase_Main2':
                    for action_wrapper in action_list:
                        action = action_wrapper['action']
                        if action['actionType'] == 'ActionType_Play' and not self.__has_land_been_played_this_turn:
                            move = {'cast': [action['instanceId']]}
                            self.__has_land_been_played_this_turn = True
                            break
        return move
