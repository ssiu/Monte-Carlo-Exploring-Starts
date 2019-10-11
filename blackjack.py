
import random as rd
import seaborn as sns
import matplotlib.pylab as plt

#Converts the number of 8 decks=[0,...,415] to the correct value. A=1,...,J,Q,K=10    
def cardvalue(n):
    return min(n//32+1,10)

#draw a card from a deck
def draw(deck):
    num=rd.choice(deck)
    deck.remove(num)    
    return cardvalue(num)

class hand:
    def __init__(self,cards,isAce,isBust):
        self.cards = cards
        self.isAce = isAce
        self.isBust = 0
    #Getting dealt a new card
    def deal(self,newcard):      
        if self.isAce == 0:
            if newcard == 1:
                if self.cards + newcard + 10 <= 21:
                    self.isAce = 1
            if self.cards + newcard > 21:
                self.isBust = 1           
            self.cards += newcard
        else:
            if self.cards + newcard > 21:
                self.cards = self.cards + newcard - 10
                self.isAce = 0
            else:
                self.cards += newcard
             
#playing a game of blackjack, starting with a random starting action and following a policy after
def play(policy):
    #initialise the game with 8 decks
    episode=[]
    deck = [ _ for _ in range(416)]        
    #dealer card    
    dealer_card = draw(deck)
    dealer = hand(dealer_card + 10 if dealer_card == 1 else dealer_card, 1 if dealer_card == 1 else 0 , 0 )    
    #player cards
    player_card1=draw(deck)
    player_card2=draw(deck)    
    if player_card1 == 1 or player_card2 == 1:
        isAce = 1
    else:
        isAce = 0
    player = hand(player_card1 + player_card2 + 10 if isAce == 1 else player_card1 + player_card2, isAce, 0 )
    
    #generate initial random action
    random_action = rd.choice([0,1])       
    if random_action == 0:
        episode.append([player.cards,player.isAce,dealer_card,0])
    else: 
        episode.append([player.cards,player.isAce,dealer_card,1])
        newcard=draw(deck)
        player.deal(newcard)    
        
        if player.isBust == 1:
            return [episode,-1]
    
        #player plays according to policy
        while player.isBust == 0:          
            if player.cards <= 11:
                newcard=draw(deck)
                player.deal(newcard)
            else:           
                if policy[player.cards][player.isAce][dealer_card] == 1:
                    episode.append([player.cards,player.isAce,dealer_card,1])
                    newcard=draw(deck)
                    player.deal(newcard)            
                else:
                    episode.append([player.cards,player.isAce,dealer_card,0])
                    break
            
        if player.isBust == 1:
            return [episode,-1]
    
    #player is in the game, dealer plays
    while dealer.isBust == 0:        
        newcard = draw(deck)
        dealer.deal(newcard)
        if dealer.isAce == 0:
            if dealer.cards >= 17:
                break
        else:
            if dealer.cards >=18:
                break
    
    if dealer.isBust == 1:
        return [episode , 1]
    else:
        if player.cards > dealer.cards:
            return [episode,1]
        elif player.cards == dealer.cards:
            return [episode,0]
        elif player.cards < dealer.cards:
            return [episode,-1]
        
#assign rewards
policy = [[[0 for k in range(11)] for j in range(2)] for i in range(22)]
value = [[[[[0,0] for l in range(2)] for k in range(11)] for j in range(2)] for i in range(22)]

#estimate optimal strategy by playing the game 10 million times
for _ in range(10000000):    
    [episode,reward] = play(policy)        
    for state in episode: 
        player = state[0]
        isAce=state[1]
        dealer=state[2]
        action=state[3]
        q=value[player][isAce][dealer][action][0]
        count = value[player][isAce][dealer][action][1]        
        value[player][isAce][dealer][action][0]=(q*count+reward)/(count+1)
        value[player][isAce][dealer][action][1]+=1
    if value[player][isAce][dealer][0][0] >= value[player][isAce][dealer][1][0]:
        policy[player][isAce][dealer] = 0
    else:
        policy[player][isAce][dealer] = 1

#debugging stuff
'''
for i in range(12,22):
    for j in range(2):
        for k in range(1,11):
            print("player =",i,"isAce =",j,"dealer =",k,"action =",policy[i][j][k],"STAND = ",value[i][j][k][0][0],"count = ",value[i][j][k][0][1],"HIT =",value[i][j][k][1][0],"count = ",value[i][j][k][1][1])
'''

#plotting the optimal strategy
hard_total = [[0 for k in range(10)] for i in range(10)]
soft_total = [[0 for k in range(10)] for i in range(10)]

for i in range(10):
    for k in range(10):
        hard_total[i][k]=policy[i+12][0][k+1]
        soft_total[i][k]=policy[i+12][1][k+1]
        
ax1 = sns.heatmap(hard_total, linewidth=0.5, cmap="Set3")
ax1.invert_yaxis()
ax1.set(yticklabels=[12,13,14,15,16,17,18,19,20,21])
ax1.set(xticklabels=[1,2,3,4,5,6,7,8,9,10])
plt.show()

ax2= sns.heatmap(soft_total, linewidth=0.5, cmap="Set3")
ax2.invert_yaxis()
ax2.set(yticklabels=[12,13,14,15,16,17,18,19,20,21])
ax2.set(xticklabels=[1,2,3,4,5,6,7,8,9,10])
plt.show()