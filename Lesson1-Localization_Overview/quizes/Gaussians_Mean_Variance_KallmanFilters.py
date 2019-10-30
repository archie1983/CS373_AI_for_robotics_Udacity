#!/usr/bin/python

# Write a program to update your mean and variance
# when given the mean and variance of your belief
# and the mean and variance of your measurement.
# This program will update the parameters of your
# belief function.
def update(mean1, var1, mean2, var2):
    new_mean = (mean1 * var2 + mean2 * var1) / (var1 + var2)
    new_var = 1 / (1 / var1 + 1 / var2)
    return [new_mean, new_var]

# Write a program that will predict your new mean
# and variance given the mean and variance of your 
# prior belief and the mean and variance of your 
# motion. 
def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

#print update(10.,8.,13., 2.) # measurement
#print predict(10., 4., 12., 4.) # motion

# Write a program that will iteratively update and
# predict based on the location measurements 
# and inferred motions shown below. 
measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

#Please print out ONLY the final values of the mean
#and the variance in a list [mu, sig]. 

# Insert code here

print [mu, sig]