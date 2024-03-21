import numpy as np
import time
from itertools import product

def print_board(board):
    print("  1 2 3 4 5 6 7 8")
    rows = 'ABCDEFGH'
    for i, row in enumerate(board):
        print(f"{rows[i]} {' '.join('O' if cell == 2 else 'X' if cell == 1 else '-' for cell in row)}")

def initialize_board():
    return np.zeros((8, 8), dtype=int)

def get_human_move(board):
    while True:
        move = input("Choose your next move (e.g., A1): ").upper()
        if len(move) == 2 and move[0] in 'ABCDEFGH' and move[1].isdigit():
            i, j = 'ABCDEFGH'.index(move[0]), int(move[1]) - 1
            if 0 <= j < 8 and board[i][j] == 0:
                return i, j
        print("Invalid move. Please try again.")

def is_winner(board, player):
    for i in range(8):
        for j in range(5):
            if np.all(board[i, j:j + 4] == player) or np.all(board[j:j + 4, i] == player):
                return True
    return False

def is_draw(board):
    return not np.any(board == 0)

def evaluate(board):
    if is_winner(board, 1):
        return 10000
    elif is_winner(board, 2):
        return -10000
    score = dynamic_scoring(board) + positional_score(board, 1) - positional_score(board, 2)
    return score

def dynamic_scoring(board):
    remaining_moves = 64 - np.count_nonzero(board)
    if remaining_moves <= 10:
        return score_board(board, 1, 1000, -1000) - score_board(board, 2, -1500, 1500)
    else:
        return score_board(board, 1, 100, -200) - score_board(board, 2, -300, 300)

def positional_score(board, player):
    positional_values = np.array([
        [3, 4, 5, 5, 5, 5, 4, 3],
        [4, 6, 8, 8, 8, 8, 6, 4],
        [5, 8, 11, 11, 11, 11, 8, 5],
        [5, 8, 11, 12, 12, 11, 8, 5],
        [5, 8, 11, 12, 12, 11, 8, 5],
        [5, 8, 11, 11, 11, 11, 8, 5],
        [4, 6, 8, 8, 8, 8, 6, 4],
        [3, 4, 5, 5, 5, 5, 4, 3]
    ])
    return np.sum(positional_values[board == player])

def score_board(board, player, win_score, block_score):
    score = 0
    opponent = 2 if player == 1 else 1
    for i in range(8):
        for j in range(6):
            score += line_score(board, i, j, player, opponent, win_score, block_score)
    score += diagonal_score(board, player, opponent, win_score, block_score)
    return score

def line_score(board, i, j, player, opponent, win_score, block_score):
    line_score = 0
    if np.sum(board[i, j:j+3] == player) == 3 and board[i, j+3] == 0:
        line_score += win_score
    if np.sum(board[j:j+3, i] == player) == 3 and board[j+3, i] == 0:
        line_score += win_score
    if np.sum(board[i, j:j+3] == opponent) == 3 and board[i, j+3] == 0:
        line_score += block_score
    if np.sum(board[j:j+3, i] == opponent) == 3 and board[j+3, i] == 0:
        line_score += block_score
    return line_score

def diagonal_score(board, player, opponent, win_score, block_score):
    diag_score = 0
    for i in range(5):
        for j in range(5):
            if np.sum([board[i+k, j+k] == player for k in range(3)]) == 3 and (i+3 < 8 and j+3 < 8 and board[i+3, j+3] == 0):
                diag_score += win_score
            if np.sum([board[i+3-k, j+k] == player for k in range(3)]) == 3 and (i >= 3 and j+3 < 8 and board[i-3, j+3] == 0):
                diag_score += win_score
            if np.sum([board[i+k, j+k] == opponent for k in range(3)]) == 3 and (i+3 < 8 and j+3 < 8 and board[i+3, j+3] == 0):
                diag_score += block_score
            if np.sum([board[i+3-k, j+k] == opponent for k in range(3)]) == 3 and (i >= 3 and j+3 < 8 and board[i-3, j+3] == 0):
                diag_score += block_score
    return diag_score

def minimax(board, depth, alpha, beta, maximizing_player, start_time, time_limit):
    if time.time() - start_time > time_limit:
        return 0, None, None
    if depth == 0 or is_winner(board, 1) or is_winner(board, 2) or is_draw(board):
        score = evaluate(board)
        return score, None, None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for i, j in product(range(8), repeat=2):
            if board[i][j] == 0:
                board[i][j] = 1
                eval, _, _ = minimax(board, depth - 1, alpha, beta, False, start_time, time_limit)
                board[i][j] = 0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (i, j)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, *best_move
    else:
        min_eval = float('inf')
        best_move = None
        for i, j in product(range(8), repeat=2):
            if board[i][j] == 0:
                board[i][j] = 2
                eval, _, _ = minimax(board, depth - 1, alpha, beta, True, start_time, time_limit)
                board[i][j] = 0
                if eval < min_eval:
                    min_eval = eval
                    best_move = (i, j)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval, *best_move

def game_loop():
    board = initialize_board()
    print_board(board)
    first_player = input("Would you like to go first? (y/n): ").strip().lower() == 'y'
    time_limit = float(input("How long should the computer think about its moves (in seconds)? : "))
    turn = first_player
    while True:
        if turn:
            i, j = get_human_move(board)
            board[i][j] = 2
            if is_winner(board, 2):
                print("Human wins!")
                break
        else:
            start_time = time.time()
            _, i, j = minimax(board, 5, float('-inf'), float('inf'), True, start_time, time_limit)
            end_time = time.time()
            if i is not None and j is not None:
                board[i][j] = 1
                print(f"Computer places on {chr(65 + i)}{j + 1} (Time taken: {end_time - start_time:.2f}s)")
                if is_winner(board, 1):
                    print("Computer wins!")
                    break
        print_board(board)
        if is_draw(board):
            print("It's a draw!")
            break
        turn = not turn

game_loop()
