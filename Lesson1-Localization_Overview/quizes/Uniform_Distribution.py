#!/usr/bin/python
#Modify the code so that it updates the probability twice
#and gives the posterior distribution after both 
#measurements are incorporated. Make sure that your code 
#allows for any sequence of measurement of any length.

p=[0, 1, 0, 0, 0] # where the robot is (probabilities for each field in the world)
world=['green', 'red', 'red', 'green', 'green'] # the map of the world- true colours of each field
measurements = ['red', 'green'] # what was measured both times that we measuered
pHit = 0.6 # "caution" factor with which we are going to multiply a measurement, that we expected (adds to our belief about a state)
pMiss = 0.2 # "caution" factor with which we are going to multiply a mesaurement, that we didn't expect (adds doubt to our belief about a state)

motions = [1, 1] # In one of the scenarios the robot moves twice to the right by 1 step each time

pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    #
    # AE: So we have a probability vector p and we
    # have measured state Z. We now want to change
    # p in such a way that it will reflect the new
    # probability vector given the measurement, but
    # before normalisation.
    #
    q = []
    for i in range(len(world)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
        #print hit, " ", q, " ", p[i]
    
    # Now normalisation
    q_sum = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / q_sum
    
    return q

#Program a function that returns a new distribution 
#q, shifted to the right by U units. If U=0, q should 
#be the same as p.
#Modify the move function to accommodate the added 
#probabilities of overshooting or undershooting 
#the intended destination.
#
# NOTE: What we shift here is the p -- THE WORLD and NOT THE POSITION OF ROBOT
#
def move(p, U):
    #U = U % len(p)
    #q = p[-U:] + p[:-U]
    q = []
    for i in range(len(p)):
        # so robot moves to the right if U is positive and to the left if it's negative. Or we can say that robot stays where it was, but the world shifts
        # either to the left if U is positive or right if U is negative.
        
        old_val_u = p[(i-U)%len(p)] # the cell to look at if we started at i and the whole world shifted to the opposite direction of robot movement.
        old_val_prev_u = p[(i-U+1)%len(p)] # the cell to look at if we started at i and undershot by 1
        old_val_post_u = p[(i-U-1)%len(p)] # the cell to look at if we started at i and overshot by 1

        new_val = old_val_u * pExact + old_val_prev_u * pUndershoot + old_val_post_u * pOvershoot
        q.append(new_val)
    return q

print "Initial world: ", p
p = move(p, 2)
print "After moving two steps to the right: ", p
    
# applying the measured result to the probability vector:
for i in range(len(measurements)):
    p = sense(p, measurements[i])

print "After subsequent sense: ", p, " Because the measurements were contradictory, we get back the same probability vector"

# printing what the world will look like if robot moves twice without anymore sensing
print "After two more moves by 1 step to the right without sensing anymore: ", move(move(p, 1),1)

# Now move 1000 times and see how certainty decays to uniform distribution of 0.2
for i in range(1000):
    p = move(p, 1)

print "After 1000 more moves to the right without sensing: ", p

#
# Now robot first senses red, then moves right one, then senses 
# green, then moves right again, starting with a uniform prior distribution.
for m in range(len(motions)):
    p = sense(p, measurements[m])
    p = move(p, motions[m])

print "Robot moves to the right, then senses red, then moves right again and senses green (starts at uniform disitribution): ", p
print "The world is always: ", world

print "And now according to our algorithm the highest possibility for the robot is to be at cell 5 (right most)"
