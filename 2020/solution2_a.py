# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30
@author: Natalie Robinson

Being a henchman isn't all drudgery. Occasionally, when Commander Lambda is feeling generous, she'll hand out Lucky LAMBs 
(Lambda's All-purpose Money Bucks). Henchmen can use Lucky LAMBs to buy things like a second pair of socks, a pillow for their bunks,
 or even a third daily meal!

However, actually passing out LAMBs isn't easy. Each henchman squad has a strict seniority ranking which must be respected - or else 
the henchmen will revolt and you'll all get demoted back to minions again!

There are 4 key rules which you must follow in order to avoid a revolt: 1. The most junior henchman (with the least seniority) gets 
exactly 1 LAMB. (There will always be at least 1 henchman on a team.) 2. A henchman will revolt if the person who ranks immediately 
above them gets more than double the number of LAMBs they do. 3. A henchman will revolt if the amount of LAMBs given to their next 
two subordinates combined is more than the number of LAMBs they get. (Note that the two most junior henchmen won't have two subordinates, 
so this rule doesn't apply to them. The 2nd most junior henchman would require at least as many LAMBs as the most junior henchman.) 4. 
You can always find more henchmen to pay - the Commander has plenty of employees. If there are enough LAMBs left over such that another 
henchman could be added as the most senior while obeying the other rules, you must always add and pay that henchman.

Note that you may not be able to hand out all the LAMBs. A single LAMB cannot be subdivided. That is, all henchmen must get a positive 
integer number of LAMBs.

Write a function called solution(total_lambs), where total_lambs is the integer number of LAMBs in the handout you are trying to divide. 
It should return an integer which represents the difference between the minimum and maximum number of henchmen who can share the LAMBs 
(that is, being as generous as possible to those you pay and as stingy as possible, respectively) while still obeying all of the above 
rules to avoid a revolt. For instance, if you had 10 LAMBs and were as generous as possible, you could only pay 3 henchmen (1, 2, and 4 
LAMBs, in order of ascending seniority), whereas if you were as stingy as possible, you could pay 4 henchmen (1, 1, 2, and 3 LAMBs). 
Therefore, solution(10) should return 4-3 = 1.

To keep things interesting, Commander Lambda varies the sizes of the Lucky LAMB payouts. You can expect total_lambs to always be a 
positive integer less than 1 billion (10 ^ 9).
"""

def solution(total_lambs):
    '''
    Divide total_lambs with min and max payouts as:
          1. The most junior henchman gets 1 LAMB
          2. The next henchman cannot get more than double the LAMBs of the previous henchman
          3. A henchman cannot get less than the sum of the previous two lower level henchmen's LAMBs
    '''
    if total_lambs < 1:
        raise Exception('You cheapskate, you have to have at least 1 LAMB to pay henchmen')
    if total_lambs > pow(10, 9):
        raise Exception('You are not that rich, please limit your LAMBs to 1 billion or less')
    # Initiate variables
    h_min = 1  # Min henchmen
    h_max = 1  # Max henchmen
    h_lamb_rng = [[1,1]] # Store lamb payout ranges for all henchmen considered
    max_lambs_left = total_lambs # Maximum LAMBs remaining when henchmen paid according to rules
    # While there are still LAMBs available, add henchmen and recalculate
    while max_lambs_left > 0:
        # Calculte lamb payout range for next henchmen; update h_lamb_rng
        if h_max == 1:
            new_rng = [1,2]
        else:
            new_rng = [sum([x[0] for x in h_lamb_rng[h_max-2:h_max]]),2*h_lamb_rng[h_max-1][1]]
        h_lamb_rng.append(new_rng)
        # If there are enough LAMBs available to keep being stingy, update max henchmen
        if total_lambs - sum([x[0] for x in h_lamb_rng]) >= 0:
            h_max = h_max + 1
            # If there are enough LAMBs available to keep being generous, update min henchmen
            if total_lambs - sum([x[1] for x in h_lamb_rng]) >= 0:
                h_min = h_min + 1
        # Recalculate the maximum LAMBs remaining
        max_lambs_left = total_lambs - sum([x[0] for x in h_lamb_rng])
    return h_max - h_min


# Better solution, drawing on Fibonacci sequence and base2
# # Fibonacci seq, excluding 1st value
# def fibSeq(n):
#      [a, b] = [1, 1]
#      while n >0:
#           [a, b] = [b, a + b]
#           n = n - 1
#      return a
    
# def solution2(total_lambs):
#     '''
#     Divide total_lambs with min and max payouts as:
#           1. The most junior henchman gets 1 LAMB
#           2. The next henchman cannot get more than double the LAMBs of the previous henchman
#           3. A henchman cannot get less than the sum of the previous two lower level henchmen's LAMBs
#     '''
#     if total_lambs < 1:
#         raise Exception('You cheapskate, you have to have at least 1 LAMB to pay henchmen')
#     if total_lambs > pow(10, 9):
#         raise Exception('You are not that rich, please limit your LAMBs to 1 billion or less')
#     # Initiate variables
#     max_lambs_left = total_lambs  # Maximum LAMBs remaining when henchmen paid according to rules
#     h_min = 0  # Min henchmen
#     h_max = 0  # Max henchmen
#     # While there are still LAMBs available, add henchmen and recalculate
#     while max_lambs_left > 0:
#         # If there are enough LAMBs available to keep being stingy, update max henchmen
#         if total_lambs - sum([fibSeq(x) for x in range(0,h_max+1)]) >= 0:
#             # Recalculate the maximum LAMBs remaining
#             max_lambs_left = total_lambs - sum([fibSeq(x) for x in range(0,h_max+1)])
#             h_max = h_max + 1 
#             # If there are enough LAMBs available to keep being generous, update min henchmen
#             if total_lambs - sum([pow(2,x) for x in range(0,h_max)]) >= 0:
#                 h_min = h_min + 1
#         else:
#             break
#     return h_max - h_min
