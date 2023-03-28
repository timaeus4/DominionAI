class card():
    def __init__(self, name, cardtype, cost, money_point, victory_point, num):
        self.name = name
        self.cardtype = cardtype
        self.cost = cost
        self.money_point = money_point
        self.victory_point = victory_point
        self.num = num
        
    def reduce(self, n):
        self.num -= n