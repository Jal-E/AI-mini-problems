import numpy as np
import heapq
from itertools import count
import random
import time


class PuzzleState:
    def __init__(self, board, parent=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return (self.f, self.g) < (other.f, other.g)

def make_random_move(state):
    zero_row, zero_col = np.argwhere(state == 0)[0]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
    valid_moves = []

    for dx, dy in directions:
        new_row, new_col = zero_row + dx, zero_col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            valid_moves.append((new_row, new_col))

    if not valid_moves:
        return state

    move = random.choice(valid_moves)
    new_state = np.copy(state)
    new_state[zero_row, zero_col], new_state[move] = new_state[move], new_state[zero_row, zero_col]
    return new_state

def is_solvable(board):
    flat_board = board.flatten()
    inversions = sum(1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)) if
                     flat_board[j] and flat_board[i] and flat_board[i] > flat_board[j])
    return inversions % 2 == 0


def calculate_misplaced_tiles(board, goal):
    return np.sum(board != goal) - 1  # Subtract 1 for the empty tile


def calculate_manhattan_distance(board, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if board[i, j] != 0:
                x, y = divmod(goal.flatten().tolist().index(board[i, j]), 3)
                distance += abs(x - i) + abs(y - j)
    return distance


def get_successors(current_state, heuristic, goal_state):
    successors = []
    zero_row, zero_col = np.argwhere(current_state.board == 0)[0]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

    for dx, dy in directions:
        new_row, new_col = zero_row + dx, zero_col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_board = np.copy(current_state.board)
            new_board[zero_row, zero_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[
                zero_row, zero_col]
            g = current_state.g + 1
            h = heuristic(new_board)
            successors.append(PuzzleState(new_board, current_state, g, h))

    return successors


def a_star_search(initial_state, heuristic, goal_state):
    open_set = []
    closed_set = set()
    counter = count()
    nodes_generated = 0  # Counter for the number of nodes generated

    heapq.heappush(open_set, (initial_state.f, next(counter), initial_state))
    nodes_generated += 1

    while open_set:
        current_state = heapq.heappop(open_set)[2]

        if np.array_equal(current_state.board, goal_state):
            return build_solution_path(current_state), nodes_generated

        closed_set.add(tuple(map(tuple, current_state.board)))

        for successor in get_successors(current_state, heuristic, goal_state):
            if tuple(map(tuple, successor.board)) in closed_set:
                continue

            heapq.heappush(open_set, (successor.f, next(counter), successor))
            nodes_generated += 1

    return None, nodes_generated



def build_solution_path(state):
    path = []
    while state:
        path.insert(0, state.board)
        state = state.parent
    return path

goal_state = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
def read_manual_puzzle():
    puzzle = []
    print("Enter your puzzle, row by row (3 rows, 3 numbers per row, separated by spaces):")
    for _ in range(3):
        row = input().split()
        puzzle.append([int(num) for num in row])
    return np.array(puzzle)

def main():
    input_method = int(input("Select Input Method:\n[1] Random\n[2] Manual\n"))

    if input_method == 1:
        d = int(input("Enter desired solution depth (2-20): "))
        if d < 2 or d > 20:
            print("Invalid depth. Please choose a depth between 2 and 20.")
            return

        initial_state = np.array(goal_state)
        for _ in range(d):
            initial_state = make_random_move(initial_state)

    elif input_method == 2:
        initial_state = read_manual_puzzle()
        if not is_solvable(initial_state):
            print("Puzzle is unsolvable.")
            return

    print("Puzzle:")
    print('\n'.join(' '.join(str(cell) for cell in row) for row in initial_state))

    heuristic_choice = int(input("Select Heuristic Function [1] H1 (Misplaced Tiles) [2] H2 (Manhattan Distance): "))
    heuristic_function = calculate_misplaced_tiles if heuristic_choice == 1 else calculate_manhattan_distance
    heuristic = lambda board: heuristic_function(board, goal_state)

    start_time = time.time()
    solution, search_cost = a_star_search(PuzzleState(initial_state), heuristic, goal_state)
    end_time = time.time()
    if solution:
        print("Solution Found")
        for i, step in enumerate(solution, 1):
            print(f"Step: {i}")
            print('\n'.join(' '.join(str(cell) for cell in row) for row in step))
        print(f"H{heuristic_choice} Search Cost: {search_cost}")
        print(f"H{heuristic_choice} Time: {end_time - start_time} seconds")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
