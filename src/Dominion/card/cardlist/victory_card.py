from Dominion.card.cardlist import card

# 勝利点
class victory_card(card.card):
    def __init__(self, name, japanese, cost, victory_point):
        super(victory_card, self).__init__(name, japanese, "victory", cost, 0, victory_point, 12)
        
class house(victory_card):
    def __init__(self):
        super(house, self).__init__("house", "屋敷", 2, 1)
    
class territory(victory_card):
    def __init__(self):
        super(territory, self).__init__("territory", "公領", 5, 3)
    
class province(victory_card):
    def __init__(self):
        super(province, self).__init__("province", "属州", 8, 6)

# 庭園
class gardens(victory_card):
    def __init__(self):
        super(gardens, self).__init__("gardens", "庭園", 4, 0)
        
class curse(card.card):
    def __init__(self):
        super(curse, self).__init__("curse", "curse", "呪い", 0, 0, -1, 30)