import sys
sys.path.append("../src")

import unittest
from Dominion import player
from Dominion.card.cardlist import action_card
from Dominion.card.cardlist import victory_card
from Dominion.card.cardlist import money_card
from Dominion.card.cardlist import card
from Dominion.operation import deck_operation

plain_card = card.card("", "", "", 0, 0, 0, 0, "N")

class test_deckoperation(unittest.TestCase):
    def test_checktop(self):
        
        supply = []
        deck = [plain_card]
        deck2 = []
        hand = []
        play_area = []
        discard = []
        
        exp_deck = []
        exp_hand = [plain_card]
        exp_actionstack = 2
        exp_card = None
        
        act_card = deck_operation.check_top(deck2,discard)
        self.assertEqual(exp_card, act_card)
    
if __name__ == '__main__':
    unittest.main()
