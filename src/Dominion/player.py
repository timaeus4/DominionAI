from Dominion.process import game_start

class Player():
    def __init__(self):
        pass
        
    def setup(self, n):
        self.deck = []
        self.hand = []
        self.discard = []
        self.money_stack = 0
        self.buy_stack = 1
        self.play_area = []
        self.turn = 0
        self.buy_history = []
        self.order = n
        
        self.deck, self.hand, self.discard = game_start.setup_personal_info()
    
    # プレイヤーが持っている全カードの情報    
    def get_allcard(self):
        allcard = []
        
        allcard.extend(self.deck)
        allcard.extend(self.hand)
        allcard.extend(self.discard)
        allcard.extend(self.play_area)
        
        return allcard
    
    # 金スタックと手札の財宝を足し算    
    def count_money(self):
        money = 0
    
        for card in self.hand:
            money += card.money_point
        
        return money + self.money_stack