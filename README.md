# BlackJack_Dice_Game

### How the game is played:
Two players alternately roll dice, and keep track of their total across turns.   
They are each trying to reach a sum that lies in a specified target, between a fixed low value and high value. If a player reaches a score in the target range, they immediately win.   
If a player exceeds the high value, the player immediately loses.  
The players can choose the number of dice to roll on each turn, between 1 and a fixed maximum.  

### The game has 5 parameters:
- _NSides_ (int): The number of sides of the die. The die is numbered 1 to _NSides_, and all outcomes are equally likely.
- _LTarget_ (int): The lowest winning value.
- _UTarget_ (int): The highest winning value.
- _NDice_ (int): The maximum number of dice a player may roll.
- _M_ (float): A hyperparameter that controls the "explore/exploit" trade-off.


#### How to run program:
- Make sure Python3 is installed.
- Run the program on the terminal using "python3 <program_name>.py".


_Note that this is not an interactive game. It is merely a program simulates the game between two players in order to give the user an optimal playing strategy._  

_The outputs of the program are two LTarget × LTarget arrays, the correct number of dice to roll in state (X, Y), and
the probability of winning if you roll the correct number of dice._
