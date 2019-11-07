#!/usr/bin/python
# -----------------
# USER INSTRUCTIONS
#
# Write a function in the class robot called move()
#
# that takes self and a motion vector (this
# motion vector contains a steering* angle and a
# distance) as input and returns an instance of the class
# robot with the appropriate x, y, and orientation
# for the given motion.
#
# *steering is defined in the video
# which accompanies this problem.
#
# For now, please do NOT add noise to your move function.
#
# Please do not modify anything except where indicated
# below.
#
# There are test cases which you are free to use at the
# bottom. If you uncomment them for testing, make sure you
# re-comment them before you submit.

from math import *
import random
# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------

    # init: 
    #	creates robot and initializes location/orientation 
    #

    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    
    ############# ONLY ADD/MODIFY CODE BELOW HERE ###################

    # --------
    # move:
    #   move along a section of a circular path according to motion
    #
    def move(self, motion): # Do not change the name of this function

        # ADD CODE HERE
        distance_to_travel = motion[1]
        steering_angle = motion[0]
        
        # before anything else, let's add some input checks
        if abs(steering_angle) > max_steering_angle:
            raise ValueError, 'Exceeding max steering angle'
            
        if distance_to_travel < 0.0:
            raise ValueError, 'Moving backwards is not valid'
        
        # first creating a new robot, which will have the updated state.
        result = robot()
        # we want to copy the input robots length and noise parameters.
        result.length = self.length
        result.bearing_noise = self.bearing_noise
        result.steering_noise = self.steering_noise
        result.distance_noise = self.distance_noise
        
        # now let's apply noise
        steering_angle = random.gauss(steering_angle, self.steering_noise)
        distance_to_travel = random.gauss(distance_to_travel, self.distance_noise)
        
        turning_angle = (distance_to_travel / self.length) * tan(steering_angle)
        
        # First the case where steering angle is large enough to take into account - we will be turning while driving.
        if (turning_angle >= 0.001):
            # first we need turning radius
            turning_radius = distance_to_travel / turning_angle
            
            # now update X
            cx = self.x - sin(self.orientation) * turning_radius
            result.x = cx + sin(self.orientation + turning_angle) * turning_radius
            
            # now update Y
            cy = self.y + cos(self.orientation) * turning_radius
            result.y = cy - cos(self.orientation + turning_angle) * turning_radius
            
            # now update orientation
            result.orientation = (self.orientation + turning_angle) % (2.0 * pi)
        else:
            # Now the case where steering angle is tiny and we can just update the position based on the current orientation
            result.x = self.x + distance_to_travel * cos(self.orientation)
            result.y = self.y + distance_to_travel * sin(self.orientation)
            result.orientation = (self.orientation + turning_angle) % (2.0 * pi)
            
        return result # make sure your move function returns an instance
                      # of the robot class with the correct coordinates.
                      
                      
    # --------------
    # USER INSTRUCTIONS
    #
    # Write a function in the class robot called sense()
    # that takes self as input
    # and returns a list, Z, of the four bearings* to the 4
    # different landmarks. you will have to use the robot's
    # x and y position, as well as its orientation, to
    # compute this.
    #
    # *bearing is defined in the video
    # which accompanies this problem.
    #
    # For now, please do NOT add noise to your sense function.
    #
    # Please do not modify anything except where indicated
    # below.
    #
    # There are test cases provided at the bottom which you are
    # free to use. If you uncomment any of these cases for testing
    # make sure that you re-comment it before you submit.

    # --------
    # 
    # the "world" has 4 landmarks.
    # the robot's initial coordinates are somewhere in the square
    # represented by the landmarks.
    #
    # NOTE: Landmark coordinates are given in (y, x) form and NOT
    # in the traditional (x, y) format!
    
    # --------
    # sense:
    #   obtains bearings from positions
    #
    
    def sense(self, add_noise = 1): #do not change the name of this function
        Z = []

        # ENTER CODE HERE
        # HINT: You will probably need to use the function atan2()
        #print "landmarks : ", landmarks, self
        for i in range(len(landmarks)):
            cur_landmark = landmarks[i]
            #print "ra: ", cur_landmark[0] - self.y, " r32: ", cur_landmark[1] - self.x
            bearing = atan2(cur_landmark[0] - self.y, cur_landmark[1] - self.x) - self.orientation
            
            if (add_noise):
                bearing += random.gauss(0.0, self.bearing_noise)
            
            bearing = bearing % (2 * pi) # a very important moment here: The bearing HAS TO BE NORMALIZED, because atan2 function
                                         # will happily give out negative numbers, which mean angles with (-x) component on the x-y
                                         # space, but we of course want positive angles from 0 to 2 * pi.
            
            Z.append(bearing)

        return Z #Leave this line here. Return vector Z of 4 bearings.

        
## TEST CASES for MOVEMENT (STATE) model
##
## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## move function with randomized motion data.

## --------
## TEST CASE:
## 
## 1) The following code should print:
##       Robot:     [x=0.0 y=0.0 orient=0.0]
##       Robot:     [x=10.0 y=0.0 orient=0.0]
##       Robot:     [x=19.861 y=1.4333 orient=0.2886]
##       Robot:     [x=39.034 y=7.1270 orient=0.2886]
##
##
# length = 20.
# bearing_noise  = 0.0
# steering_noise = 0.0
# distance_noise = 0.0

# myrobot = robot(length)
# myrobot.set(0.0, 0.0, 0.0)
# myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

# motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]

# T = len(motions)

# print 'Robot:    ', myrobot
# for t in range(T):
   # myrobot = myrobot.move(motions[t])
   # print 'Robot:    ', myrobot
##
##

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## move function with randomized motion data.

    
## 2) The following code should print:
##      Robot:     [x=0.0 y=0.0 orient=0.0]
##      Robot:     [x=9.9828 y=0.5063 orient=0.1013]
##      Robot:     [x=19.863 y=2.0201 orient=0.2027]
##      Robot:     [x=29.539 y=4.5259 orient=0.3040]
##      Robot:     [x=38.913 y=7.9979 orient=0.4054]
##      Robot:     [x=47.887 y=12.400 orient=0.5067]
##      Robot:     [x=56.369 y=17.688 orient=0.6081]
##      Robot:     [x=64.273 y=23.807 orient=0.7094]
##      Robot:     [x=71.517 y=30.695 orient=0.8108]
##      Robot:     [x=78.027 y=38.280 orient=0.9121]
##      Robot:     [x=83.736 y=46.485 orient=1.0135]
##
##
# length = 20.
# bearing_noise  = 0.0
# steering_noise = 0.0
# distance_noise = 0.0

# myrobot = robot(length)
# myrobot.set(0.0, 0.0, 0.0)
# myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

# motions = [[0.2, 10.] for row in range(10)]

# T = len(motions)

# print 'Robot:    ', myrobot
# for t in range(T):
   # myrobot = myrobot.move(motions[t])
   # print 'Robot:    ', myrobot

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## move function with randomized motion data.


## --------
## TEST CASES FOR SENSE MODEL:
##
## 1) The following code should print the list [6.004885648174475, 3.7295952571373605, 1.9295669970654687, 0.8519663271732721]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print 'Robot:        ', myrobot
print 'Measurements: ', myrobot.sense()
##

## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## sense function with randomized initial robot coordinates.
    

##
## 2) The following code should print the list [5.376567117456516, 3.101276726419402, 1.3012484663475101, 0.22364779645531352]
##
##
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, pi / 5.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print 'Robot:        ', myrobot
print 'Measurements: ', myrobot.sense()
##


## IMPORTANT: You may uncomment the test cases below to test your code.
## But when you submit this code, your test cases MUST be commented
## out. Our testing program provides its own code for testing your
## sense function with randomized initial robot coordinates.