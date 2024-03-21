import random
import time

#Compute the heuristic value of a state: number of pairs of queens attacking each other.
def compute_heuristic(state):
    h = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            # Check for queens in the same row or diagonal
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                h += 1
    return h

#Generate the neighbor states of a given state by moving one queen at a time.
def get_neighbors(state):
    neighbors = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i] != j:
                # Move queen i to row j
                new_state = list(state)
                new_state[i] = j
                neighbors.append(new_state)
    return neighbors

#Perform the Steepest-Ascent Hill Climbing algorithm.
def steepest_ascent_hill_climbing(initial_state):
    current_state = initial_state
    while True:
        current_heuristic = compute_heuristic(current_state)
        neighbors = get_neighbors(current_state)
        next_state = current_state
        next_heuristic = current_heuristic
        for neighbor in neighbors:
            h = compute_heuristic(neighbor)
            if h < next_heuristic:
                next_state = neighbor
                next_heuristic = h
        if next_heuristic >= current_heuristic:
            return current_state, current_heuristic == 0  # Return state and whether it's a solution
        current_state = next_state

#Run the algorithm on 100 instances and record the performance.
def run_analysis(num_instances):
    solved = 0
    total_cost = 0
    total_time = 0
    for _ in range(num_instances):
        initial_state = [random.randint(0, 7) for _ in range(8)]
        start_time = time.time()
        final_state, is_solution = steepest_ascent_hill_climbing(initial_state)
        end_time = time.time()
        total_time += end_time - start_time
        total_cost += compute_heuristic(final_state)
        if is_solution:
            solved += 1
    return (solved / num_instances) * 100, total_cost / num_instances, total_time / num_instances


percentage_solved, avg_cost, avg_time = run_analysis(100)
print(f"Solved: {percentage_solved}%, Average Cost: {avg_cost}, Average Time: {avg_time} seconds")
