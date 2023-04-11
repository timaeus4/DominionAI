from Dominion.card.cardlist import card

# 財宝
class money_card(card.card):
    def __init__(self, name, cost, money_point, num):
        super(money_card, self).__init__(name, "money", cost, money_point, 0, num)

class bronze(money_card):
    def __init__(self):
        super(bronze, self).__init__("bronze", 0, 1, 32)
    
class silver(money_card):
    def __init__(self):
        super(silver, self).__init__("silver", 3, 2, 40)
    
class gold(money_card):
    def __init__(self):
        super(gold, self).__init__("gold", 6, 3, 30)