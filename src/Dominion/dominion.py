import numpy as np
from Dominion.process import game_start
from Dominion.card import card_factory as CF

class Dominion():
    
    def __init__(self, ver_name):
        # バージョン毎の全カードリスト、全カード数
        self.all_cardlist, self.version_card_num = CF.make_cardlist_for_version(ver_name)
        self.all_cardlist = game_start.sort_by_cost(self.all_cardlist)
    
    # 初期設定
    def setup(self, random_supply):
        self.supply = []
        self.trash = []
        
        self.supply = game_start.set_common_supply(self.supply)
        for card in random_supply:
            self.supply.append(card)
        self.supply = game_start.sort_by_cost(self.supply)

        self.current_numlist = self.get_current_numlist()
    
    # サプライランダム生成        
    def generate_random_supply(self, version, max):
        return game_start.set_random_supply(version, max)
        
    # 指定したコスト以下のサプライ数
    def count_supply(self, i):
        count = 0
        for card in self.supply:
            if(card.cost <= i):
                count += 1
        return count
        
    # Tensor型 -> card型への変換
    def int2allcard(self, i):
        if (i==0):
            return None
        else:
            return self.all_cardlist[i-1]
    
    # card型 -> Tensor型への変換
    def allcard2int(self, c):
        if c==None:
            return 0
        else:
            for i in range(len(self.all_cardlist)):
                if c.name == self.all_cardlist[i].name:
                    return i+1
    
    # 状態取得
    def get_state(self, allcard):
        # カードごとに列を割り当て、持っている枚数分カウントアップ
        state = np.zeros(len(self.all_cardlist))
        for card in allcard:
            for i in range(len(self.all_cardlist)):
                if card.name == self.all_cardlist[i].name:
                    state[i] += 1
                    
        return state
    
    # 全リストから今回のランダムサプライ番号を取得
    def get_current_numlist(self):
        numlist = []
        for card in self.supply:
            for i in range(len(self.all_cardlist)):
                if card.name == self.all_cardlist[i].name:
                    numlist.append(i)
        return numlist
    
    # サプライ番号リストからmoneyで絞り込み
    def get_numlist_for_money(self, money):
        numlist = []
        for i in range(self.count_supply(money)):
            numlist.append(self.current_numlist[i])
        return numlist

    # サプライ番号リストからmoneyで絞り込み
    def get_numlist_for_just_money(self, money):
        if money < 0:
            return None
        numlist = []
        for i in range(len(self.supply)):
            if self.supply[i].cost == money:
                numlist.append(self.current_numlist[i])
        if numlist == []:
            numlist = self.get_numlist_for_just_money(money-1)
        return numlist



