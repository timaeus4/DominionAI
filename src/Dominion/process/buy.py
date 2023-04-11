def buy(supply, money, purchase, discard):
    for card in supply:
        if(card.name == purchase.name):
            if(card.num <= 0):
                return money, discard
            else:
                card.reduce(1)
                money = money - purchase.cost
                discard.append(purchase)
    
                return money, discard
    else:
        return money, discard
    
# 購入プロセス。購入カードはあらかじめ導出しておいて外から与える
def execute(supply, player, money, purchase):

    # TODO: 購入数は難しいのでとりあえず1固定
    buy_stack = 1
    for i in range(buy_stack):
        if(purchase != None):
            for card in supply:
                if(card.name == purchase.name):
                    if(card.num > 0):
                        player.buy_history.append([money, purchase.name])
                        money, player.discard = buy(supply, money, purchase, player.discard)
                        return player
                    else:
                        break
        player.buy_history.append([money, "nothing"])
        
    return player