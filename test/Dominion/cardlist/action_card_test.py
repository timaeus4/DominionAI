import sys
sys.path.append("..\src")

import unittest
from Dominion import player
from Dominion.card.cardlist import action_card
from Dominion.card.cardlist import victory_card
from Dominion.card.cardlist import money_card
from Dominion.card.cardlist import card

plain_card = card.card("", "", "", "", 0, 0, 0, 0, "N")

class test_village(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.village()
        
        supply = []
        t = player.Player()
        t.deck = [plain_card]
        t.hand = []
        t.play_area = []
        t.discard = []
        t.money_stack = 0
        t.buy_stack = 0
        trash = []
        action_stack = 0
        
        exp_deck = []
        exp_hand = [plain_card]
        exp_actionstack = 2
        
        _, act_t, _, _, act_actionstack = test_class.effect(supply, t, None, trash, action_stack)
        self.assertEqual(exp_deck, act_t.deck)
        self.assertEqual(exp_hand, act_t.hand)
        self.assertEqual(exp_actionstack,act_actionstack)
    
if __name__ == '__main__':
    unittest.main()
