# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:01:08 2020
@author: Natalie Robinson

Bomb, Baby!

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy special 
self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach bombs (M) and Facula 
bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy to all the strategic points you've 
identified and destroy them at the same time. 

But there's a few catches. First, the bombs self-replicate via one of two distinct processes: 
Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce 3 Mach bombs and 5 Facula bombs, or 5 Mach 
bombs and 2 Facula bombs. The replication process can be changed each cycle. 

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP device. Too few, 
and the device might survive. Too many, and you might overload the mass capacitors and create a singularity at the heart of the 
space station - not good! 

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you arrived, so
that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP, but that's not going 
to stop you from trying!) 

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to destroy the LAMBCHOP. 
Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed. Return the fewest number of generations 
(as a string) that need to pass before you'll have the exact number of bombs necessary to destroy the LAMBCHOP, or the string "impossible" 
if this can't be done! M and F will be string representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", 
one generation would need to pass, so the solution would be "1". However, if M = "2" and F = "4", it would not be possible.
"""

def solution(F, M):
    '''
    Inputs: F = desired Facula bombs (as string)
            M = desired Mach  bombs (as string)
    Goal: Starting with 1 of each bomb type, create new bombs - via one of the processes
            below - until F and M are satisfied, then return the number of cycles needed to
            create the desired M and F bombs. If desired F and M are never created, return 'impossible'
        Process 1: Create a new F bomb for every input M bomb
        Process 2: Create a new M bomb for every input F bomb
    '''
    try:
        # # Exception if inputs are not string, are too large or too small, or are not integer
        # if not isinstance('F', str) or not isinstance('M', str):
        #     raise Exception('Invalid starting F and/or M. Each value must be a whole integer, input as a string, that is > 0 and <= 10^50')
        # if eval(M) > pow(10, 50) or eval(F) > pow(10, 50) or eval(M) < 1 or eval(F) < 1 or not isinstance(eval(F), int) or not isinstance(eval(M), int):
        #     raise Exception('Invalid starting F and/or M. Each value must be a whole integer, input as a string, that is > 0 and <= 10^50')
        # Initiate inputs
        bombs_needed = [int(eval(M)), int(eval(F))]
        cycle = 0
        # Work backward from desired numbers to [1, 1]. Outcomes are additive, with larger number having increased by smaller number each time. Chunks of steps can be knocked out by # times smaller number goes into larger
        while sum(bombs_needed) > 2:
            # When the min # bombs is met by one type, large-small more steps gets both to 1
            if 1 in bombs_needed:
                cycle += max(bombs_needed) - min(bombs_needed)
                break
            # If one # has gone below minimum, the steps reached an impossible combo
            elif max(bombs_needed) % min(bombs_needed) == 0:
                cycle = 'impossible'
                break
            else:
                # Number of times (steps) small number goes into large
                cycle += int(max(bombs_needed)/min(bombs_needed))
                # Update list with [remainder of large/small, small] (as small # held steady)
                bombs_needed = [max(bombs_needed) % min(bombs_needed), min(bombs_needed)]            
        return str(cycle)
    except:
        return 'Invalid starting F and/or M. Each value must be a whole integer, input as a string, that is > 0 and <= 10^50'

# Someone else's solution from internet - for comparison and learning.  
def solution_2(F, M):
    F, M = int(F), int (M)
    cycle = 0
    
    while (F != 1 and M != 1):
        if F % M == 0:
            return 'impossible'        
        else:
            cycle = cycle + int(max(F, M)/min(F, M))
            F, M = max(F, M) % min (F, M), min(F, M)
    return str(cycle + max(F, M) - 1)

# Compare outputs - they're always the same
for F in [str(x) for x in range(1,1001)]:
    for M in [str(x) for x in range(1,1001)]:
        if solution (F, M) != solution_2 (F, M):
            print(F, M)

# VERY FRUSTRATING!  When I removed the exceptions (commented out in solution) that 1st verified the inputs were 'legal', the code passed foobar tests. With those exceptions, it failed foobar tests.  Without the exceptions, 0 is returned for values < 1, pow(10,50)+1 is allowed to run, etc.  WHY DOESN'T GOOGLE WANT CLEAN PROGRAMS?