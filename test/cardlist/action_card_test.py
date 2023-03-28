import unittest
from cardlist import action_card
from cardlist import victory_card
from cardlist import money_card
from cardlist import card

plain_card = card.card("", "", 0, 0, 0, 0)

class test_village(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.village()
        
        supply = []
        deck = [plain_card]
        hand = []
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_deck = []
        expected_hand = [plain_card]
        expected_actionstack = 2
        
        _,act_deck,act_hand,_,_,_,act_actionstack,_,_ = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_deck,act_deck)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)

class test_blacksmith(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.blacksmith()
        
        supply = []
        deck = [plain_card,plain_card,plain_card]
        hand = []
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_deck = []
        expected_hand = [plain_card,plain_card,plain_card]
        expected_actionstack = 0
        
        _,act_deck,act_hand,_,_,_,act_actionstack,_,_ = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_deck,act_deck)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)
        
class test_laboratory(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.laboratory()
        
        supply = []
        deck = [plain_card,plain_card]
        hand = []
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_deck = []
        expected_hand = [plain_card,plain_card]
        expected_actionstack = 1
        
        _,act_deck,act_hand,_,_,_,act_actionstack,_,_ = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_deck,act_deck)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)
        
class test_chapel(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.chapel()
        
        card_house = victory_card.house()
        card_cursed = victory_card.cursed()
        card_bronze = money_card.bronze()
        
        supply = []
        deck = []
        hand = [plain_card,card_house,card_cursed,card_bronze]
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_deck = []
        expected_hand = [plain_card]
        expected_trash = [card_cursed,card_house,card_bronze]
        expected_actionstack = 0
        
        _,act_deck,act_hand,_,_,act_trash,act_actionstack,_,_ = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_deck,act_deck)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)
        self.assertEqual(expected_trash,act_trash)
        
class test_market(unittest.TestCase):
    def test_effect(self):
        test_class=action_card.market()
        
        supply = []
        deck = [plain_card,plain_card]
        hand = []
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_deck = [plain_card]
        expected_hand = [plain_card]
        expected_actionstack = 1
        expected_moneystack = 1
        expected_buystack = 1
        
        _,act_deck,act_hand,_,_,_,act_actionstack,act_moneystack,act_buystack = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_deck,act_deck)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)
        self.assertEqual(expected_moneystack,act_moneystack)
        self.assertEqual(expected_buystack,act_buystack)
    
class test_mine(unittest.TestCase):
    def test_effect(self):    
        test_class=action_card.mine()
        
        card_bronze = money_card.bronze()
        card_silver = money_card.silver()
        card_gold = money_card.gold()
        
        supply = [card_bronze,card_silver,card_gold]
        deck = []
        hand = [plain_card,card_bronze,card_silver]
        play_area = []
        discard = []
        trash = []
        action_stack = 0
        money_stack = 0
        buy_stack = 0
        
        expected_hand = [plain_card,card_bronze,card_gold]
        expected_actionstack = 0
        expected_trash = [card_silver]
        
        _,_,act_hand,_,_,act_trash,act_actionstack,_,_ = test_class.effect(supply,deck,hand,play_area,discard,trash,action_stack,money_stack,buy_stack)
        self.assertEqual(expected_hand,act_hand)
        self.assertEqual(expected_actionstack,act_actionstack)
        self.assertEqual(expected_trash,act_trash)
    
if __name__ == '__main__':
    unittest.main()
