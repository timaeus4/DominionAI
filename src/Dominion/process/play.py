# プレイするアクションカードを選択
def select_card_to_use(hand):
    priority = 3
    # Todo: ラストアクションの優先度の処理
    while(priority >= 0):
        for i in range(len(hand)):
            if(hand[i].cardtype == "action"):
                if(hand[i].priority == priority):
                    card = hand.pop(i)
                    return hand, card
        priority -= 1
    
    card = None
    
    return hand, card

def execute(supply, target, players, trash):
    # アクション権
    action_stack = 1
    
    while(action_stack > 0):
        target.hand, card = select_card_to_use(target.hand)
        if(card != None):
            target.play_area.append(card)
            supply, target, players, trash, action_stack = card.effect(supply, target, players, trash, action_stack)
        else:
            action_stack = 0
            break
    
        action_stack -= 1  
        
    return supply, target, players, trash