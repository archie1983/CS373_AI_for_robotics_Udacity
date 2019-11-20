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
    
    # # AE: Ok, so what we're going to do now, is first calculate normal g-values,
    # # AE: then pick a random start point (probably just [0, 0]) and recalculate
    # # AE: everything with stochastic movement probabilities. Then do it again
    # # AE: and again until there are no more changes to the grid. Then we'll have
    # # AE: value matrix.
    # # AE:
    # # AE: So- first the usual breadth-first search and g-values:
    # cell_queue = []
    # start_cell = goal
    # cell_queue.append(start_cell)
    # value[goal[0]][goal[1]] = 0
    # visited = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    
    # while len(cell_queue) > 0:
        # cur_cell = cell_queue.pop(0)
        # cur_y = cur_cell[0]
        # cur_x = cur_cell[1]
        # cur_value = value[cur_y][cur_x]
        # visited[cur_y][cur_x] = 1
        
        # # AE: now go through all actions
        # for ac in range(len(delta)):
            # cur_action = delta[ac]
            # new_y = cur_y + cur_action[0]
            # new_x = cur_x + cur_action[1]

            # if (new_y < len(grid) and
                # new_y >= 0 and
                # new_x < len(grid[0]) and
                # new_x >= 0 and
                # grid[new_y][new_x] != 1 and
                # visited[new_y][new_x] != 1):
                
                # cell_queue.append([new_y, new_x])
                # value[new_y][new_x] = cur_value + cost_step
                
    # AE: A different approach: Pick a random cell (probably just [0, 0]) and take the current initialised
    # AE: value function at its face value (pun not intended) and find the direction with the minimum cost.
    # AE: Use that minimum cost as the new value for that cell and move on to the neighbours. Repeat until
    # AE: no more updates happen.
    # AE:
    # AE: When there are no more changes in the values greater than this, then we'll stop
    max_allowed_change = 0.001
    greatest_change_last_seen = max_allowed_change
    value[goal[0]][goal[1]] = 0
    
    while greatest_change_last_seen >= max_allowed_change:
        # AE: dropping it once we're in the loop to collect the largest value
        greatest_change_last_seen = 0

        # AE: Other than we run it until precision is ok, it's just a normal breadth-first-search.
        cell_queue = []
        start_cell = [2, 3]
        cell_queue.append(start_cell)
        #value[goal[0]][goal[1]] = 0
        visited = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
        
        while not (cell_queue == []):
            cur_cell = cell_queue.pop(0)
            cur_y = cur_cell[0]
            cur_x = cur_cell[1]
            cur_g_value = value[cur_y][cur_x]
            
            if visited[cur_y][cur_x] == 1: continue
            
            visited[cur_y][cur_x] = 1
            
            new_g_value = cur_g_value
            # AE: now go through all actions.
            # AE: So the new value will be 50% of the intended action and 25% of each of the two
            # AE: unintended actions: ((ac - 1) % 4) and ((ac + 1) % 4)
            for ac in range(len(delta)):
                
                # AE: According to the model if we go in this direction (ac), then we will actually
                # AE: perform one of the following three actions: good_action, bad_action1 or bad_action2
                good_action = delta[ac]
                bad_action1 = delta[(ac - 1) % len(delta)]
                bad_action2 = delta[(ac + 1) % len(delta)]
                
                actions_to_explore = [good_action, bad_action1, bad_action2]
                total_action_value = 0.
                
                # AE: let's explore each of these potential actions
                for ate in range(len(actions_to_explore)):
                    cur_action = actions_to_explore[ate]
                    new_y = cur_y + cur_action[0]
                    new_x = cur_x + cur_action[1]
                    cur_action_value = 0.

                    # AE: If this action brings us to a valid new cell, then get that cell's g-value
                    if (new_y < len(grid) and
                        new_y >= 0 and
                        new_x < len(grid[0]) and
                        new_x >= 0 and
                        grid[new_y][new_x] != 1):
                        
                        cur_action_value = value[new_y][new_x] + cost_step
                    else: # but if this action brings us off the world or onto an obstacle, then the value of it is the penalty
                        cur_action_value = collision_cost

                    # AE: At this point we now know what this potential action would cost us, we can add that with the given probability
                    # AE: to the total action cost.
                    if cur_action == good_action:
                        total_action_value += cur_action_value * success_prob
                    else:
                        total_action_value += cur_action_value * failure_prob

                # AE: The total_action_value will also contain the cost for making the move
                total_action_value += cost_step
                
                # AE: If this new total_action_value is less than the value for previous move, then let's take it as a candidate
                # AE: for updating the current g-value.
                if new_g_value > total_action_value:
                    new_g_value = total_action_value
                #print "ate: ", actions_to_explore, " new_g_value=", new_g_value
                
            # AE: Now we have found the best move and its cost. That will then be the new g-value of this cell.
            # AE: The only thing that's left before we move on, is the difference, by how much we change this cell.
            if abs(value[cur_y][cur_x] - new_g_value) > greatest_change_last_seen:
                greatest_change_last_seen = abs(value[cur_y][cur_x] - new_g_value)

            # AE: Updating the g-value
            value[cur_y][cur_x] = new_g_value
            #print("value[",cur_y,"][",cur_x,"] = ", new_g_value)
            
            # AE: Now I'll add the neighbouring cells to the queue so they too get looked at.
            for ac in range(len(delta)):
                cur_action = delta[ac]
                new_y = cur_y + cur_action[0]
                new_x = cur_x + cur_action[1]

                # AE: And of course we only want to explore valid neighbours.
                if (new_y < len(grid) and
                    new_y >= 0 and
                    new_x < len(grid[0]) and
                    new_x >= 0 and
                    grid[new_y][new_x] != 1 and
                    visited[new_y][new_x] != 1):
                    
                    cell_queue.append([new_y, new_x])
                    print("cq: ", cell_queue) 

        print "greatest change seen this cycle : ", greatest_change_last_seen
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
