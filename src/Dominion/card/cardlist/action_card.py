from Dominion.card.cardlist import card, victory_card
from Dominion import strategy
from Dominion.operation import deck_operation
from Dominion.process import buy
import copy


# アクション
class action_card(card.card):
    def __init__(self, name, japanese, cost, priority, attack, reaction):
        super(action_card, self).__init__(name, japanese, "action", cost, 0, 0, 10)
        self.priority = priority
        self.attack = attack
        self.reaction = reaction
        
    def effect(self, supply, t, players, trash, action_stack):
        return supply, t, players, trash, action_stack
        
# 村
class village(action_card):
    def __init__(self):
        super(village, self).__init__("village", "村", 3, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        action_stack += 2
        
        return supply, t, players, trash, action_stack
        
        
# 鍛冶屋
class blacksmith(action_card):
    def __init__(self):
        super(blacksmith, self).__init__("blacksmith", "鍛冶屋", 4, 1, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(3):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        
        return supply, t, players, trash, action_stack
        
# 研究所
class laboratory(action_card):
    def __init__(self):
        super(laboratory, self).__init__("laboratory", "研究所", 5, 3, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(2):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        action_stack += 1
        
        return supply, t, players, trash, action_stack
        
# 地下貯蔵庫
class cellar(action_card):
    def __init__(self):
        super(cellar, self).__init__("cellar", "地下貯蔵庫", 2, 3, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        count = 0
        expect_money = self.calc_expect_money(t.deck, t.discard)
        for i in reversed(range(len(t.hand))):
            if(t.hand[i].name == "curse"):
                card = t.hand.pop(i)
                t.discard.append(card)
                count += 1
            elif(t.hand[i].name=="house") or (t.hand[i].name=="territory") or (t.hand[i].name=="province"):
                card = t.hand.pop(i)
                t.discard.append(card)
                count += 1
            elif(t.hand[i].name == "bronze"):
                if(expect_money > 1):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
            elif(t.hand[i].name == "silver"):
                if(expect_money > 2):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
            elif(t.hand[i].name == "gold"):
                if(expect_money > 3):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
            
                
        if count > 0:
            for i in range(count):
                t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        
        return supply, t, players, trash, action_stack
        
    def calc_expect_money(self,deck,discard):
        money= 0
        expect_money = 0
        for card in deck:
            money += card.money_point
        for card in discard:
            money += card.money_point
        return money / (len(deck) + len(discard))
        

# 礼拝堂
class chapel(action_card):
    def __init__(self):
        super(chapel, self).__init__("chapel", "礼拝堂", 2, 0, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        count = 0
        while(count < 4):
            for i in reversed(range(len(t.hand))):
                if(t.hand[i].name == "cursed"):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
                    break
            else:
                break
            
        while(count < 4):    
            for i in reversed(range(len(t.hand))):
                if(t.hand[i].name == "house"):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
                    break
            else:
                break
        
        while(count < 4):
            for i in reversed(range(len(t.hand))):
                if(t.hand[i].name == "bronze"):
                    card = t.hand.pop(i)
                    trash.append(card)
                    count += 1
                    break
            else:
                break
        
        return supply, t, players, trash, action_stack

# 堀
class moat(action_card):
    def __init__(self):
        super(moat, self).__init__("moat", "堀", 2, 1, False, True)

    def effect(self, supply, t, players, trash, action_stack):
        for i in range(2):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)

        return supply, t, players, trash, action_stack

# 工房
class workshop(action_card):
    def __init__(self):
        super(workshop, self).__init__("workshop", "工房", 3, 0, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        card = strategy.coin_method(4)
        _, t.discard = buy.buy(supply, 4, card, t.discard)
        
        return supply, t, players, trash, action_stack

# 改築
class remodel(action_card):
    def __init__(self):
        super(remodel, self).__init__("remodel", "改築", 4, 0, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        
        for i in supply:
            if i.name == "province":
                province = i
        
        for i in reversed(range(len(t.hand))):
            tmp_money = 0
            if(t.hand[i].name == "curse"):
                trash.append(t.hand.pop(i))
                tmp_money = 2
            elif(t.hand[i].name=="house"):
                trash.append(t.hand.pop(i))
                tmp_money = 4
            elif(t.hand[i].name == "bronze"):
                trash.append(t.hand.pop(i))
                tmp_money = 2
            elif(t.hand[i].name == "gold"):
                if(province.num <= 4):
                    trash.append(t.hand.pop(i))
                    tmp_money = 8
            if tmp_money!=0:
                card = strategy.coin_method(tmp_money)
                if card != None:
                    _, t.discard = buy.buy(supply, tmp_money, card, t.discard)
                break
                    
        return supply, t, players, trash, action_stack

# 金貸し
class money_lender(action_card):
    def __init__(self):
        super(money_lender, self).__init__("money_lender", "金貸し", 4, 0, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(len(t.hand)):
            if(t.hand[i].name == "bronze"):
                t.money_stack += 3
                card = t.hand.pop(i)
                trash.append(card)
                break
            
        return supply, t, players, trash, action_stack
        
# 玉座の間
class throne_room(action_card):
    def __init__(self):
        super(throne_room, self).__init__("throne_room", "玉座の間", 4, 3, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        priority = 3
        while(priority > 0):
            for i in range(len(t.hand)):
                if(t.hand[i].cardtype == "action"):
                    if(t.hand[i].priority == priority):
                        card = t.hand.pop(i)
                        t.play_area.append(card)
                        card.effect(supply, t, players, trash, action_stack) 
                        card.effect(supply, t, players, trash, action_stack) 
                        break
            else:
                priority -= 1
                continue
            break
            
        return supply, t, players, trash, action_stack

# 民兵
class militia(action_card):
    def __init__(self):
        super(militia, self).__init__("militia", "民兵", 4, 0, True, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        t.money_stack += 2
        
        for player in players:
            if player.order == (t.order+1)%4:
                left = player
            if player.order == (t.order+2)%4:
                center = player
            if player.order == (t.order+3)%4:
                right = player
                
        left = self.sub_effect(left)
        center = self.sub_effect(center)
        right = self.sub_effect(right)
        
        return supply, t, players, trash, action_stack
        
    def sub_effect(self, p):
        while len(p.hand) > 3:
            for i in range(len(p.hand)):
                if (p.hand[i].name=="cursed") or (p.hand[i].name=="house") or (p.hand[i].name=="territory") or (p.hand[i].name=="province"):
                    card = p.hand.pop(i)
                    p.discard.append(card)
                    break
            else:
                break
            
        while len(p.hand) > 3:
            for i in range(len(p.hand)):
                if (p.hand[i].name=="bronze"):
                    card = p.hand.pop(i)
                    p.discard.append(card)
                    break
            else:
                break
            
        while len(p.hand) > 3:
            for i in range(len(p.hand)):
                card = p.hand.pop(i)
                p.discard.append(card)
                break
                
        return p
        
# 役人
class bureaucrat(action_card):
    def __init__(self):
        super(bureaucrat, self).__init__("bureaucrat", "役人", 4, 0, True, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for card in supply:
            if(card.name == "silver"):
                if(card.num > 0):
                    t.deck.insert(0, card)
        
        for player in players:
            if player.order == (t.order+1)%4:
                left = player
            if player.order == (t.order+2)%4:
                center = player
            if player.order == (t.order+3)%4:
                right = player
                
        left = self.sub_effect(left)
        center = self.sub_effect(center)
        right = self.sub_effect(right)
        
        return supply, t, players, trash, action_stack
        
    def sub_effect(self, p):
        for i in range(len(p.hand)):
            if p.hand[i].victory_point > 0:
                card = p.hand.pop(i)
                p.deck.insert(0, card)
                break
        return p

# 市場
class market(action_card):
    def __init__(self):
        super(market, self).__init__("market", "市場", 5, 3, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(1):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        action_stack += 1
        t.money_stack += 1
        t.buy_stack += 1
        
        return supply, t, players, trash, action_stack

# 議事堂
class council_room(action_card):
    def __init__(self):
        super(council_room, self).__init__("council_room", "議事堂", 5, 1, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(4):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        
        for player in players:
            if player.order == (t.order+1)%4:
                left = player
            if player.order == (t.order+2)%4:
                center = player
            if player.order == (t.order+3)%4:
                right = player
        
        left.deck, left.hand, left.discard = deck_operation.draw(left.deck, left.hand, left.discard)
        center.deck, center.hand, center.discard = deck_operation.draw(center.deck, center.hand, center.discard)
        right.deck, right.hand, right.discard = deck_operation.draw(right.deck, right.hand, right.discard)
        
        return supply, t, players, trash, action_stack
    

# 鉱山（銅銀のみ対応）
class mine(action_card):
    def __init__(self):
        super(mine, self).__init__("mine", "鉱山", 5, 0, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(len(t.hand)):
            if(t.hand[i].name == "silver"):
                for card in supply:
                    if(card.name == "gold"):
                        if(card.num > 0):
                            silver = t.hand.pop(i)
                            trash.append(silver)
                            card.reduce(1)
                            t.hand.append(card)
                            return supply, t, players, trash, action_stack
                        else:
                            break
                else:
                    continue
                break
            
        for i in range(len(t.hand)):
            if(t.hand[i].name == "bronze"):
                for card in supply:
                    if(card.name == "silver"):
                        if(card.num > 0):
                            bronze = t.hand.pop(i)
                            trash.append(bronze)
                            card.reduce(1)
                            t.hand.append(card)
                            return supply, t, players, trash, action_stack
                        else:
                            break
                else:
                    continue
                break
            
        return supply, t, players, trash, action_stack

# 祝祭
class festival(action_card):
    def __init__(self):
        super(festival, self).__init__("festival", "祝祭", 5, 2, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        action_stack += 2
        t.money_stack += 2
        t.buy_stack += 1
        
        return supply, t, players, trash, action_stack
        
# 書庫
class archive(action_card):
    def __init__(self):
        super(archive, self).__init__("archive", "書庫", 5, 1, False, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        action_count = action_stack
        tmps = []
        while(len(t.hand) < 7):
            card = deck_operation.check_top(t.deck, t.hand, t.discard)
            if(card.cardtype != "action"):
                t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
            else:
                if action_stack <= 1:
                    tmps.append(t.deck.pop(0))
                else:
                    if card.priority > 1:
                        t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
                    else:
                        if action_count > 1:
                            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
                            action_count -= 1
                        else:
                            tmps.append(t.deck.pop(0))
               
        for tmp in tmps:
            t.discard.append(tmp)
         
        return supply, t, players, trash, action_stack
# 魔女
class witch(action_card):
    def __init__(self):
        super(witch, self).__init__("witch", "魔女", 5, 1, True, False)
        
    def effect(self, supply, t, players, trash, action_stack):
        for i in range(2):
            t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        
        for player in players:
            if player.order == (t.order+1)%4:
                left = player
            if player.order == (t.order+2)%4:
                center = player
            if player.order == (t.order+3)%4:
                right = player
        
        for card in supply:
            if card.name == "curse":
                curse = card
        if curse.num > 0:       
            left.discard.append(curse)
            curse.reduce(1)
        if curse.num > 0:       
            center.discard.append(curse)
            curse.reduce(1)
        if curse.num > 0:       
            right.discard.append(curse)
            curse.reduce(1)
        
        return supply, t, players, trash, action_stack

# 家臣
class vassal(action_card):
    def __init__(self):
        super(vassal, self).__init__("vassal", "家臣", 3, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        t.money_stack += 2
        card = deck_operation.check_top(t.deck, t.hand, t.discard)
        if(card.cardtype != "action"):
            t.discard.append(t.deck.pop(0))
        else:
            t.play_area.append(t.deck.pop(0))
            card.effect(supply, t, players, trash, action_stack)

        return supply, t, players, trash, action_stack

# 商人
class merchant(action_card):
    def __init__(self):
        super(merchant, self).__init__("merchant", "商人", 3, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        
        return supply, t, players, trash, action_stack


# 前駆者
class herbinger(action_card):
    def __init__(self):
        super(herbinger, self).__init__("herbinger", "前駆者", 3, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        
        return supply, t, players, trash, action_stack
    
# 密猟者
class poacher(action_card):
    def __init__(self):
        super(poacher, self).__init__("poacher", "密猟者", 4, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        t.deck, t.hand, t.discard = deck_operation.draw(t.deck, t.hand, t.discard)
        action_stack += 1
        t.money_stack += 1

        count = 0
        for card in supply:
          if(card.num == 0):
            count += 1

        while count > 0:
            for i in range(len(t.hand)):
                if (t.hand[i].name=="cursed") or (t.hand[i].name=="house") or (t.hand[i].name=="territory") or (t.hand[i].name=="province"):
                    card = t.hand.pop(i)
                    t.discard.append(card)
                    count -= 1
                    break
            else:
                break
            
        while count > 0:
            for i in range(len(t.hand)):
                if (t.hand[i].name=="bronze"):
                    card = t.hand.pop(i)
                    t.discard.append(card)
                    count -= 1
                    break
            else:
                break
            
        while count > 0:
            for i in range(len(t.hand)):
                card = t.hand.pop(i)
                t.discard.append(card)
                break
                
        return supply, t, players, trash, action_stack

# 衛兵
class stentry(action_card):
    def __init__(self):
        super(stentry, self).__init__("stentry", "衛兵", 5, 3, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        
        return supply, t, players, trash, action_stack

# 山賊
class bandit(action_card):
    def __init__(self):
        super(bandit, self).__init__("bandit", "山賊",5, 0, True, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        
        return supply, t, players, trash, action_stack

# 職人
class artisan(action_card):
    def __init__(self):
        super(artisan, self).__init__("artisan", "職人", 6, 0, False, False)
    
    def effect(self, supply, t, players, trash, action_stack):
        purchase = strategy.coin_method(5)
        for card in supply:
          if(card.name == purchase.name):
            if(card.num > 0):
                card.reduce(1)
                t.hand.append(purchase)

        if action_stack <= 1:
          for i in range(len(t.hand)):
            if t.hand[i].cardtype == "action":
              temp = t.hand.pop(i)
              t.deck.insert(0,temp)
              return supply, t, players, trash, action_stack
        
        for i in range(len(t.hand)):
         if t.hand[i].cardtype == "victory":
            temp = t.hand.pop(i)
            t.deck.insert(0,temp)
            return supply, t, players, trash, action_stack
        
        temp = t.hand.pop(0)
        t.deck.insert(0,temp)
        return supply, t, players, trash, action_stack