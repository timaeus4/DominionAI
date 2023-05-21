# 学習用拡張クラス

import numpy as np
from Dominion import dominion
from Dominion.process import game_start
from Dominion.process import game_end
from Dominion.process import buy
from Dominion.process import play
from Dominion.process import clean_up


class Dominion_forTrain(dominion.Dominion):
    
    def __init__(self, ver_name):
        super(Dominion_forTrain, self).__init__(ver_name)
        
    def execute_action(self, target, players):
        self.supply, target, players, self.trash = play.execute(self.supply, target, players, self.trash)
        return target, players
    
    def execute_buy(self, player, purchase):
        self.supply, player, self.trash = play.buy_effect(self.supply, player, self.trash)
        money = player.count_money()
        player = buy.execute(self.supply, player, money, purchase)
        return player
        
    def execute_cleanup(self, player):
        player = clean_up.execute(player)
        player.turn += 1
        return player
        
    def check_gameset(self):
        return game_end.gameset_judge(self.supply)
        
    def is_win(self, player, others):
        return game_end.is_win(player, others)
