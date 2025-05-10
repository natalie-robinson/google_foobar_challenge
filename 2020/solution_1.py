# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:45:03 2020
@author: Natalie Robinson

Solar Doomsday:

Who would've guessed? Doomsday devices take a LOT of power. Commander Lambda wants to supplement the LAMBCHOP's quantum antimatter reactor 
core with solar arrays, and she's tasked you with setting up the solar panels.

Due to the nature of the space station's outer paneling, all of its solar panels must be squares. Fortunately, you have one very large and 
flat area of solar material, a pair of industrial-strength scissors, and enough MegaCorp Solar Tape(TM) to piece together any excess panel 
material into more squares. For example, if you had a total area of 12 square yards of solar material, you would be able to make one 3x3 
square panel (with a total area of 9). That would leave 3 square yards, so you can turn those into three 1x1 square solar panels.

Write a function solution(area) that takes as its input a single unit of measure representing the total area of solar panels you have 
(between 1 and 1000000 inclusive) and returns a list of the areas of the largest squares you could make out of those panels, starting with
the largest squares first.

So, following the example above; solution(12) returns [9, 1, 1, 1].

"""

import math
import numpy as np

# Function
def solution(area):
    if area < 1 or area > 1000000:
        return ['BONG - You have entered an illegal area value for the Doomsday project! Please try again minion']
    else:
        # Initiate LAMBCHOP cut instruction list
        lc_cutList = []
        # Get largest square and what remains
        lgst_sq = math.floor(math.sqrt(area))
        remain = area - pow(lgst_sq,2)     
        # Add largest square to cut list
        lc_cutList.append([pow(lgst_sq,2)])
        # Continue making squares from the remainder of material, until only 1yd squares available
        while math.sqrt(remain) >= 2:                 
            lgst_sq = math.floor(math.sqrt(remain))
            # Add largest square to cut list
            lc_cutList.append([pow(lgst_sq,2)])
            remain = remain - pow(lgst_sq,2)
        # Split remainder into single squares
        lc_cutList.append(np.repeat(1,remain).tolist())
        # Return final LAMBCHOP cut instruction list
        return [int(x) for y in lc_cutList for x in y]
