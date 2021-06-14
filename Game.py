from ControllerInterface import ControllerSecondary
from MTGAController import Controller


class MTGGame:
    class GameState:
        def __init__(self, permanent_id_array, attributes_array, player_hand_ids, opponent_hand_ids, player_life, 
                     opponent_life, stack_ids, other_zone_ids, turn_phase, turn):
            self.turn = turn
            self.turn_phase = turn_phase
            self.other_zone_ids = other_zone_ids
            self.stack_ids = stack_ids
            self.opponent_life = opponent_life
            self.player_life = player_life
            self.opponent_hand_ids = opponent_hand_ids
            self.player_hand_ids = player_hand_ids
            self.attributes_array = attributes_array
            self.permanent_id_array = permanent_id_array

    def __init__(self, controller: Controller = Controller()):
        controller.start_game()
        while not controller.game_over():
            current_state = controller.get_game_state()



