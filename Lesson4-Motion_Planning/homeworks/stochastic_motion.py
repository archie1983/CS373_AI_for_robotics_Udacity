#!/usr/bin/python

# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    # AE: Ok, so what we're going to do now, is first calculate normal g-values,
    # AE: then pick a random start point (probably just [0, 0]) and recalculate
    # AE: everything with stochastic movement probabilities. Then do it again
    # AE: and again until there are no more changes to the grid. Then we'll have
    # AE: value matrix.
    # AE:
    # AE: So- first the usual breadth-first search and g-values:
    cell_queue = []
    start_cell = goal
    cell_queue.append(start_cell)
    value[goal[0]][goal[1]] = 0
    visited = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    while len(cell_queue) > 0:
        cur_cell = cell_queue.pop(0)
        cur_y = cur_cell[0]
        cur_x = cur_cell[1]
        cur_value = value[cur_y][cur_x]
        visited[cur_y][cur_x] = 1
        
        # AE: now go through all actions
        for ac in range(len(delta)):
            cur_action = delta[ac]
            new_y = cur_y + cur_action[0]
            new_x = cur_x + cur_action[1]

            if (new_y < len(grid) and
                new_y >= 0 and
                new_x < len(grid[0]) and
                new_x >= 0 and
                grid[new_y][new_x] != 1 and
                visited[new_y][new_x] != 1):
                
                cell_queue.append([new_y, new_x])
                value[new_y][new_x] = cur_value + cost_step
    
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
#[471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
#[334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977], 
#[398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738], 
#[700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
