# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30
@author: Natalie Robinson

Commander Lambda uses an automated algorithm to assign minions randomly to tasks, in order to keep her minions on their toes. 
But you’ve noticed a flaw in the algorithm - it eventually loops back on itself, so that instead of assigning new minions as it 
iterates, it gets stuck in a cycle of values so that the same minions end up doing the same tasks over and over again. You think 
proving this to Commander Lambda will help you make a case for your next promotion.

You have worked out that the algorithm has the following process:

Start with a random minion ID n, which is a nonnegative integer of length k in base b
Define x and y as integers of length k. x has the digits of n in descending order, and y has the digits of n in ascending order
Define z = x - y. Add leading zeros to z to maintain length k if necessary
Assign n = z to get the next minion ID, and go back to step 2
For example, given minion ID n = 1211, k = 4, b = 10, then x = 2111, y = 1112 and z = 2111 - 1112 = 0999. Then the next minion
ID will be n = 0999 and the algorithm iterates again: x = 9990, y = 0999 and z = 9990 - 0999 = 8991, and so on.

Depending on the values of n, k (derived from n), and b, at some point the algorithm reaches a cycle, such as by reaching a 
constant value. For example, starting with n = 210022, k = 6, b = 3, the algorithm will reach the cycle of values [210111, 122221, 102212] 
and it will stay in this cycle no matter how many times it continues iterating. Starting with n = 1211, the routine will reach the 
integer 6174, and since 7641 - 1467 is 6174, it will stay as that value no matter how many times it iterates.

Given a minion ID as a string n representing a nonnegative integer of length k in base b, where 2 <= k <= 9 and 2 <= b <= 10, write a 
function solution(n, b) which returns the length of the ending cycle of the algorithm above starting with n. For instance, in the example 
above, solution(210022, 3) would return 3, since iterating on 102212 would return to 210111 when done in base 3. If the algorithm reaches 
a constant, such as 0, then the length is 1.

"""

def numberToBase10(num, b):
    '''
    Convert integer from base b to base 10 notation. Return as string
    '''
    if num == 0:
        return [0]
    digits = []
    while num:
        digits.append(int(num % b))
        num //= b
    digits.reverse()
    return ''.join([str(x) for x in digits])

def solution(n, b):
    '''
    Inputs: n = minion ID (as string)
            b = base in which to run algorithm
    Goal: Update n until the algorithm gets stuck in a loop. Report the length
       of the ending cycle (number of updated minion IDs in a cycle before one is reused)
    '''
    try:
        if int(n) > pow(10, 9):
            raise Exception('Invalid starting minion ID (n) or base (b). n must be a string between 10 and 1 billion, and valid for the base system of b. b must be between 2 and 10')
        # Get length of input string
        k = len(n)
        # Initiate list of IDs already used
        visited = []
        # Loop through IDs, apply logic, update to next ID for as long as end ID has not been used
        while n not in visited:
            # Add current ID to visited
            visited.append(n)
            # Calculate new n
            x = str(int(''.join(reversed(sorted(n))), b))  # reverse sort characters and convert to base10
            y = str(int(''.join(sorted(n)), b)) # sort characters and convert to base10
            diff = int(x) - int(y)  # find difference
            if diff != 0:
                z = str(diff).rjust(k, '0')  # Pad with leading 0's
                n = numberToBase10(int(z), b).rjust(k, '0')  # convert back to base b and pad
            else:
                break
        # Return length of loop
        if diff == 0:
            return 1
        else:
            return len(visited) - visited.index(n)
    except:
        return 'Invalid starting minion ID (n) or base (b). n must be a string between 10 and 1 billion, and valid for the base system of b. b must be between 2 and 10'
