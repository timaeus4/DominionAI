from Dominion.card.cardlist import card

# 財宝
class money_card(card.card):
    def __init__(self, name, japanese, cost, money_point, num, alter_flg):
        super(money_card, self).__init__(name, japanese, "money", cost, money_point, 0, num, alter_flg)

class bronze(money_card):
    def __init__(self):
        super(bronze, self).__init__("bronze", "銅貨", 0, 1, 32, "N")
    
class silver(money_card):
    def __init__(self):
        super(silver, self).__init__("silver", "銀貨", 3, 2, 40, "N")
    
class gold(money_card):
    def __init__(self):
        super(gold, self).__init__("gold", "金貨", 6, 3, 30, "N")