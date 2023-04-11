from Dominion.operation import deck_operation

# 手札とプレイエリアを一掃
def flow(player):
    player.discard.extend(player.hand)
    player.discard.extend(player.play_area)
    player.hand = []
    player.play_area = []
    
    return player

def execute(player):
    player = flow(player)
    player.money_stack = 0
    player.buy_stack = 1
     
    for i in range(5):
        player.deck, player.hand, player.discard = deck_operation.draw(player.deck, player.hand, player.discard)
        
    player.hand = sorted(player.hand, key=lambda t:t.cost)
        
    return player