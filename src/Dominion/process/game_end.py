from Dominion.process import play

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
    
    score += play.victory_effect(cardlist)
    
    return cardlist, score
    
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
