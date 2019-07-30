#!/usr/bin/python
#Modify the code so that it updates the probability twice
#and gives the posterior distribution after both 
#measurements are incorporated. Make sure that your code 
#allows for any sequence of measurement of any length.


p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

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

# applying the measured result to the probability vector:
for i in range(len(measurements)):
    p = sense(p, measurements[i])
print p