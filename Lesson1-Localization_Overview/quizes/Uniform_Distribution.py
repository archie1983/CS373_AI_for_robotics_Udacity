#!/usr/bin/python
#Modify the code so that it updates the probability twice
#and gives the posterior distribution after both 
#measurements are incorporated. Make sure that your code 
#allows for any sequence of measurement of any length.

p=[1, 2, 3, 4, 5]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

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
def move(p, U):
    #U = U % len(p)
    #q = p[-U:] + p[:-U]
    q = []
    for i in range(len(p)):
        q.append(p[(i-U)%len(p)])
    return q

print move(p, 1)
    
# applying the measured result to the probability vector:
for i in range(len(measurements)):
    p = sense(p, measurements[i])
print p