8-Puzzle Solver

Overview: This 8-Puzzle Solver is an implementation of the A* search algorithm to efficiently solve the 8-puzzle game. 
It utilizes two heuristic functions: the number of misplaced tiles(h1) and the Manhattan distance(h2).

Features:
	- Solves any solvable 8-puzzle configuration.
	- Allows input of custom puzzle configurations or generates random puzzles.
	- Compares two heuristic functions: misplaced tiles (h1) and Manhattan distance (h2).
	- Outputs step-by-step solution from the initial state to the goal state.

Requirements:
	- Python 3.x
	- NumPy library

Running the Program: 
	- Navigate to the directory containing the script.
	- Run the script using Python:
		"python puzzle_solver.py"
	- Follow the on-screen prompts to input your puzzle or generate a random one.
	- Select the desired heuristic function when prompted.

Input Format:
	- For manual input, enter your puzzle row by row, with each number separated by a space. 
	  For example:
		1 2 3
		4 5 6
		7 8 0

Author:
[Anjali Rai]
