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
            if card.alter_flg == "A":
                supply, target, players, trash = attack_effect(card, supply, target, players, trash)
        else:
            action_stack = 0
            break
    
        action_stack -= 1  
        
    return supply, target, players, trash

# アタック
# アクション発動時に呼び出される
def attack_effect(attack_card, supply, target, players, trash):
    for player in players:
        if player.order == (target.order+1)%4:
            left = player
        if player.order == (target.order+2)%4:
            center = player
        if player.order == (target.order+3)%4:
            right = player

    supply, left, trash = react_effect(supply, left, trash)
    supply, center, trash = react_effect(supply, center, trash)
    supply, right, trash = react_effect(supply, right, trash)

    if not left.barrier_flg:            
        supply, left, trash = attack_card.attack_effect(supply, left, trash)
    if not center.barrier_flg:
        supply, center, trash = attack_card.attack_effect(supply, center, trash)
    if not right.barrier_flg:
        supply, right, trash = attack_card.attack_effect(supply, right, trash)

    return supply, target, players, trash

# リアクション
# アタックアクション発動時に呼び出される
def react_effect(supply, player, trash):
    for card in player.hand:
        if card.alter_flg == "R":
            supply, player, trash = card.react_effect(supply, player, trash)
    return supply, player, trash

# 購入時効果
# 購入直前に呼び出される
def buy_effect(supply, target, trash):
    for card in target.play_area:
        if card.alter_flg == "B":
            supply, target, trash = card.buy_effect(supply, target, trash)

    return supply, target, trash

# 勝利点効果
# ゲーム終了時に呼び出される
def victory_effect(cardlist):
    score = 0
    for card in cardlist:
        if card.alter_flg == "V":
            score += card.victory_effect(cardlist)

    return score
