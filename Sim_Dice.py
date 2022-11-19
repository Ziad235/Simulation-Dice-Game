import pprint as pp
import random
import numpy as np

NDice = 0
NSides = 0
LTarget = 0
UTarget = 0
M = 0
##############################################################################################
def Score_Track(Current_Player, Score_Dict):
    #This code block keep track of the final score of each player
    if (Current_Player == "A"):
        return (Score_Dict["A_Score"], Score_Dict["B_Score"])
    elif (Current_Player == "B"):
        return (Score_Dict["B_Score"], Score_Dict["A_Score"])
##############################################################################################
def chooseFromDist(p):
    Index_List = []

    for index in range(len(p)):
        Index_List.append(index+1)

    Chosen_Item = random.choices(Index_List, weights = p, k = 1)

    return (Chosen_Item[0])
##############################################################################################
def rollDice(NDice, NSides):
    Number = []

    for x in range(NDice):
        Number.append(chooseFromDist([1/NSides]*NSides))
    
    return Number
##############################################################################################
def chooseDice(Score, LoseCount, WinCount, NDice, M):
    flist = []
    K = NDice
    g = 0
    T = 0

    #This code block calculates all flist values to be added in the list
    for i in range(1, NDice+1):
        if ((LoseCount[i][Score]+WinCount[i][Score]) == 0):
            flist.append(0.5)
            continue
        else:
            flist.append((WinCount[i][Score] / (LoseCount[i][Score] + WinCount[i][Score])))
    
     #This code block chooses the maximmum value of flist
    if (flist.count(max(flist)) > 1):
        B = random.choice([i for i, x in enumerate(flist) if x == max(flist)]) + 1
    else:
        B = flist.index(max(flist)) + 1

    #This code block calculates g
    for x in range(len(flist)):
        if (x == (B - 1)):
            continue
        else:
            g += flist[x]

    #This code block calculates T
    for x in range(1, NDice+1):
        T += (WinCount[x][Score] + LoseCount[x][Score])

    prob_dict = {}

    #This code block calculates pb
    pb = (T*flist[B-1]+M)/(T*flist[B-1]+(K*M))
    prob_dict[B] = pb

    #This code block calculates pj for j =\= b
    for x in range(len(flist)):
        if x == B-1:
            continue
        else:
            pj = (1 - pb)*(T*flist[x] + M)/((g*T)+((K-1)*M))
            prob_dict[x+1] = pj
    
    prob_dict = dict(sorted(prob_dict.items()))

    return (chooseFromDist(prob_dict.values()))
##############################################################################################
def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    Winner = None
    PlayerA = {"State": []}
    PlayerB = {"State": []}

    Score_Dict = {"A_Score": 0, "B_Score": 0}

    NoTarget = True

    #This while loop is where the game is played
    while(NoTarget):

        #Player A's turn
        Score = Score_Track("A", Score_Dict)
        J = chooseDice(Score, LoseCount, WinCount, NDice, M)
        PlayerA["State"].append((Score, J))

        Roll_Number = rollDice(J, NSides)

        #This code block adds to Player A's scoreboard
        for x in range(len(Roll_Number)):
            Score_Dict["A_Score"] += Roll_Number[x]

        #This code block checks if game is over after a roll
        if (Score_Dict["A_Score"] > UTarget):
            Winner = "B"
            NoTarget = False
            break
        if (Score_Dict["A_Score"] >= LTarget and Score_Dict["A_Score"] <= UTarget):
            Winner = "A"
            NoTarget = False
            break


        #Player B's turn
        Score = Score_Track("B", Score_Dict)
        J = chooseDice(Score, LoseCount, WinCount, NDice, M)
        PlayerB["State"].append((Score, J))

        Roll_Number = rollDice(J, NSides)

        #This code block adds to Player A's scoreboard
        for x in range(len(Roll_Number)):
            Score_Dict["B_Score"] += Roll_Number[x]

        #This code block checks if game is over after a roll
        if (Score_Dict["B_Score"] > UTarget):
            Winner = "A"
            NoTarget = False
            break
        if (Score_Dict["B_Score"] >= LTarget and Score_Dict["B_Score"] <= UTarget):
            Winner = "B"
            NoTarget = False
            break


    #This code block updates the WinCount and LoseCount matrices accordingly, after the game has ended
    if (Winner == "A"):
        for x in PlayerA["State"]:
            WinCount[x[1]][x[0][0]][x[0][1]] += 1
        for x in PlayerB["State"]:
            LoseCount[x[1]][x[0][0]][x[0][1]] += 1
    elif (Winner == "B"):
        for x in PlayerB["State"]:
            WinCount[x[1]][x[0][0]][x[0][1]] += 1
        for x in PlayerA["State"]:
            LoseCount[x[1]][x[0][0]][x[0][1]] += 1          

    return (WinCount, LoseCount)

##############################################################################################
def extractAnswer(WinCount, LoseCount, LTarget, NDice):
    #This block of code initializes the 2x2 matrices that are expected in the output
    Final_Answer = np.zeros((LTarget, LTarget), dtype = int)
    Probs = np.zeros((LTarget, LTarget), dtype = float)

    for X in range(LTarget):
        for Y in range(LTarget):
            tmplist = []
            answer = 0
            prob = 0

            for i in range(1, NDice+1):
                if (LoseCount[i][X][Y] + WinCount[i][X][Y] == 0):
                    tmplist.append(0)
                    continue
                else:
                    tmplist.append((WinCount[i][X][Y] / (LoseCount[i][X][Y] + WinCount[i][X][Y])))

            if (tmplist.count(max(tmplist)) > 1):
                answer = random.choice([i for i, x in enumerate(tmplist) if x == max(tmplist)]) + 1
                prob = max(tmplist)
            else:
                answer = tmplist.index(max(tmplist)) + 1
                prob = max(tmplist)

            Final_Answer[X][Y] = answer
            Probs[X][Y] = prob

    return (Final_Answer, Probs)
##############################################################################################
def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    WinCount = np.zeros((NDice+1, LTarget, LTarget), dtype = np.int64)
    LoseCount = np.zeros((NDice+1, LTarget, LTarget), dtype = np.int64)

    for game in range(NGames):
        WinCount, LoseCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

    Final_Answer, Prob_Table = extractAnswer(WinCount, LoseCount, LTarget, NDice)

    print("\nPLAY: ")
    print(Final_Answer)

    print("\nPROB: ")
    print(Prob_Table)
##############################################################################################
def main():
    global NDice, NSides, LTarget, UTarget, NGames, M
    NSides = int(input("Input the number of sides on each die: "))
    NDice = int(input("Input the maximum number of dice to play in one: "))
    LTarget = int(input("Input the lower bound of the winning target: "))
    UTarget = int(input("Input the upper bound of the winning target: "))
    NGames = int(input("Input the number of games to play: "))
    M = float(input("Input the value for M: "))

    # NSides = 2
    # NDice = 2
    # LTarget = 4
    # UTarget = 4
    # NGames = int(input("Enter the number of games to play: "))
    # M = float(input("Enter the hyperparameter M: "))

    prog3(NDice, NSides, LTarget, UTarget, NGames, M)
##############################################################################################
if __name__ == "__main__":
    main()