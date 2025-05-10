# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 09:34:57 2020
@author: Natalie Robinson

With her LAMBCHOP doomsday device finished, Commander Lambda is preparing for her debut on the galactic stage - but in order to make a
 grand entrance, she needs a grand staircase! As her personal assistant, you've been tasked with figuring out how to build the best 
 staircase EVER. 

Lambda has given you an overview of the types of bricks available, plus a budget. You can buy different amounts of the different types 
of bricks (for example, 3 little pink bricks, or 5 blue lace bricks). Commander Lambda wants to know how many different types of staircases 
can be built with each amount of bricks, so she can pick the one with the most options. 

Each type of staircase should consist of 2 or more steps.  No two steps are allowed to be at the same height - each step must be lower than 
the previous one. All steps must contain at least one brick. A step's height is classified as the total amount of bricks that make up that 
step. For example, when N = 3, you have only 1 choice of how to build the staircase, with the first step having a height of 2 and the second 
step having a height of 1: (# indicates a brick)

#
##
21

When N = 4, you still only have 1 staircase choice:

#
#
##
31
 
But when N = 5, there are two ways you can build a staircase from the given bricks. The two staircases can have heights (4, 1) or (3, 2), 
as shown below:

#
#
#
##
41

#
##
##
32

Write a function called solution(n) that takes a positive integer n and returns the number of different staircases that can be 
built from exactly n bricks. n will always be at least 3 (so you can have a staircase at all), but no more than 200, because Commander 
Lambda's not made of money!
"""

def solution(n):
    '''
    How many unique sets from a list of available bricks sum to n bricks?
       (integer partitioning, perfect sum problem)
    
    Inputs: n = number of bricks available for building stairs
    Goal: Figure out how  many different staircases could be built with n bricks, using these rules:
        1. Each type of staircase must have > 1 step
        2. No two steps can be the same height
        3. All steps must contain at least one brick
        4. A step's height == the total amount of bricks used to make it
    '''
    try:
        # Initiate list of possible bricks to use in creating sets of steps, starting with 1 (min allowed/step)
        n_list = [i for i in range(1, n+1)]
        # Create a 2D array with:
            # c columns, where c = 0:len(n_list). To incrementally evaluate #'s of bricks for creating steps of increasing height
            # r rows, where r = 0:n+1. For step-wise evaluations of adding incrementally larger steps
        # Array stores (in cell [r,c]) the sum of ways step of height r could be created by n_list element c and previous values
        arr = [[0 for c in range(n)] for r in range(n+1)] # Initiate with 0's
        # Iterate over steps of increasing height, storing the numbers of ways they can be built using the available bricks
        # 1) fill 0th row with 1's, because step of height[0,n] can always be built
        arr[0] = [1 for c in range(n)]
        # 2) seed the first column, so each subsequent evaluation has a "previous number of steps built"
        arr[n_list[0]][0] = 1  # If n_list[0] is in the rows heights being evaluated, set the 0th element in that row to 1
        # 3) use iteration to evaluate possible ways each set of elements in n_list could be used to build steps
        for r in range(1, n+1):
            for c in range(1, n):
                # If c_th element of n_list > r_th step height, can't add a new step. Value = previous value for r_th step
                if n_list[c] > r:
                    arr[r][c] = arr[r][c-1]
                # Otherwise, add new steps via:
                    # Find the diff between the height of step r and the c_th element in n_list
                    # Get # of ways smaller steps could have previoulsy been built with diff (0 if diff isn't in n_list[0:c+1]], 1 if diff itself in n_list, > 1 if diff in list and/or combo of other values in n_list has been used to make step of height diff)
                    # Add answer to the # ways r_th step could have previously been built
                else:
                    diff = r - n_list[c]
                    arr[r][c] = arr[diff][c-1] + arr[r][c-1]
        # Last arr element = total sets of steps using n bricks, including 1 step w/all bricks. Subtract 1 to remove illegal step
        return arr[n][len(n_list)-1] - 1
    except:
        return 'Invalid starting n'