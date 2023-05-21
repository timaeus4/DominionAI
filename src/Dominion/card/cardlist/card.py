class card():
    def __init__(self, name, japanese, cardtype, cost, money_point, victory_point, num, alter_flg):
        self.name = name
        self.japanese = japanese
        self.cardtype = cardtype
        self.cost = cost
        self.money_point = money_point
        self.victory_point = victory_point
        self.num = num
        # 追加効果フラグ
        # N: なし
        # A: アタック
        # R: リアクション
        # B: 購入直前
        # V: 勝利点計算
        self.alter_flg = alter_flg
        
    def reduce(self, n):
        self.num -= n