def count_point(deck, hand, discard):
    cardlist = []
    score = 0
    
    for card in deck:
        cardlist.append(card)
        score += card.victory_point
        
    for card in hand:
        cardlist.append(card)
        score += card.victory_point
    
    for card in discard:
        cardlist.append(card)
        score += card.victory_point

    score += count_gardens_point(cardlist)
    
    return cardlist, score

# 庭園の得点計算
def count_gardens_point(cardlist):
    gardens_num = 0
    for card in cardlist:
        if card.name=="gardens":
            gardens_num += 1
    
    gardens_point = len(cardlist) // 10
    return gardens_num * gardens_point

    
def province_judge(supply):
    for card in supply:
        if(card.name == "province"):
            if(card.num == 0):
                return True
            else:
                return False
                
def triple_judge(supply):
    count = 0
    for card in supply:
        if(card.num == 0):
            count += 1
    if(count >= 3):
        return True
    else:
        return False
        
def gameset_judge(supply):
    return province_judge(supply) or triple_judge(supply)

# not use    
def execute(agents):
    max_score = -100
    for agent in agents:
        cardlist, score = count_point(agent.deck, agent.hand, agent.discard)
        if (score > max_score):
            max_score = score
            win_cardlist = cardlist
            winner = agent
    return winner, cardlist, score
    
def is_win(target, players):
    _, score = count_point(target.deck, target.hand, target.discard)
    for player in players:
        if player.order != target.order:
            _, other_score = count_point(player.deck, player.hand, player.discard)
            if (other_score > score):
                return False
            if (other_score == score):
                if (player.turn < target.turn):
                    return False
    return True
    
def calc_behind_point(target, players):
    _, target_score = count_point(target.deck, target.hand, target.discard)
    
    pointlist = []
    for player in players:
        if player.order != target.order:
            _, other_score = count_point(player.deck, player.hand, player.discard)
            pointlist.append(target_score - other_score)
        
    return min(pointlist)
