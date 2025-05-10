# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:26:54 2020
@author: Natalie Robinson

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during 
processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample 
could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. 
You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, 
the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering 
the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have 
hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next 
state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the
 numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is 
 guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will 
 always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the 
 calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
"""

import numpy as np
from fractions import gcd  # For python 2 only
# import math

def simplify (n, d):
    ''' Reduce in put numerator (n) and denominoator (d) by dividing each by greatest common divisor'''
    if d != 0:
        # Remove greatest common divisor:
        #gComDiv = math.gcd(n, d)  # For python 3
        gComDiv = gcd(n, d)
        (reduced_n, reduced_d) = (n / gComDiv, d / gComDiv)
        return [int(reduced_n), int(reduced_d)]

def solution(m):
    '''
    Take in input array and find probabilities of each stable state after markov chaining

    Parameters
    ----------
    m : array of observations of state transitions from state in row r to state in column c

    Returns
    -------
    List of numerators of stable states plus common denominator for all (so any given numerator/common denominator == probability for the state)
    
    '''
    # Initiate common denominator as max sum of rows in m
    comm_denom = max([sum(m[x]) for x in range(m.shape[0])])
    
    # 1) Convert each cell into a list, to retain the denominator
    #      - if row sums to 0: insert [1,0] at the diagonal because the state transitions to itself with probability 1
    #      - else: 0 -> [0, 0], others -> [value,rowSum]
    arr = []
    for r in range(m.shape[0]):
        if sum(m[r]) == 0:
            arr.append([[1,0] if c == r else [0,0] for c in range(m.shape[1])])
        else:
            arr.append([[cell,sum(m[r])] if cell != 0 else [0,0] for cell in m[r]])
    # Convert to array
    arr = np.array(arr)
    
    # 2) Rectify loops between non-absobing states
    r = 0  # Initiate row counter
    while r < arr.shape[0]:
        # Identify instances with sum(arr[r][c]) > 1 and sum(arr[c][r]) > 1 (looping transitions)
        for c in [c for c in range(arr.shape[1]) if sum(arr[r][c]) > 1 and sum(arr[c][r]) > 1]:
            # Reduce one row by the probability of both state changes, and eliminate state change in the other row
            prob_both = np.lcm([arr[r][c][0],arr[r][c][1]], [arr[c][r][0],arr[c][r][1]])
            # Reduction numerator: divide elems of arr[r,c], subtract prob_both, multiply by denom from prob_both, return as list
            red_num = [int(((arr[r][c][0]/float(arr[r][c][1]))-(prob_both[0]/float(prob_both[1]))) * prob_both[1]), prob_both[1]]
            # Reduction denominator: 1 - prob_both, reduced and returned as list
            red_denom = simplify(int(((prob_both[1]/float(prob_both[1])) - (prob_both[0]/float(prob_both[1]))) * prob_both[1]), prob_both[1])
            # Reduced value
            reduced = np.lcm([red_num[0], red_num[1]], [red_denom[1], red_denom[0]])
            reduced = simplify(reduced[0],reduced[1])
            arr[r][c] = reduced
            # Redistribute values for row with reduction
            for update_1 in [u for u in range(c+1,arr.shape[1]) if sum(arr[r][u]) > 1]:
                val = arr[r][update_1]
                # Remove 1 trial from the denominator
                val[1] = val[1] - 1
                # Calculate new numerator and update denominator to common denom
                val[0] = int(round(((reduced[1] - reduced[0]) * val[0])/float(val[1])))
                val[1] = reduced[1]
                # Add back to array
                arr[m][update_1] = val
                # Update common denominator
                if reduced[1] > comm_denom:
                    comm_denom = reduced[1]
            # Redistribute values for other row and set primary value to 0
            for update_2 in [u for u in range(r+1,arr.shape[1]) if sum(arr[c][u]) > 1]:
                val = arr[c][update_2]
                # Update denominator
                val[1] = val[1] - arr[c][r][0]
                # Add back to array
                arr[c][update_2] = val
            arr[c][r] = 0
        r += 1
            
    # 3) Convert back to float array to calculate steady state probabilities (re-use m)
    # Keep numerators from each pair
    m = []
    for i in range(arr.shape[0]):
        m.append([item[0] for item in arr[i]])
    # Convert to array
    m = np.array(m)
    m = m.astype(float)  # For python 2
    
    # Convert into transition matrix representing probabilities of state transitions (value/rowSum if value != 0)
    # Python 3
    # m = m/m.sum(axis=1)[:,None]
    # m = np.nan_to_num(m,0)  # Replace nan with 0
    # Python 2
    for i in range(m.shape[0]):
      r_sum = sum(m[i])
      for j in range(m.shape[1]):
        if m[i][j] > 1:
          m[i][j] = m[i][j]/r_sum
    
    # 4) Define s_init and add it to an array of state vector histories (so we can define when the state vector stabilizes)
    # ore starts in state 0 (with probability  == 1 for state 0, 0 for all others)
    s_init = np.zeros(len(m[0]),int)
    s_init[0] = 1  
    
    # 5) Run markov chain 10000 times, multiplying state transition by state vector to update state vector
    for iteration in range(10001):
        # Multiply the state vector by m, and update s_init
        s_init = np.dot(s_init,m)
        iteration += 1
    
    # Return list of integers + common denominator for transition matrix
    return [int(x * comm_denom) for x in s_init if x > 0] + [comm_denom]
