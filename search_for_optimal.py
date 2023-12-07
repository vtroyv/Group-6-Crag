from collections import Counter
import time


#For finding index in each list for any combination of categories left to enter
def enteredlist_toindex(entered):
    return int(''.join([str(int(x)) for x in entered]),2)


#For finding which categories have been entered based on position in list
def indexto_enteredlist(i):
    return [int(j) for j in list(f'{i:06b}')]


#Creating list containing expected values for final turn
def expected_list_setup(roll_number):
    expected_list = [0]*64
    one_left =[[0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1], 
               [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0]]
    if roll_number == 0:
        multiplier = 11/12
    elif roll_number == 1:
        multiplier = 1/2
    else:
        assert ValueError("Roll number should be 0 or 1")
    for entered in one_left:
        index = entered.index(0)
        expected_list[enteredlist_toindex(entered)] = (index+1)*multiplier
    return(expected_list)


#Expected score in future rounds if category i entered in this turn
def give_expected(i, entered):
    temp_entered = entered.copy()
    temp_entered[i-1] = 1
    return expected_startofturn[enteredlist_toindex(temp_entered)]


#decision for category to score in based on dice after 2nd roll
#uses future turn expected values to make a decision
def snd_roll_dec(current_dice,entered):
    current_dice_count = Counter(current_dice)
    scores_left = [i+1 for i,k in enumerate(entered) if k==0]
    expected_to_end = [0]*6
    for i in scores_left:
        expected_to_end[i-1] = i*current_dice_count[i] + give_expected(i, entered)
    max_exp = max(expected_to_end)
    return (expected_to_end.index(max_exp),max_exp)
    

#compares expected scores expected over the rest of the game for each choice of dice to reroll
#only considers choices which "store" one value of dice and will always store max number of each value
def fst_roll_dec(roll,entered):
    current_dice_count = Counter(roll)
    scores_left = [i+1 for i,k in enumerate(entered) if k==0]
    expected_list = [0]*6
    expected_reroll_all = expected_reroll[enteredlist_toindex(entered)]
    for i in scores_left:
        if current_dice_count[i]==3:
            expected_list[i-1] = snd_roll_dec((i,i,i), entered)[1]
        elif current_dice_count[i]==2:
            for j in range(1,7):
                expected_list[i-1] += snd_roll_dec((i,i,j), entered)[1]/6
        elif current_dice_count[i]==1:
            for j in dice_list_2:
                expected_list[i-1] += len(set(j))*snd_roll_dec((i,j[0],j[1]), entered)[1]/36
        elif current_dice_count[i]==0:
            expected_list[i-1] = expected_reroll_all
    max_exp = max(expected_list)
    if max_exp >= expected_reroll_all:
        return (expected_list.index(max_exp),max_exp)
    else:
        return (-1,expected_reroll_all)


#updating lists containing score expected across remainder of the game
def change_expected_lists(expectation, entered, roll_number):
    if roll_number == 1:
        expected_reroll[enteredlist_toindex(entered)] = expectation
    elif roll_number == 0:
        expected_startofturn[enteredlist_toindex(entered)] = expectation


#iterating through all combinations of categories left to enter at this turn
#and iterating through all possible dice rolls always making optimal decision
#finding expected score across remainder of game and updating list accordingly
def turn_expectations(left_to_enter,roll_number):
    for entered in left_to_enter:
        exp_for_entered = 0
        for roll in dice_list_3:
            if roll_number == 1:
                exp_for_roll = snd_roll_dec(roll, entered)[1]
            elif roll_number == 0:
                exp_for_roll = fst_roll_dec(roll, entered)[1]
            mult_decider = len(set(roll))
            if mult_decider == 1:
                exp_for_entered += exp_for_roll/216
        
            if mult_decider == 2:
                exp_for_entered += 3*exp_for_roll/216
        
            if mult_decider == 3:
                exp_for_entered += 6*exp_for_roll/216
        change_expected_lists(exp_for_entered, entered,roll_number) 


#list of all unique dice rolls for 2 and 3 dice
dice_list_2=((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2), 
             (2, 3), (2, 4), (2, 5), (2, 6), (3, 3), (3, 4), (3, 5),
             (3, 6), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 6))
dice_list_3 = ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4), (1, 1, 5), (1, 1, 6), 
               (1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 2, 6), (1, 3, 3), 
               (1, 3, 4), (1, 3, 5), (1, 3, 6), (1, 4, 4), (1, 4, 5), (1, 4, 6), 
               (1, 5, 5), (1, 5, 6), (1, 6, 6), (2, 2, 2), (2, 2, 3), (2, 2, 4), 
               (2, 2, 5), (2, 2, 6), (2, 3, 3), (2, 3, 4), (2, 3, 5), (2, 3, 6), 
               (2, 4, 4), (2, 4, 5), (2, 4, 6), (2, 5, 5), (2, 5, 6), (2, 6, 6), 
               (3, 3, 3), (3, 3, 4), (3, 3, 5), (3, 3, 6), (3, 4, 4), (3, 4, 5), 
               (3, 4, 6), (3, 5, 5), (3, 5, 6), (3, 6, 6), (4, 4, 4), (4, 4, 5), 
               (4, 4, 6), (4, 5, 5), (4, 5, 6), (4, 6, 6), (5, 5, 5), (5, 5, 6), 
               (5, 6, 6), (6, 6, 6))


#categories left to enter at each turn 
#1 if category has been entered 0 if not
two_left_to_enter = [[0, 0, 1, 1, 1, 1], [0, 1, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1], [0, 1, 1, 1, 0, 1], 
                     [0, 1, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1], [1, 0, 1, 0, 1, 1], [1, 0, 1, 1, 0, 1], 
                     [1, 0, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 1, 0], 
                     [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 0, 0]]

three_left_to_enter = [[0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 1, 1], [0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 1, 0], 
                      [0, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1], 
                      [0, 1, 1, 0, 1, 0], [0, 1, 1, 1, 0, 0], [1, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 1], 
                      [1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0], [1, 0, 1, 1, 0, 0], 
                      [1, 1, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0], [1, 1, 0, 1, 0, 0], [1, 1, 1, 0, 0, 0]]

four_left_to_enter = [[0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 1], 
                      [0, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 1, 0], 
                      [0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0], 
                      [1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0]]

five_left_to_enter = [[0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0], 
                      [0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]]

categories_left_to_enter = [two_left_to_enter,three_left_to_enter,four_left_to_enter,five_left_to_enter,[[0,0,0,0,0,0]]]


t1 = time.time()
#using expected values on the last turn instead of iterating through all dice rolls
expected_reroll = expected_list_setup(1)
expected_startofturn = expected_list_setup(0)
print(expected_reroll)
print("")
print(expected_startofturn)
print("---------------------------------------")
#working back through each roll and turn
#will edit each list on each iteration to be used for earlier rounds
for left_to_enter in categories_left_to_enter:
    for number_of_roll in reversed(range(2)):
        turn_expectations(left_to_enter ,number_of_roll)
    print(expected_reroll)
    print("")
    print(expected_startofturn)
    print("----------------------------------------------")
t2 = time.time()
print("")
print(f"time taken: {t2-t1}seconds")
print(" ")
print(f"So the optimal expected total score is {max(expected_startofturn)}")


#writing lists to text file to be used for testing 
with open('expected_list_startofturn.txt', 'x') as file:
    for line in expected_startofturn:
        file.write(f"{line},")
file.close()

with open('expected_list_reroll.txt', 'x') as file:
    for line in expected_reroll:
        file.write(f"{line},")
file.close()








