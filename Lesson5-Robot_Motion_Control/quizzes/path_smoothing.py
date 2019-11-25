#!/usr/bin/python
# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite 
# correct).
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    # AE: We're going to loop until last change seen is smaller than the tolerance.
    last_change_seen = tolerance
    while last_change_seen >= tolerance:
        last_change_seen = 0. # AE: We'll be collecting the change later.
        
        # AE: We need to loop through all elements in the path excepth the first and last ones.
        for i in range(1, len(newpath) - 1):
            # AE: Gradient Descent update.
            # AE: In essence: newpath[i] = newpath[i] + weight_data * (path[i] - newpath[i]) + weight_smooth * (newpath[i + 1] + newpath[i - 1] - 2 * newpath[i])
            cur_point = newpath[i]
            new_point_x = newpath[i][0] + weight_data * (path[i][0] - newpath[i][0]) + weight_smooth * (newpath[i + 1][0] + newpath[i - 1][0] - 2 * newpath[i][0])
            new_point_y = newpath[i][1] + weight_data * (path[i][1] - newpath[i][1]) + weight_smooth * (newpath[i + 1][1] + newpath[i - 1][1] - 2 * newpath[i][1])
            
            if (new_point_x - cur_point[0] > last_change_seen):
                last_change_seen = new_point_x - cur_point[0]
                
            if (new_point_y - cur_point[1] > last_change_seen):
                last_change_seen = new_point_y - cur_point[1]
            
            newpath[i] = [new_point_x, new_point_y]
    
    return newpath # Leave this line for the grader!

printpaths(path,smooth(path))
