# Solving Blackjack using Monte Carlo Exploring Starts

We use the Monte Carlo Exploring Starts algorithm to derive an optimal strategy of playing Blackjack. 

Running [blackjack.py](https://github.com/unital/Monte-Carlo-Exploring-Starts/blob/master/blackjack.py) will generate the two pictures below. The horizontal axis denotes the dealer's face-up card (1 being A) while the vertical axis denotes the player's hand.  Yellow boxes mean hit and teal boxes mean stand. The first picture is the strategy when the player has a usable ace the second picture is when the player does not have an usable ace.  

![](https://github.com/unital/Monte-Carlo-Exploring-Starts/blob/master/hard_total.png)


![](https://github.com/unital/Monte-Carlo-Exploring-Starts/blob/master/soft_total.png)

This strategy is indeed consistent with the tables provided on wikipedia, but for our case we only allow hit and stand.

https://en.wikipedia.org/wiki/Blackjack
