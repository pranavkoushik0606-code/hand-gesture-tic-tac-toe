from game import board, check_winner, is_board_full
import random


# -----------------------------
# MINIMAX ALGORITHM
# -----------------------------

def minimax(board_state, is_maximizing):

    winner = check_winner(board_state)

    if winner == "O":
        return 10

    if winner == "X":
        return -10

    if is_board_full(board_state):
        return 0

    if is_maximizing:

        best_score = -1000

        for row in range(3):
            for col in range(3):

                if board_state[row][col] == "":

                    board_state[row][col] = "O"

                    score = minimax(
                        board_state,
                        False
                    )

                    board_state[row][col] = ""

                    best_score = max(
                        best_score,
                        score
                    )

        return best_score

    else:

        best_score = 1000

        for row in range(3):
            for col in range(3):

                if board_state[row][col] == "":

                    board_state[row][col] = "X"

                    score = minimax(
                        board_state,
                        True
                    )

                    board_state[row][col] = ""

                    best_score = min(
                        best_score,
                        score
                    )

        return best_score


# -----------------------------
# HARD AI (MINIMAX)
# -----------------------------

def ai_move():

    best_score = -1000
    best_move = None

    for row in range(3):
        for col in range(3):

            if board[row][col] == "":

                board[row][col] = "O"

                score = minimax(
                    board,
                    False
                )

                board[row][col] = ""

                if score > best_score:

                    best_score = score
                    best_move = (row, col)

    if best_move:

        row, col = best_move
        board[row][col] = "O"


# -----------------------------
# EASY AI (RANDOM)
# -----------------------------

def easy_move():

    empty_cells = []

    for row in range(3):
        for col in range(3):

            if board[row][col] == "":
                empty_cells.append((row, col))

    if empty_cells:

        row, col = random.choice(empty_cells)
        board[row][col] = "O"


# -----------------------------
# MEDIUM AI
# 50% RANDOM
# 50% MINIMAX
# -----------------------------

def medium_move():

    if random.random() < 0.5:
        easy_move()
    else:
        ai_move()