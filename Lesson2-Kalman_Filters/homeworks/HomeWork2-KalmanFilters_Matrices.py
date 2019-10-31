#!/usr/bin/python

# Write a function 'kalman_filter' that implements a multi-
# dimensional Kalman Filter for the example given

from math import *


class matrix:
    
    # implements basic operations of a matrix class
    
    def __init__(self, value):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0
    
    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]
    
    def identity(self, dim):
        # check if valid dimension
        if dim < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dim
            self.dimy = dim
            self.value = [[0 for row in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1
    
    def show(self):
        for i in range(self.dimx):
            print(self.value[i])
        print(' ')
    
    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to add"
        else:
            # add if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res
    
    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to subtract"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res
    
    def __mul__(self, other):
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError, "Matrices must be m*n and n*p to multiply"
        else:
            # multiply if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
            return res
    
    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res
    
    # Thanks to Ernesto P. Adorio for use of Cholesky and CholeskyInverse functions
    
    def Cholesky(self, ztol=1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError, "Matrix not positive-definite"
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                try:
                   res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
                except:
                   raise ValueError, "Zero diagonal"
        return res
    
    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)


########################################

# Implement the filter function below

def kalman_filter(x, P):
    for n in range(len(measurements)):
        
        # measurement update (sensor reading of where we are in this step)
        y = matrix([[measurements[n]]]) - H * x
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + (K * y)
        P = (I - K * H) * P
        print "update : "
        x.show()
        print "P: "
        P.show()
        
        # prediction (of where we should end up in the next (not this, but next) step)
        x = F * x + u
        P = F * P * F.transpose()
        print "predict : "
        x.show()
        print "P: "
        P.show()
        
    return x,P

############################################
### use the code below to test your filter!
############################################

measurements = [1, 2, 3]

x = matrix([[0.], [0.]]) # initial state (location and velocity) - a.k.a. the mean or mu variable (in 1D Gaussian)
P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty - a.k.a. the covariance or in 1D Gaussian - the variance or sigma squared
u = matrix([[0.], [0.]]) # external motion
F = matrix([[1., 1.], [0, 1.]]) # next state function - a.k.a. state transition function - the matrix that we multiply current state with to get to the next state
H = matrix([[1., 0.]]) # measurement function - a.k.a. the vector that we use for updating measurement - we update location (hence first element is 1) and we don't update speed (hence second element is 0)
R = matrix([[1.]]) # measurement uncertainty
I = matrix([[1., 0.], [0., 1.]]) # identity matrix

print "very first P: "
P.show()
        
print(kalman_filter(x, P))
# output should be:
# x: [[3.9996664447958645], [0.9999998335552873]]
# P: [[2.3318904241194827, 0.9991676099921091], [0.9991676099921067, 0.49950058263974184]]

## What I'm getting is really awesome:
#
## So we start at position=0 and speed=0 : x = matrix([[0.], [0.]])
## Covariance is very very uncertain (1000 uncertainty for location and same for speed) : P = matrix([[1000., 0.], [0., 1000.]])
#
## Now we take in a measurement of location (first measurement is 1)
#
#update :
#[0.9990009990009988]
#[0.0]
#
## And low and behold our idea of location is now very close to 1 (not exactly 1, because even though at high uncertainty,
## but still we thought we were at 0 before this measurement)
## Since we only have taken 1 measurement so far, we can't know the speed, so that is still 0
##
#P:
#[0.9990009990011872, 0.0]
#[0.0, 1000.0]
##
## And our uncertainty covariance after this measurement says that we're a lot more confident about our location 
## ([0.9990009990011872, 0.0]), but as for speed we're just a unconvinced as before ([0.0, 1000.0])
##
## Now we'll try to predict where we'll be in the next step (where we're heading)
#
#predict :
#[0.9990009990009988]
#[0.0]
#
## And since we've only taken 1 measurement so far, we can't know the speed any better than before and based on that
## we think that we'll stay at the same place.
##
#P:
#[1000.9990009990012, 1000.0]
#[1000.0, 1000.0]
##
## And the uncertainty about such prediction is still very high for both - the speed and the location
##
## Now let's take in the next update with a new position (this time 2)
#
#update :
#[1.9990009980049868]
#[0.9990019950129659]
#
## So we measured 2, right? That means that we're very close to location 2 (remember there's still tiny residue of 
## previous very uncertain location of 0).
## And the speed must be very close to 1, since we were at location 1 before and are now at location 2 (after 1 time step)
## 
#P:
#[0.9990019950130065, 0.9980049870339514]
#[0.9980049870339371, 1.9950129660888933]
##
## And our uncertainty covariance after this measurement is much lower for both speed and location
##
## Now let's see where we think we'll end up in the next step if we carry on like this.
#
#predict :
#[2.998002993017953]
#[0.9990019950129659]
#
## And according to the data that we have, we will be at location 3 (or very close to 3) and our speed should still be about 1.
##
#P:
#[4.990024935169789, 2.9930179531228447]
#[2.9930179531228305, 1.9950129660888933]
##
## And our uncertainty for this prediction is slightly higher than after measurement, but we're now much more confident that at
## the beginning
##
## Now let's take in the next (and in the homework case - the final measurement) - measurement of location 3
#
#update :
#[2.999666611240577]
#[0.9999998335552873]
#
## So yes, we're at 3 and our speed is still 1
##
#P:
#[0.8330557867750087, 0.49966702735236723]
#[0.4996670273523649, 0.49950058263974184]
##
## We're also getting more confident.
##
## And what do we think about next step if we carry on like this?
#
#predict :
#[3.9996664447958645]
#[0.9999998335552873]
#
## We think that we'll end up at location 4 and speed will still be 1.
##
#P:
#[2.3318904241194827, 0.9991676099921091]
#[0.9991676099921067, 0.49950058263974184]
##
## And the uncertainty for this kind of prediction of movement is now getting closer and closer to the uncertainty that we 
## get from measurement.
##
## AND THAT IS MASSIVELY COOL :)
