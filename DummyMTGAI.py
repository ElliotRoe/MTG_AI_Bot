from MTGAIInterface import MTGAI
from MTGGame import MTGGame

class DummyMTGAI(MTGAI):
    def generate_move(self, game_state: MTGGame.GameState):
        move = 'pass'
        if game_state.turn == 'player':
            if game_state.turn_phase == 'declare_attackers_step':
                move = 'all_attack'
            elif game_state.turn_phase == 'main_phase':
