from AIInterface import AIKernel
from ControllerInterface import ControllerSecondary
from GameState import GameState


class DummyAI(AIKernel):

    def __init__(self):
        self.__current_turn_num = 0
        self.__has_land_been_played_this_turn = False
        self.__total_mana = {"red": 0, "green": 0, "blue": 0, "black": 0, "white": 0, "generic": 0}
        self.__avail_mana = {"red": 0, "green": 0, "blue": 0, "black": 0, "white": 0, "generic": 0}

    def generate_keep(self, card_list) -> bool:
        return True

    def __reset_mana(self):
        for key in self.__avail_mana:
            self.__avail_mana[key] = self.__total_mana[key]

    def __convert_raw_mana_cost_arr_to_standard(self, mana_cost_arr):
        """
        Converts a raw mana cost dict to a standard one

        Raw array
        [
          {
            "color": [
              "ManaColor_" + colorName
            ],
            "count": int
          },
          ...
        ]

        Standard dict
        {
            "red": int,
            "green": int,
            "blue": int,
            "black": int,
            "white": int,
            "generic": int
        }

        Returns:
             Standard dict representing the mana cost
        """
        reformatted_mana_cost_dict = {}
        for color_dict in mana_cost_arr:
            key = color_dict['color'][11:].lower()
            reformatted_mana_cost_dict[key] = color_dict['count']
        return reformatted_mana_cost_dict

    def __use_mana(self, stand_mana_cost_dict):
        """
        Updates self.__avail_mana with the appropriate mana
        Requires:
            Already have enough mana to use that mana
        Parameters:
            stand_mana_cost_dict: mana to be taken away from available mana
        """
        for key in stand_mana_cost_dict.keys():
            if key != 'generic':
                self.__avail_mana[key] -= stand_mana_cost_dict[key]
        if self.__avail_mana['generic'] <= stand_mana_cost_dict['generic']:
            stand_mana_cost_dict['generic'] -= self.__avail_mana['generic']
            self.__avail_mana['generic'] = 0
            for key in stand_mana_cost_dict.keys():
                if self.__avail_mana[key] <= stand_mana_cost_dict['generic']:
                    stand_mana_cost_dict['generic'] -= self.__avail_mana[key]
                    self.__avail_mana[key] = 0
                else:
                    self.__avail_mana[key] -= stand_mana_cost_dict['generic']
                    stand_mana_cost_dict['generic'] = 0
                if stand_mana_cost_dict['generic'] == 0:
                    break
        else:
            self.__avail_mana['generic'] -= stand_mana_cost_dict['generic']


    def __has_mana(self, mana_cost_arr):
        """
        Requires:
            mana_cost_dict must be of raw form
        """
        has_mana = True
        total_generic_count = 0
        reformatted_mana_cost_dict = self.__convert_raw_mana_cost_arr_to_standard(mana_cost_arr)
        for color in reformatted_mana_cost_dict.keys():
            total_generic_count += self.__avail_mana[color]
            if color != 'generic':
                total_generic_count -= reformatted_mana_cost_dict[color]
                if reformatted_mana_cost_dict[color] > self.__avail_mana[color]:
                    has_mana = False
        if total_generic_count < reformatted_mana_cost_dict['generic']:
            has_mana = False
        return has_mana

    def __new_turn_check(self, current_game_state: 'GameState'):
        turn_info = current_game_state.get_turn_info()
        new_turn_num = turn_info['turnNumber']
        if self.__current_turn_num < new_turn_num:
            self.__current_turn_num = new_turn_num
            self.__has_land_been_played_this_turn = False
            self.__reset_mana()

    def generate_move(self, game_state: GameState):
        move = {'resolve': []}
        self.__new_turn_check(game_state)
        turn_info = game_state.get_turn_info()
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
                            self.__total_mana['red'] += 1
                            self.__avail_mana['red'] += 1
                            break
                        elif action['actionType'] == 'ActionType_Cast' and self.__has_mana(action['manaCost']):
                            move = {'cast': [action['instanceId']]}
                            self.__use_mana(action['manaCost'])
                            break
        return move
