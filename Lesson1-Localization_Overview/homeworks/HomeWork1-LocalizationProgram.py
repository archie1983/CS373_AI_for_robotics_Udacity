#!/usr/bin/python

# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

#import numpy as np

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    # >>> Insert your code here <<<
    for m in range(len(motions)):
        p = move(p, motions[m], p_move)
        #show(p)
        p = sense(colors, p, measurements[m], sensor_right)
        #show(p)
    
    return p

def sense(world_map, current_p_distr, Z, sensor_right):
    #
    # AE: So we have a probability distribution current_p_distr and we
    # have measured state Z. We now want to create the new
    # probability distribution new_p_distr from current_p_distr
    # given the measurement, but before normalisation.
    #
    
    # First define the probability for a correct detection (sensor may not be perfect)
    pHit = sensor_right
    pMiss = 1.0 - sensor_right
    
    # Now prepare new_p_distr with the same number of rows as current_p_distr
    new_p_distr = []
    for i in range(len(current_p_distr)):
        new_p_distr.append([])
        
    for row in range(len(current_p_distr)):
        for col in range(len(current_p_distr[row])):
            hit = (Z == world_map[row][col])
            #print "HHIT : ", hit, " Z = ", Z, "cr = ",current_p_distr[row][col]
            new_p_distr[row].append(current_p_distr[row][col] * (hit * pHit + (1-hit) * pMiss))

    #print "pMiss = ", pMiss, "pHit = ", pHit
    #show(new_p_distr)
    #show(current_p_distr)
    
    # Now normalisation
    total_probability = 0.0
    for row in range(len(new_p_distr)):
        for col in range(len(new_p_distr[row])):
            total_probability += new_p_distr[row][col]

    for row in range(len(new_p_distr)):
        for col in range(len(new_p_distr[row])):
            new_p_distr[row][col] = new_p_distr[row][col] / total_probability

    return new_p_distr

# A function that returns a new distribution q, shifted according to 
# the move U.
#
# p: current probability distribution (2-dimensional)
# U: move to take (2-dimensional)
# p_move: Chance that the move succeeds as planned.
#
# NOTE: What we shift here is the p -- THE WORLD and NOT THE POSITION OF ROBOT
def move(p, U, p_move):

    # according to rules we won't be overshooting, just either succeeding or staying in the same place 
    # (undershooting by the same number of steps as we wanted to move).
    pNoMove = 1.0 - p_move

    shifted_world = []
    shifted_world_hor = []
    
    current_row = []
    shifted_current_row = []  
    shifted_current_col = []
    current_col = []
    
    # prepare the new shifted world with the correct number of rows
    for row in range(len(p)):
        shifted_world.append([])
    
    # first do the horizontal component of the move
    hor_move = U[1]

    for row in range(len(p)):
    
        shifted_current_row = [] # reset the current row
        current_row = p[row]
        
        for col in range(len(p[row])):
            # so robot moves to the right if U is positive and to the left if it's negative. Or we can say that robot stays where it was, but the world shifts
            # either to the left if U is positive or right if U is negative.
            
            # If we moved by hor_move (positive - to the right, negative - to the left), then we started at (col - hor_move).
            # We want the probability that we had there as that is the major component of the new probability of where we are now.
            start_val = current_row[(col - hor_move) % len(current_row)]

            # If we failed to move then we are now at the same value where we started and the correct value of current_row[col]
            # is what it was, but we don't know that and can only apply probability of pNoMove to such scenario.
            fail_val = current_row[col]

            # If the move succeeded then we should now be at the col column - and that is where we will put in the newly calculated probability.
            new_val = p_move * start_val + pNoMove * fail_val
            shifted_current_row.append(new_val)

        # assembling the new map from shifted rows
        shifted_world_hor.append(shifted_current_row)

    # now do the vertical component of the move
    ver_move = U[0]
    #show(shifted_world_hor)
    #print "horw_c[0]",len(shifted_world_hor[0])
    for col in range(len(shifted_world_hor[0])): # col is index of current column from 0 to count - 1
    
        shifted_current_col = [] # reset the current col
        current_col = []
        # acquire column as a vector for manipulation
        #print "horw_r[0]",len(shifted_world_hor)
        for row in range(len(shifted_world_hor)):
            current_row = shifted_world_hor[row]
            current_col.append(current_row[col])
        
        #print "cur_col ",current_col
        # Doing identical manipulation to how we did for horizontal move. Please see comments above.
        #print "horw_ccol[0]",len(current_col)
        for ccol in range(len(current_col)):
            start_val = current_col[(ccol - ver_move) % len(current_col)]

            fail_val = current_col[ccol]

            new_val = p_move * start_val + pNoMove * fail_val
            shifted_current_col.append(new_val)
    
        #print "shft_col ",shifted_current_col
        # now put the new shifted column back into a map and create the new shifted world map (rotate the column that is now horizontal back to vertical)
        for row in range(len(shifted_current_col)):
            shifted_world[row].append(shifted_current_col[row])

    return shifted_world

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer

# # test 1
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'G'],
          # ['G', 'G', 'G']]
# measurements = ['R']
# motions = [[0,0]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)

# # test 2
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'G'],
          # ['G', 'G', 'G']]
# measurements = ['R', 'G']
# motions = [[0,0], [1,0]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# show(p) # displays your answer

# # test 3
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'R'],
          # ['G', 'G', 'G']]
# measurements = ['R']
# motions = [[0,0]]
# sensor_right = 0.8
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)

# # test 4
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'R'],
          # ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 0.8
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)

# # test 5
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'R'],
          # ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)

# # test 6
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'R'],
          # ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 0.8
# p_move = 0.5
# p = localize(colors,measurements,motions,sensor_right,p_move)

# # test 7
# colors = [['G', 'G', 'G'],
          # ['G', 'R', 'R'],
          # ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 1.0
# p_move = 0.5
# p = localize(colors,measurements,motions,sensor_right,p_move)
#show(p) # displays your answer