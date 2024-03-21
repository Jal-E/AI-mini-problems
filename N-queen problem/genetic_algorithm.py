import random
import time

def compute_heuristic(state):
    h = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                h += 1
    return h

def random_state(n=8):
    return [random.randint(0, n - 1) for _ in range(n)]

def crossover(state1, state2):
    n = len(state1)
    c = random.randint(0, n - 1)
    return state1[:c] + state2[c:]

def mutate(state):
    n = len(state)
    i = random.randint(0, n - 1)
    state[i] = random.randint(0, n - 1)
    return state

def genetic_algorithm(population_size=100, generations=1000):
    population = [random_state() for _ in range(population_size)]
    progression = []
    for generation in range(generations):
        population.sort(key=compute_heuristic)
        best_state = population[0]
        best_heuristic = compute_heuristic(best_state)
        progression.append((best_state, best_heuristic))
        if best_heuristic == 0:
            return best_state, generation, progression
        next_generation = population[:2]
        while len(next_generation) < population_size:
            parents = random.sample(population[:50], 2)
            offspring = crossover(parents[0], parents[1])
            if random.random() < 0.1:
                offspring = mutate(offspring)
            next_generation.append(offspring)
        population = next_generation
    return None, generations, progression

def run_analysis(num_runs):
    solved = 0
    total_generations = 0
    total_time = 0
    unique_solutions = set()
    solution_details = []

    for _ in range(num_runs):
        start_time = time.time()
        solution, generations, progression = genetic_algorithm()
        end_time = time.time()
        if solution:
            solved += 1
            if str(solution) not in unique_solutions and len(unique_solutions) < 3:
                unique_solutions.add(str(solution))
                solution_details.append((solution, generations, progression))
        total_generations += generations
        total_time += end_time - start_time

    return (solved / num_runs) * 100, total_generations / num_runs, total_time / num_runs, solution_details

percentage_solved, avg_generations, avg_time, solutions = run_analysis(100)
print(f"Solved: {percentage_solved}%, Average Generations: {avg_generations}, Average Time: {avg_time} seconds")

for i, (solution, generations, progression) in enumerate(solutions, start=1):
    print(f"\nUnique Solution {i}:")
    print(f"Final State: {solution}")
    print("Progression (State, Heuristic):")
    for state, heuristic in progression:
        print(f"{state}, Heuristic: {heuristic}")
    print(f"Total Generations: {generations}")