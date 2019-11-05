#!/usr/bin/python
#
# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
#
# Your program should print out the result of
# your two sense measurements.
#
# Don't modify the code below. Please enter
# your code at the bottom.

from math import *
import random



landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))



####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

myrobot = robot()

# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
myrobot.set(30, 50, pi / 2)
#print myrobot.sense()
myrobot = myrobot.move(-pi / 2, 15)
print myrobot.sense()
myrobot = myrobot.move(-pi / 2, 10)
print myrobot.sense()

# Now add noise to your robot as follows:
# forward_noise = 5.0, turn_noise = 0.1,
# sense_noise = 5.0.
#
# Once again, your robot starts at 30, 50,
# heading north (pi/2), then turns clockwise
# by pi/2, moves 15 meters, senses,
# then turns clockwise by pi/2 again, moves
# 10 m, then senses again.
myrobot = robot()
myrobot.set_noise(5.0, 0.1, 5.0)
myrobot.set(30, 50, pi / 2)
#print myrobot.sense()
myrobot = myrobot.move(-pi / 2, 15)
print myrobot.sense()
myrobot = myrobot.move(-pi / 2, 10)
print myrobot.sense()

# Having played with myrobot, we'll re-initialise it and move it to a certain place.
# We will then take a measurement from the landmarks and compare that measurement with
# 1000 other random points that have moved by the same amount.
myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

# Generating 1000 random points (particles) - initial possible robot locations
N = 1000
p = []

for i in range(N):
    p.append(robot())

#print len(p)

# Now we want to simulate robot
# motion with our particles.
# Each particle should turn by 0.1
# and then move by 5 - same as myrobot
# in the beginning.
p2 = []
for i in range(N):
    r = p[i]
    r.set_noise(0.05, 0.05, 5.0) # we need some measurement, move and turn noise, otherwise weight calculation with measurement_prob(...) will give division by 0
    p2.append(r.move(0.1, 5))

p = p2

#print p

# Now we want to give weight to our 
# particles. This code will assign weights
# to 1000 particles in the list.
w = []
for i in range(N):
    measurement_probability = p[i].measurement_prob(Z)
    w.append(measurement_probability)

print w